#!/usr/bin/env python3
#
# generated by wxGlade 1.0.0 on Thu Feb  3 06:49:54 2022
#
import os
import threading

import wx

from meerk40t.gui.icons import (
    get_default_icon_size,
    icons8_connected,
    icons8_disconnected,
)
from meerk40t.gui.mwindow import MWindow
from meerk40t.gui.wxutils import dip_size, wxButton, wxStaticText, TextCtrl
from meerk40t.kernel import signal_listener

_ = wx.GetTranslation

realtime_commands = (
    "!",  # pause
    "~",  # resume
    "?",  # status report
    # "$X",
)


class GRBLControllerPanel(wx.Panel):
    def __init__(self, *args, context=None, **kwds):
        # begin wxGlade: SerialControllerPanel.__init__
        self.service = context
        kwds["style"] = kwds.get("style", 0)
        wx.Panel.__init__(self, *args, **kwds)
        self.service.themes.set_window_colors(self)
        self.SetHelpText("grblcontoller")
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        self.iconsize = 0.75 * get_default_icon_size(context)
        self.state = None
        self.button_device_connect = wxButton(
            self, wx.ID_ANY, self.button_connect_string("Connection")
        )

        self.button_device_connect.SetFont(
            wx.Font(
                12,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                0,
                "Segoe UI",
            )
        )
        self.button_device_connect.SetToolTip(
            _("Force connection/disconnection from the device.")
        )
        self.button_device_connect.SetBitmap(
            icons8_connected.GetBitmap(use_theme=False, resize=self.iconsize)
        )
        sizer_1.Add(self.button_device_connect, 0, wx.EXPAND, 0)

        static_line_2 = wx.StaticLine(self, wx.ID_ANY)
        static_line_2.SetMinSize(dip_size(self, 483, 5))
        sizer_1.Add(static_line_2, 0, wx.EXPAND, 0)

        self.data_exchange = TextCtrl(self, wx.ID_ANY, "", style=wx.TE_MULTILINE)
        self.data_exchange.SetMinSize(dip_size(self, -1, 100))
        sizer_1.Add(self.data_exchange, 1, wx.EXPAND, 0)

        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        self.gcode_commands = list()
        if self.service.has_endstops:
            self.gcode_commands.append(
                (
                    "$H",
                    _("Physical Home"),
                    _("Send laser to physical home-position"),
                    None,
                ),
            )
        else:
            self.gcode_commands.append(
                ("G28", _("Home"), _("Send laser to logical home-position"), None)
            )
        self.gcode_commands.extend(
            [
                ("\x18", _("Reset"), _("Reset laser"), None),
                ("?", _("Status"), _("Query status"), None),
                ("$X", _("Clear Alarm"), _("Kills alarms and locks"), None),
                ("$#", _("Gcode"), _("Display active Gcode-parameters"), None),
                ("$$", _("GRBL"), _("Display active GRBL-parameters"), None),
                ("$I", _("Info"), _("Show Build-Info"), None),
            ]
        )
        for entry in self.gcode_commands:
            btn = wxButton(self, wx.ID_ANY, entry[1])
            btn.Bind(wx.EVT_BUTTON, self.send_gcode(entry[0]))
            btn.SetToolTip(entry[2])
            if entry[3] is not None:
                btn.SetBitmap(
                    entry[3].GetBitmap(
                        resize=0.5 * get_default_icon_size(self.context), use_theme=False
                    )
                )
            sizer_2.Add(btn, 1, wx.EXPAND, 0)

        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        self.macros = []
        for idx in range(5):
            macrotext = self.service.setting(str, f"macro_{idx}", "")
            self.macros.append(macrotext)
            btn = wxButton(self, wx.ID_ANY, f"Macro {idx+1}")
            btn.Bind(wx.EVT_BUTTON, self.send_macro(idx))
            btn.Bind(wx.EVT_RIGHT_DOWN, self.edit_macro(idx))
            btn.SetToolTip(_("Send list of commands to device. Right click to edit."))
            sizer_3.Add(btn, 1, wx.EXPAND, 0)

        self.btn_clear = wxButton(self, wx.ID_ANY, _("Clear"))
        self.btn_clear.SetToolTip(_("Clear log window"))
        self.btn_clear.Bind(wx.EVT_BUTTON, self.on_clear_log)
        sizer_3.Add(self.btn_clear, 0, wx.EXPAND), 0

        sizer_1.Add(sizer_2, 0, wx.EXPAND, 0)
        sizer_1.Add(sizer_3, 0, wx.EXPAND, 0)

        self.gcode_text = TextCtrl(self, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        self.gcode_text.SetToolTip(_("Enter a Gcode-Command and send it to the laser"))
        self.gcode_text.SetFocus()
        sizer_1.Add(self.gcode_text, 0, wx.EXPAND, 0)

        self.SetSizer(sizer_1)

        self.Layout()

        self.Bind(
            wx.EVT_BUTTON, self.on_button_start_connection, self.button_device_connect
        )
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_down, self.gcode_text)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_gcode_enter, self.gcode_text)
        self._buffer = ""
        self._buffer_lock = threading.Lock()
        # end wxGlade
        self.set_color_according_to_state(self.state, self.button_device_connect)
        self.command_log = []
        self.command_position = 0
        self.load_log()

    def history_filename(self):
        safe_dir = self.service.kernel.os_information["WORKDIR"]
        fname = os.path.join(safe_dir, "grblhistory.log")
        is_there = os.path.exists(fname)
        return fname, is_there

    def save_log(self, last_command):
        fname, fexists = self.history_filename()
        try:
            history_file = open(fname, "a", encoding="utf-8")  # Append mode
            history_file.write(last_command + "\n")
            history_file.close()
        except (PermissionError, OSError):
            # Could not save
            pass

    def load_log(self):
        def tail(fs, window=1):
            """
            Returns the last `window` lines of file `f` as a list of bytes.
            """
            if window == 0:
                return b""
            BUFSIZE = 1024
            fs.seek(0, 2)
            end = fs.tell()
            nlines = window + 1
            data = []
            while nlines > 0 and end > 0:
                i = max(0, end - BUFSIZE)
                nread = min(end, BUFSIZE)

                fs.seek(i)
                chunk = fs.read(nread)
                data.append(chunk)
                nlines -= chunk.count(b"\n")
                end -= nread
            return b"\n".join(b"".join(reversed(data)).splitlines()[-window:])

        # Restores the last 50 commands from disk

        self.service.setting(int, "history_limit", 50)
        limit = int(self.service.history_limit)
        # print (f"Limit = {limit}")
        self.command_log = [""]
        fname, fexists = self.history_filename()
        if fexists:
            result = []
        if fexists:
            result = []
            try:
                with open(fname, "rb") as f:
                    result = (
                        tail(f, 3 * limit).decode("utf-8", errors="ignore").splitlines()
                    )
            except (PermissionError, OSError):
                # Could not load
                pass
            for entry in result:
                if len(self.command_log) and entry == self.command_log[-1]:
                    # print (f"ignored duplicate {entry}")
                    continue
                self.command_log.append(entry)
            if len(self.command_log) > limit:
                self.command_log = self.command_log[-limit:]

    def button_connect_string(self, pattern):
        res = _(pattern)
        context = self.service
        if context.permit_serial and context.interface == "serial":
            iface = "?" if context.serial_port is None else context.serial_port
        elif context.permit_tcp and context.interface == "tcp":
            iface = f"{context.address}:{context.port}"
        elif context.permit_ws and context.interface == "tcp":
            iface = f"ws://{context.address}:{context.port}"
        elif context.permit_ws and context.interface == "ws":
            iface = f"ws://{context.address}:{context.port}"
        else:
            # Mock
            iface = "Mock"

        res += f" ({iface})"
        return res

    def on_clear_log(self, event):
        self.data_exchange.SetValue("")

    def on_button_start_connection(
        self, event
    ):  # wxGlade: SerialControllerPanel.<event_handler>
        if self.state == "connected":
            self.service.controller.stop()
        else:
            self.service.controller.start()

    def send_gcode(self, gcode_cmd):
        def handler(event):
            self.service(f"gcode_realtime {gcode_cmd}")
            if gcode_cmd == "$X" and self.service.extended_alarm_clear:
                self.service("gcode_realtime \x18")

        return handler

    def send_macro(self, idx):
        def handler(event):
            macro = self.macros[idx]
            for line in macro.splitlines():
                if line.startswith("#"):
                    self.command_log.append(f"Macro {idx + 1}: {line}")
                else:
                    self.service.driver(f"{line}{self.service.driver.line_end}")
        return handler

    def edit_macro(self, idx):
        def handler(event):
            macro = self.macros[idx]
            dlg = wx.TextEntryDialog(
                self, _("Content for macro {index}").format(index = idx + 1),
                value=macro,
                style=wx.TE_MULTILINE | wx.OK | wx.CANCEL | wx.CENTRE | wx.ICON_QUESTION,
            )
            dlg.ShowModal()
            newmacro = dlg.GetValue()
            dlg.Destroy()
            if newmacro != macro:
                self.macros[idx] = newmacro
                setattr(self.service, f"macro_{idx}", newmacro)

        return handler

    def on_key_down(self, event):
        key = event.GetKeyCode()
        try:
            if key == wx.WXK_DOWN:
                self.gcode_text.SetValue(self.command_log[self.command_position + 1])
                if not wx.IsMainThread():
                    wx.CallAfter(self.gcode_text.SetInsertionPointEnd)
                else:
                    self.gcode_text.SetInsertionPointEnd()
                self.command_position += 1
            elif key == wx.WXK_UP:
                self.gcode_text.SetValue(self.command_log[self.command_position - 1])
                if not wx.IsMainThread():
                    wx.CallAfter(self.gcode_text.SetInsertionPointEnd)
                else:
                    self.gcode_text.SetInsertionPointEnd()
                self.command_position -= 1
                # We are consuming the key...
            else:
                event.Skip()
        except IndexError:
            self.command_position = 0
            self.gcode_text.SetValue("")

    def on_gcode_enter(self, event):  # wxGlade: SerialControllerPanel.<event_handler>
        cmd = self.gcode_text.GetValue()
        self.command_log.append(cmd)
        self.save_log(cmd)
        self.command_position = 0
        if cmd in realtime_commands:
            self.service(f"gcode_realtime {cmd}")
        else:
            self.service(f"gcode {cmd}")
        self.gcode_text.Clear()

    def update(self, data, type):
        if type == "send":
            # Quick judgement call: first character extended ascii?
            # Then show all in hex:
            if len(data) > 0 and ord(data[0]) >= 128:
                display = "0x"
                idx = 0
                for c in data:
                    if idx > 0:
                        display += " "
                    display += f"{ord(c):02x}"
                    idx += 1
            else:
                display = data
            with self._buffer_lock:
                self._buffer += f"<--{display}\n"
            self.service.signal("grbl_controller_update", True)
        elif type == "recv":
            with self._buffer_lock:
                self._buffer += f"-->\t{data}\n"
            self.service.signal("grbl_controller_update", True)
        elif type == "event":
            with self._buffer_lock:
                self._buffer += f"{data}\n"
            self.service.signal("grbl_controller_update", True)
        elif type == "connection":
            with self._buffer_lock:
                self._buffer += f"{data}\n"
            self.service.signal("grbl_controller_update", True)

    @signal_listener("update_interface")
    def update_button_gui(self, origin, *args):
        self.on_status(origin, self.state)

    @signal_listener("grbl_controller_update")
    def update_text_gui(self, origin, *args):
        with self._buffer_lock:
            buffer = self._buffer
            self._buffer = ""
        self.data_exchange.AppendText(buffer)

    def set_color_according_to_state(self, stateval, control):
        def color_distance(c1, c2):
            from math import sqrt

            red_mean = int((c1.red + c2.red) / 2.0)
            r = c1.red - c2.red
            g = c1.green - c2.green
            b = c1.blue - c2.blue
            distance_sq = (
                (((512 + red_mean) * r * r) >> 8)
                + (4 * g * g)
                + (((767 - red_mean) * b * b) >> 8)
            )
            return sqrt(distance_sq)

        if stateval is None:
            stateval = "UNINITIALIZED"
        stateval = stateval.upper()
        state_colors = {
            "UNINITIALIZED": wx.Colour("#ffff00"),
            "DISCONNECTED": wx.Colour("#ffff00"),
            "CONNECTED": wx.Colour("#00ff00"),
            "STATE_DRIVER_NO_BACKEND": wx.Colour("#dfdf00"),
            "STATE_UNINITIALIZED": wx.Colour("#ffff00"),
            "STATE_USB_DISCONNECTED": wx.Colour("#ffff00"),
            "STATE_USB_SET_DISCONNECTING": wx.Colour("#ffff00"),
            "STATE_USB_CONNECTED": wx.Colour("#00ff00"),
            "STATE_CONNECTED": wx.Colour("#00ff00"),
            "STATE_CONNECTING": wx.Colour("#ffff00"),
            "CONNECTION ERROR": wx.Colour("#dfdf00"),
        }
        if stateval in state_colors:
            bgcol = state_colors[stateval]
        else:
            bgcol = state_colors["UNINITIALIZED"]
        d1 = color_distance(bgcol, wx.BLACK)
        d2 = color_distance(bgcol, wx.WHITE)
        # print(f"state={stateval}, to black={d1}, to_white={d2}")
        if d1 <= d2:
            fgcol = wx.WHITE
        else:
            fgcol = wx.BLACK
        control.SetBackgroundColour(bgcol)
        control.SetForegroundColour(fgcol)

    def on_status(self, origin, state):
        self.state = state
        self.set_color_according_to_state(state, self.button_device_connect)
        if state == "uninitialized" or state == "disconnected" or state is None:
            self.button_device_connect.SetLabel(self.button_connect_string("Connect"))
            self.button_device_connect.SetBitmap(
                icons8_disconnected.GetBitmap(use_theme=False, resize=self.iconsize)
            )
            self.button_device_connect.Enable()
        elif state == "connected":
            self.button_device_connect.SetLabel(
                self.button_connect_string("Disconnect")
            )
            self.button_device_connect.SetBitmap(
                icons8_connected.GetBitmap(use_theme=False, resize=self.iconsize)
            )
            self.button_device_connect.Enable()

    def pane_show(self):
        if (
            self.state is None
            or self.state == "uninitialized"
            or self.state == "disconnected"
        ):
            self.set_color_according_to_state(self.state, self.button_device_connect)
            self.button_device_connect.SetLabel(self.button_connect_string("Connect"))
            self.button_device_connect.SetBitmap(
                icons8_disconnected.GetBitmap(use_theme=False, resize=self.iconsize)
            )
            self.button_device_connect.Enable()
        elif self.state == "connected":
            self.set_color_according_to_state(self.state, self.button_device_connect)
            self.button_device_connect.SetLabel(
                self.button_connect_string("Disconnect")
            )
            self.button_device_connect.SetBitmap(
                icons8_connected.GetBitmap(use_theme=False, resize=self.iconsize)
            )
            self.button_device_connect.Enable()

    def pane_hide(self):
        return


class GRBLController(MWindow):
    def __init__(self, *args, **kwds):
        super().__init__(499, 357, *args, **kwds)
        self.service = self.context.device
        self.SetTitle(_("GRBL Controller"))
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(icons8_connected.GetBitmap())
        self.SetIcon(_icon)

        self.serial_panel = GRBLControllerPanel(self, wx.ID_ANY, context=self.service)
        self.sizer.Add(self.serial_panel, 1, wx.EXPAND, 0)
        self.Layout()
        self._opened_port = None
        self.restore_aspect()

    @signal_listener("grbl;status")
    def on_serial_status(self, origin, state):
        self.serial_panel.on_status(origin, state)

    def window_open(self):
        try:
            self.service.controller.add_watcher(self.serial_panel.update)
        except AttributeError:
            pass
        self.serial_panel.pane_show()

    def window_close(self):
        try:
            self.service.controller.remove_watcher(self.serial_panel.update)
        except AttributeError:
            pass
        self.serial_panel.pane_hide()

    def delegates(self):
        yield self.serial_panel

    @staticmethod
    def submenu():
        return "Device-Control", "GRBL Controller"

    @staticmethod
    def helptext():
        return _("Open the device controller window")
