# -*- coding: ISO-8859-1 -*-
#
# generated by wxGlade 0.9.3 on Fri Jun 28 16:25:14 2019
#

import wx

from meerk40t.gui.icons import (
    icons8_connected_50,
    icons8_disconnected_50,
    icons8_emergency_stop_button_50,
    icons8_laser_beam_hazard_50,
    icons8_pause_50,
    icons8_play_50,
)
from meerk40t.gui.mwindow import MWindow
from meerk40t.kernel import (
    STATE_ACTIVE,
    STATE_BUSY,
    STATE_END,
    STATE_IDLE,
    STATE_INITIALIZE,
    STATE_PAUSE,
    STATE_TERMINATE,
    STATE_WAIT,
)

_ = wx.GetTranslation

_simple_width = 500
_advanced_width = 952
_default_height = 565


class LhystudiosControllerGui(MWindow):
    def __init__(self, *args, **kwds):
        super().__init__(_advanced_width, _default_height, *args, **kwds)

        # Menu Bar
        self.LhystudiosController_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Reset USB", "Reset USB connection")
        self.Bind(wx.EVT_MENU, self.on_menu_usb_reset, id=item.GetId())
        item = wxglade_tmp_menu.Append(
            wx.ID_ANY, "Release USB", "Release USB resources"
        )
        self.Bind(wx.EVT_MENU, self.on_menu_usb_release, id=item.GetId())
        self.LhystudiosController_menubar.Append(wxglade_tmp_menu, "Tools")
        wxglade_tmp_menu = wx.Menu()
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Pause", "")
        self.Bind(wx.EVT_MENU, self.on_menu_pause, id=item.GetId())
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Stop", "")
        self.Bind(wx.EVT_MENU, self.on_menu_stop, id=item.GetId())
        self.LhystudiosController_menubar.Append(wxglade_tmp_menu, "Commands")
        wxglade_tmp_menu = wx.Menu()
        item = wxglade_tmp_menu.Append(
            wx.ID_ANY, "BufferView", "Views the Controller Buffer"
        )
        self.Bind(wx.EVT_MENU, self.on_menu_bufferview, id=item.GetId())
        self.LhystudiosController_menubar.Append(wxglade_tmp_menu, "Views")
        self.SetMenuBar(self.LhystudiosController_menubar)
        # Menu Bar end
        self.button_device_connect = wx.Button(self, wx.ID_ANY, "Connection")
        self.text_connection_status = wx.TextCtrl(
            self, wx.ID_ANY, "", style=wx.TE_READONLY
        )
        self.checkbox_mock_usb = wx.CheckBox(
            self, wx.ID_ANY, "Mock USB Connection Mode"
        )
        self.text_device_index = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        self.spin_device_index = wx.SpinCtrl(self, wx.ID_ANY, "-1", min=-1)
        self.text_device_address = wx.TextCtrl(
            self, wx.ID_ANY, "", style=wx.TE_READONLY
        )
        self.spin_device_address = wx.SpinCtrl(self, wx.ID_ANY, "-1", min=-1)
        self.text_device_bus = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        self.spin_device_bus = wx.SpinCtrl(self, wx.ID_ANY, "-1", min=-1)
        self.text_device_version = wx.TextCtrl(
            self, wx.ID_ANY, "", style=wx.TE_READONLY
        )
        self.spin_device_version = wx.SpinCtrl(self, wx.ID_ANY, "-1", min=-1, max=255)
        self.button_controller_control = wx.Button(self, wx.ID_ANY, "Start Controller")
        self.text_controller_status = wx.TextCtrl(
            self, wx.ID_ANY, "", style=wx.TE_READONLY
        )
        self.packet_count_text = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        self.rejected_packet_count_text = wx.TextCtrl(
            self, wx.ID_ANY, "", style=wx.TE_READONLY
        )
        self.packet_text_text = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        self.text_byte_0 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        self.text_byte_1 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        self.text_desc = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        self.text_byte_2 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        self.text_byte_3 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        self.text_byte_4 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        self.text_byte_5 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        self.checkbox_show_usb_log = wx.CheckBox(self, wx.ID_ANY, "Show USB Log")
        self.text_usb_log = wx.TextCtrl(
            self, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_READONLY
        )

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.on_button_start_usb, self.button_device_connect)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_mock_usb, self.checkbox_mock_usb)
        self.Bind(wx.EVT_SPINCTRL, self.spin_on_device_index, self.spin_device_index)
        self.Bind(wx.EVT_TEXT_ENTER, self.spin_on_device_index, self.spin_device_index)
        self.Bind(
            wx.EVT_SPINCTRL, self.spin_on_device_address, self.spin_device_address
        )
        self.Bind(
            wx.EVT_TEXT_ENTER, self.spin_on_device_address, self.spin_device_address
        )
        self.Bind(wx.EVT_SPINCTRL, self.spin_on_device_bus, self.spin_device_bus)
        self.Bind(wx.EVT_TEXT_ENTER, self.spin_on_device_bus, self.spin_device_bus)
        self.Bind(
            wx.EVT_SPINCTRL, self.spin_on_device_version, self.spin_device_version
        )
        self.Bind(
            wx.EVT_TEXT_ENTER, self.spin_on_device_version, self.spin_device_version
        )
        self.Bind(
            wx.EVT_BUTTON,
            self.on_button_start_controller,
            self.button_controller_control,
        )
        self.Bind(
            wx.EVT_CHECKBOX, self.on_check_show_usb_log, self.checkbox_show_usb_log
        )
        # end wxGlade
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_controller_menu, self)
        self.last_control_state = None
        self.set_widgets()

    def __set_properties(self):
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(icons8_connected_50.GetBitmap())
        self.SetIcon(_icon)
        self.SetTitle("Lhystudios-Controller")
        self.SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Segoe UI"))
        self.button_device_connect.SetBackgroundColour(wx.Colour(102, 255, 102))
        self.button_device_connect.SetFont(
            wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Segoe UI")
        )
        self.button_device_connect.SetToolTip(
            "Force connection/disconnection from the device."
        )
        self.text_connection_status.SetToolTip("Connection status")
        self.checkbox_mock_usb.SetToolTip(
            "DEBUG. Without a K40 connected continue to process things as if there was one."
        )
        self.text_device_index.SetMinSize((55, 23))
        self.spin_device_index.SetToolTip(
            "-1 match anything. 0+ match exactly that value."
        )
        self.text_device_address.SetMinSize((55, 23))
        self.spin_device_address.SetToolTip(
            "-1 match anything. 0+ match exactly that value."
        )
        self.text_device_bus.SetMinSize((55, 23))
        self.spin_device_bus.SetToolTip(
            "-1 match anything. 0+ match exactly that value."
        )
        self.text_device_version.SetMinSize((55, 23))
        self.spin_device_version.SetToolTip(
            "-1 match anything. 0+ match exactly that value."
        )
        self.button_controller_control.SetBackgroundColour(wx.Colour(102, 255, 102))
        self.button_controller_control.SetFont(
            wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Segoe UI")
        )
        self.button_controller_control.SetToolTip(
            "Change the currently performed operation."
        )
        self.text_controller_status.SetToolTip(
            "Displays the controller's current process."
        )
        self.packet_count_text.SetMinSize((77, 23))
        self.packet_count_text.SetToolTip("Total number of packets sent")
        self.rejected_packet_count_text.SetMinSize((77, 23))
        self.rejected_packet_count_text.SetToolTip("Total number of packets rejected")
        self.packet_text_text.SetToolTip("Last packet information sent")
        self.text_byte_0.SetMinSize((77, 23))
        self.text_byte_1.SetMinSize((77, 23))
        self.text_desc.SetMinSize((75, 23))
        self.text_desc.SetToolTip("The meaning of Byte 1")
        self.text_byte_2.SetMinSize((77, 23))
        self.text_byte_3.SetMinSize((77, 23))
        self.text_byte_4.SetMinSize((77, 23))
        self.text_byte_5.SetMinSize((77, 23))
        self.checkbox_show_usb_log.SetValue(1)
        self.button_device_connect.SetBitmap(icons8_disconnected_50.GetBitmap())
        self.button_controller_control.SetBitmap(icons8_play_50.GetBitmap())
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: LhystudiosController.__do_layout
        sizer_24 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_show_usb_log = wx.BoxSizer(wx.HORIZONTAL)
        packet_count = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, "Packet Info"), wx.VERTICAL
        )
        byte_data_status = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, "Byte Data Status"), wx.HORIZONTAL
        )
        byte5sizer = wx.BoxSizer(wx.VERTICAL)
        byte4sizer = wx.BoxSizer(wx.VERTICAL)
        byte3sizer = wx.BoxSizer(wx.VERTICAL)
        byte2sizer = wx.BoxSizer(wx.VERTICAL)
        byte1sizer = wx.BoxSizer(wx.VERTICAL)
        byte0sizer = wx.BoxSizer(wx.VERTICAL)
        packet_info = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, "Last Packet"), wx.HORIZONTAL
        )
        sizer_25 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_21 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, "Rejected Packets"), wx.VERTICAL
        )
        sizer_22 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, "Packet Count"), wx.VERTICAL
        )
        sizer_controller = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, "Controller"), wx.VERTICAL
        )
        sizer_usb_settings = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, "USB Settings"), wx.VERTICAL
        )
        sizer_23 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_12 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, "Chip Version"), wx.HORIZONTAL
        )
        sizer_11 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, "Device Bus:"), wx.HORIZONTAL
        )
        sizer_10 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, "Device Address:"), wx.HORIZONTAL
        )
        sizer_3 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, "Device Index:"), wx.HORIZONTAL
        )
        sizer_usb_connect = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, "USB Connection"), wx.VERTICAL
        )
        sizer_usb_connect.Add(self.button_device_connect, 0, wx.EXPAND, 0)
        sizer_usb_connect.Add(self.text_connection_status, 0, wx.EXPAND, 0)
        sizer_1.Add(sizer_usb_connect, 0, wx.EXPAND, 0)
        sizer_usb_settings.Add(self.checkbox_mock_usb, 0, 0, 0)
        sizer_3.Add(self.text_device_index, 0, 0, 0)
        sizer_3.Add(self.spin_device_index, 0, 0, 0)
        sizer_23.Add(sizer_3, 0, wx.EXPAND, 0)
        sizer_10.Add(self.text_device_address, 0, 0, 0)
        sizer_10.Add(self.spin_device_address, 0, 0, 0)
        sizer_23.Add(sizer_10, 0, wx.EXPAND, 0)
        sizer_11.Add(self.text_device_bus, 0, 0, 0)
        sizer_11.Add(self.spin_device_bus, 0, 0, 0)
        sizer_23.Add(sizer_11, 0, wx.EXPAND, 0)
        sizer_12.Add(self.text_device_version, 0, 0, 0)
        sizer_12.Add(self.spin_device_version, 0, 0, 0)
        sizer_23.Add(sizer_12, 0, wx.EXPAND, 0)
        sizer_usb_settings.Add(sizer_23, 1, wx.EXPAND, 0)
        sizer_1.Add(sizer_usb_settings, 0, wx.EXPAND, 0)
        sizer_controller.Add(self.button_controller_control, 0, wx.EXPAND, 0)
        sizer_controller.Add(self.text_controller_status, 0, wx.EXPAND, 0)
        sizer_1.Add(sizer_controller, 0, wx.EXPAND, 0)
        sizer_22.Add(self.packet_count_text, 0, wx.EXPAND, 0)
        sizer_25.Add(sizer_22, 1, wx.EXPAND, 0)
        sizer_21.Add(self.rejected_packet_count_text, 0, wx.EXPAND, 0)
        sizer_25.Add(sizer_21, 1, wx.EXPAND, 0)
        packet_count.Add(sizer_25, 1, wx.EXPAND, 0)
        packet_info.Add(self.packet_text_text, 11, wx.EXPAND, 0)
        packet_count.Add(packet_info, 0, wx.EXPAND, 0)
        byte0sizer.Add(self.text_byte_0, 0, 0, 0)
        label_1 = wx.StaticText(self, wx.ID_ANY, "Byte 0")
        byte0sizer.Add(label_1, 0, 0, 0)
        byte_data_status.Add(byte0sizer, 1, wx.EXPAND, 0)
        byte1sizer.Add(self.text_byte_1, 0, 0, 0)
        label_2 = wx.StaticText(self, wx.ID_ANY, "Byte 1")
        byte1sizer.Add(label_2, 0, 0, 0)
        byte1sizer.Add(self.text_desc, 0, 0, 0)
        byte_data_status.Add(byte1sizer, 1, wx.EXPAND, 0)
        byte2sizer.Add(self.text_byte_2, 0, 0, 0)
        label_3 = wx.StaticText(self, wx.ID_ANY, "Byte 2")
        byte2sizer.Add(label_3, 0, 0, 0)
        byte_data_status.Add(byte2sizer, 1, wx.EXPAND, 0)
        byte3sizer.Add(self.text_byte_3, 0, 0, 0)
        label_4 = wx.StaticText(self, wx.ID_ANY, "Byte 3")
        byte3sizer.Add(label_4, 0, 0, 0)
        byte_data_status.Add(byte3sizer, 1, wx.EXPAND, 0)
        byte4sizer.Add(self.text_byte_4, 0, 0, 0)
        label_5 = wx.StaticText(self, wx.ID_ANY, "Byte 4")
        byte4sizer.Add(label_5, 0, 0, 0)
        byte_data_status.Add(byte4sizer, 1, wx.EXPAND, 0)
        byte5sizer.Add(self.text_byte_5, 0, 0, 0)
        label_18 = wx.StaticText(self, wx.ID_ANY, "Byte 5")
        byte5sizer.Add(label_18, 0, 0, 0)
        byte_data_status.Add(byte5sizer, 1, wx.EXPAND, 0)
        packet_count.Add(byte_data_status, 0, wx.EXPAND, 0)
        sizer_1.Add(packet_count, 0, 0, 0)
        label_6 = wx.StaticText(self, wx.ID_ANY, "")
        sizer_show_usb_log.Add(label_6, 10, wx.EXPAND, 0)
        sizer_show_usb_log.Add(self.checkbox_show_usb_log, 0, 0, 0)
        sizer_1.Add(sizer_show_usb_log, 1, wx.EXPAND, 0)
        sizer_24.Add(sizer_1, 1, 0, 0)
        sizer_24.Add(self.text_usb_log, 2, wx.EXPAND, 0)
        self.SetSizer(sizer_24)
        self.Layout()
        # end wxGlade

    def window_open(self):
        self.context.channel("pipe/usb", buffer_size=500).watch(self.update_text)

        self.context.listen("pipe;index", self.on_update_pipe_index)
        self.context.listen("pipe;chipv", self.on_update_pipe_chipv)
        self.context.listen("pipe;bus", self.on_update_pipe_bus)
        self.context.listen("pipe;address", self.on_update_pipe_address)

        self.context.listen("pipe;status", self.update_status)
        self.context.listen("pipe;packet_text", self.update_packet_text)
        self.context.listen("pipe;usb_status", self.on_connection_status_change)
        self.context.listen("pipe;state", self.on_connection_state_change)
        self.context.listen("pipe;thread", self.on_control_state)
        self.context.listen("active", self.on_active_change)

    def window_close(self):
        self.context.channel("pipe/usb").unwatch(self.update_text)

        self.context.unlisten("pipe;index", self.on_update_pipe_index)
        self.context.unlisten("pipe;chipv", self.on_update_pipe_chipv)
        self.context.unlisten("pipe;bus", self.on_update_pipe_bus)
        self.context.unlisten("pipe;address", self.on_update_pipe_address)

        self.context.unlisten("pipe;status", self.update_status)
        self.context.unlisten("pipe;packet_text", self.update_packet_text)
        self.context.unlisten("pipe;usb_status", self.on_connection_status_change)
        self.context.unlisten("pipe;state", self.on_connection_state_change)
        self.context.unlisten("pipe;thread", self.on_control_state)
        self.context.unlisten("active", self.on_active_change)

    def on_active_change(self, origin, active):
        # self.Close()
        pass

    def update_text(self, text):
        if not wx.IsMainThread():
            wx.CallAfter(self.update_text_gui, text + "\n")
        else:
            self.update_text_gui(text + "\n")

    def update_text_gui(self, text):
        try:
            if self.text_usb_log.IsShown():
                self.text_usb_log.AppendText(text)
        except RuntimeError:
            pass

    def restore(self, *args, **kwargs):
        self.set_widgets()

    def set_widgets(self):
        self.context.setting(bool, "show_usb_log", False)
        self.context.setting(int, "usb_index", -1)
        self.context.setting(int, "usb_bus", -1)
        self.context.setting(int, "usb_address", -1)
        self.context.setting(int, "usb_version", -1)
        self.context.setting(bool, "mock", False)

        self.checkbox_show_usb_log.SetValue(self.context.show_usb_log)
        self.checkbox_mock_usb.SetValue(self.context.mock)
        self.spin_device_index.SetValue(self.context.usb_index)
        self.spin_device_bus.SetValue(self.context.usb_bus)
        self.spin_device_address.SetValue(self.context.usb_address)
        self.spin_device_version.SetValue(self.context.usb_version)

        self.on_check_show_usb_log()

    def device_execute(self, control_name):
        def menu_element(event):
            self.context.execute(control_name)

        return menu_element

    def on_controller_menu(self, event):
        gui = self
        menu = wx.Menu()
        path_scale_sub_menu = wx.Menu()
        for control_name in self.context.match("control"):
            gui.Bind(
                wx.EVT_MENU,
                self.context.execute(control_name),
                path_scale_sub_menu.Append(
                    wx.ID_ANY, list(control_name.split("/"))[-1], "", wx.ITEM_NORMAL
                ),
            )
        menu.Append(wx.ID_ANY, _("Kernel Force Event"), path_scale_sub_menu)
        if menu.MenuItemCount != 0:
            gui.PopupMenu(menu)
            menu.Destroy()

    def on_update_pipe_index(self, origin, value):
        if origin != self.context._path:
            return
        self.text_device_index.SetValue(str(value))

    def on_update_pipe_chipv(self, origin, value):
        if origin != self.context._path:
            return
        self.text_device_version.SetValue(str(value))

    def on_update_pipe_bus(self, origin, value):
        if origin != self.context._path:
            return
        self.text_device_bus.SetValue(str(value))

    def on_update_pipe_address(self, origin, value):
        if origin != self.context._path:
            return
        self.text_device_address.SetValue(str(value))

    def update_status(self, origin, status_data, code_string):
        if origin != self.context._path:
            return
        if status_data is not None:
            if isinstance(status_data, int):
                self.text_desc.SetValue(str(status_data))
                self.text_desc.SetValue(code_string)
            else:
                if len(status_data) == 6:
                    self.text_byte_0.SetValue(str(status_data[0]))
                    self.text_byte_1.SetValue(str(status_data[1]))
                    self.text_byte_2.SetValue(str(status_data[2]))
                    self.text_byte_3.SetValue(str(status_data[3]))
                    self.text_byte_4.SetValue(str(status_data[4]))
                    self.text_byte_5.SetValue(str(status_data[5]))
                    self.text_desc.SetValue(code_string)
        self.packet_count_text.SetValue(str(self.context.packet_count))
        self.rejected_packet_count_text.SetValue(str(self.context.rejected_count))

    def update_packet_text(self, origin, string_data):
        if origin != self.context._path:
            return
        if string_data is not None and len(string_data) != 0:
            self.packet_text_text.SetValue(str(string_data))

    def on_connection_status_change(self, origin, status):
        if origin != self.context._path:
            return
        self.text_connection_status.SetValue(str(status))

    def on_connection_state_change(self, origin, state):
        if origin != self.context._path:
            return
        if state == "STATE_CONNECTION_FAILED" or state == "STATE_DRIVER_NO_BACKEND":
            self.button_device_connect.SetBackgroundColour("#dfdf00")
            usb_status = self.context.last_signal("pipe;usb_status")
            if usb_status is not None:
                self.button_device_connect.SetLabel(str(usb_status[0]))
            self.button_device_connect.SetBitmap(icons8_disconnected_50.GetBitmap())
            self.button_device_connect.Enable()
        elif state == "STATE_UNINITIALIZED" or state == "STATE_USB_DISCONNECTED":
            self.button_device_connect.SetBackgroundColour("#ffff00")
            self.button_device_connect.SetLabel(_("Connect"))
            self.button_device_connect.SetBitmap(icons8_connected_50.GetBitmap())
            self.button_device_connect.Enable()
        elif state == "STATE_USB_SET_DISCONNECTING":
            self.button_device_connect.SetBackgroundColour("#ffff00")
            self.button_device_connect.SetLabel(_("Disconnecting..."))
            self.button_device_connect.SetBitmap(icons8_disconnected_50.GetBitmap())
            self.button_device_connect.Disable()
        elif state == "STATE_USB_CONNECTED" or state == "STATE_CONNECTED":
            self.button_device_connect.SetBackgroundColour("#00ff00")
            self.button_device_connect.SetLabel(_("Disconnect"))
            self.button_device_connect.SetBitmap(icons8_connected_50.GetBitmap())
            self.button_device_connect.Enable()
        elif state == "STATE_CONNECTING":
            self.button_device_connect.SetBackgroundColour("#ffff00")
            self.button_device_connect.SetLabel(_("Connecting..."))
            self.button_device_connect.SetBitmap(icons8_connected_50.GetBitmap())
            self.button_device_connect.Disable()

    def on_button_start_usb(self, event):  # wxGlade: Controller.<event_handler>
        state = self.context.last_signal("pipe;state")
        if state is not None and isinstance(state, tuple):
            state = state[0]
        if state in (
            "STATE_USB_DISCONNECTED",
            "STATE_UNINITIALIZED",
            "STATE_CONNECTION_FAILED",
            "STATE_DRIVER_MOCK",
            None,
        ):
            try:
                self.context("dev usb_connect\n")
            except ConnectionRefusedError:
                dlg = wx.MessageDialog(
                    None,
                    _("Connection Refused. See USB Log for detailed information."),
                    _("Manual Connection"),
                    wx.OK | wx.ICON_WARNING,
                )
                result = dlg.ShowModal()
                dlg.Destroy()
        elif state in ("STATE_CONNECTED", "STATE_USB_CONNECTED"):
            self.context("dev usb_disconnect\n")

    def on_control_state(self, origin, state):
        if origin != self.context._path:
            return

        if self.last_control_state == state:
            return
        self.last_control_state = state
        button = self.button_controller_control
        if self.text_controller_status is None:
            return
        value = self.context._kernel.get_text_thread_state(state)
        self.text_controller_status.SetValue(str(value))
        if state == STATE_INITIALIZE or state == STATE_END or state == STATE_IDLE:

            def f(event):
                self.context("dev start\n")
                self.context("dev hold\n")

            self.Bind(wx.EVT_BUTTON, f, button)
            button.SetBackgroundColour("#009900")
            button.SetLabel(_("Hold Controller"))
            button.SetBitmap(icons8_play_50.GetBitmap())
            button.Enable(True)
        elif state == STATE_BUSY:
            button.SetBackgroundColour("#00dd00")
            button.SetLabel(_("LOCKED"))
            button.SetBitmap(icons8_play_50.GetBitmap())
            button.Enable(False)
        elif state == STATE_WAIT:

            def f(event):
                self.context("dev continue\n")

            self.Bind(wx.EVT_BUTTON, f, button)
            button.SetBackgroundColour("#dddd00")
            button.SetLabel(_("Force Continue"))
            button.SetBitmap(icons8_laser_beam_hazard_50.GetBitmap())
            button.Enable(True)
        elif state == STATE_PAUSE:

            def f(event):
                self.context("dev resume\n")

            self.Bind(wx.EVT_BUTTON, f, button)
            button.SetBackgroundColour("#00dd00")
            button.SetLabel(_("Resume Controller"))
            button.SetBitmap(icons8_play_50.GetBitmap())
            button.Enable(True)
        elif state == STATE_ACTIVE:

            def f(event):
                self.context("dev hold\n")

            self.Bind(wx.EVT_BUTTON, f, button)
            button.SetBackgroundColour("#00ff00")
            button.SetLabel(_("Pause Controller"))
            button.SetBitmap(icons8_pause_50.GetBitmap())
            button.Enable(True)
        elif state == STATE_TERMINATE:

            def f(event):
                self.context("dev abort\n")

            self.Bind(wx.EVT_BUTTON, f, button)
            button.SetBackgroundColour("#00ffff")
            button.SetLabel(_("Manual Reset"))
            button.SetBitmap(icons8_emergency_stop_button_50.GetBitmap())
            button.Enable(True)

    def spin_on_device_index(self, event):  # wxGlade: Preferences.<event_handler>
        self.context.usb_index = int(self.spin_device_index.GetValue())

    def spin_on_device_address(self, event):  # wxGlade: Preferences.<event_handler>
        self.context.usb_address = int(self.spin_device_address.GetValue())

    def spin_on_device_bus(self, event):  # wxGlade: Preferences.<event_handler>
        self.context.usb_bus = int(self.spin_device_bus.GetValue())

    def spin_on_device_version(self, event):  # wxGlade: Preferences.<event_handler>
        self.context.usb_version = int(self.spin_device_version.GetValue())

    def on_check_mock_usb(self, event):  # wxGlade: Preferences.<event_handler>
        self.context.mock = self.checkbox_mock_usb.GetValue()

    def on_button_start_controller(
        self, event
    ):  # wxGlade: LhystudiosController.<event_handler>
        print("Event handler 'on_button_start_controller' not implemented!")
        event.Skip()

    def on_check_show_usb_log(
        self, event=None
    ):  # wxGlade: LhystudiosController.<event_handler>
        on = self.checkbox_show_usb_log.GetValue()
        self.text_usb_log.Show(on)
        self.context.show_usb_log = bool(on)
        if on:
            self.SetSize((_advanced_width, _default_height))
        else:
            self.SetSize((_simple_width, _default_height))

    def on_menu_usb_reset(self, event):  # wxGlade: LhystudiosController.<event_handler>
        print("Event handler 'on_menu_usb_reset' not implemented!")
        event.Skip()

    def on_menu_usb_release(
        self, event
    ):  # wxGlade: LhystudiosController.<event_handler>
        print("Event handler 'on_menu_usb_release' not implemented!")
        event.Skip()

    def on_menu_pause(self, event):  # wxGlade: LhystudiosController.<event_handler>
        try:
            self.context("dev pause\n")
        except AttributeError:
            pass

    def on_menu_stop(self, event):  # wxGlade: LhystudiosController.<event_handler>
        try:
            self.context("dev estop\n")
        except AttributeError:
            pass

    def on_menu_bufferview(
        self, event
    ):  # wxGlade: LhystudiosController.<event_handler>
        self.context("window open BufferView\n")
