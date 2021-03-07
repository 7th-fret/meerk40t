#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.3 on Sat Feb  1 06:42:01 2020
#

import wx

from ..kernel import STATE_UNKNOWN, Module
from .icons import (icons8_administrative_tools_50, icons8_manager_50,
                    icons8_plus_50, icons8_trash_50)

_ = wx.GetTranslation


class DeviceManager(wx.Frame, Module):
    def __init__(self, context, path, parent, *args, **kwds):
        # begin wxGlade: DeviceManager.__init__
        if parent is None:
            wx.Frame.__init__(self, parent, -1, "", style=wx.DEFAULT_FRAME_STYLE)
        else:
            wx.Frame.__init__(
                self,
                parent,
                -1,
                "",
                style=wx.DEFAULT_FRAME_STYLE
                | wx.FRAME_FLOAT_ON_PARENT
                | wx.TAB_TRAVERSAL,
            )
        Module.__init__(self, context, path)
        self.SetSize((707, 337))
        self.devices_list = wx.ListCtrl(
            self, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES
        )
        self.new_device_button = wx.BitmapButton(
            self, wx.ID_ANY, icons8_plus_50.GetBitmap()
        )
        self.remove_device_button = wx.BitmapButton(
            self, wx.ID_ANY, icons8_trash_50.GetBitmap()
        )
        self.device_properties_button = wx.BitmapButton(
            self, wx.ID_ANY, icons8_administrative_tools_50.GetBitmap()
        )

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.on_list_drag, self.devices_list)
        self.Bind(
            wx.EVT_LIST_ITEM_ACTIVATED, self.on_list_item_activated, self.devices_list
        )
        self.Bind(
            wx.EVT_LIST_ITEM_RIGHT_CLICK, self.on_list_right_click, self.devices_list
        )
        self.Bind(wx.EVT_BUTTON, self.on_button_new, self.new_device_button)
        self.Bind(wx.EVT_BUTTON, self.on_button_remove, self.remove_device_button)
        self.Bind(
            wx.EVT_BUTTON, self.on_button_properties, self.device_properties_button
        )
        # end wxGlade

        self.Bind(wx.EVT_CLOSE, self.on_close, self)

        self.context.close(self.name)
        self.Show()
        self.context.setting(str, "list_devices", "")
        self.refresh_device_list()
        # OSX Window close
        if parent is not None:
            parent.accelerator_table(self)

    def on_close(self, event):
        item = self.devices_list.GetFirstSelected()
        if item != -1:
            uid = self.devices_list.GetItem(item).Text
            self.context.device_primary = uid

        if self.state == 5:
            event.Veto()
        else:
            self.state = 5
            self.context.close(self.name)
            event.Skip()  # Call destroy as regular.

    def finalize(self, *args, **kwargs):
        try:
            self.Close()
        except RuntimeError:
            pass

    def __set_properties(self):
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(icons8_manager_50.GetBitmap())
        self.SetIcon(_icon)
        # begin wxGlade: DeviceManager.__set_properties
        self.SetTitle("Device Manager")
        self.devices_list.SetFont(
            wx.Font(
                13,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                0,
                "Segoe UI",
            )
        )
        self.devices_list.AppendColumn(_("Id"), format=wx.LIST_FORMAT_LEFT, width=72)
        self.devices_list.AppendColumn(
            _("Driver"), format=wx.LIST_FORMAT_LEFT, width=119
        )
        self.devices_list.AppendColumn(
            _("State"), format=wx.LIST_FORMAT_LEFT, width=127
        )
        self.devices_list.AppendColumn(
            _("Location"), format=wx.LIST_FORMAT_LEFT, width=258
        )
        self.devices_list.AppendColumn(_("Boot"), format=wx.LIST_FORMAT_LEFT, width=51)
        self.new_device_button.SetToolTip(_("Add a new device"))
        self.new_device_button.SetSize(self.new_device_button.GetBestSize())
        self.remove_device_button.SetToolTip(_("Remove selected device"))
        self.remove_device_button.SetSize(self.remove_device_button.GetBestSize())
        self.device_properties_button.SetToolTip(_("View Device Properties"))
        self.device_properties_button.SetSize(
            self.device_properties_button.GetBestSize()
        )
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: DeviceManager.__do_layout
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.devices_list, 1, wx.EXPAND, 0)
        button_sizer.Add(self.new_device_button, 0, 0, 0)
        button_sizer.Add(self.remove_device_button, 0, 0, 0)
        button_sizer.Add(self.device_properties_button, 0, 0, 0)
        main_sizer.Add(button_sizer, 0, wx.EXPAND, 0)
        self.SetSizer(main_sizer)
        self.Layout()
        # end wxGlade

    def refresh_device_list(self):
        self.devices_list.DeleteAllItems()
        i = 0
        for device in self.context.derivable():
            try:
                d = int(device)
            except ValueError:
                continue
            settings = self.context.derive(device)
            device_name = settings.setting(str, "device_name", "Lhystudios")
            autoboot = settings.setting(bool, "autoboot", True)
            location_name = settings.setting(str, "location_name", "Unknown")
            try:
                device_obj = self.context._kernel.contexts[device]
                state = device_obj._state
            except KeyError:
                state = -1
            m = self.devices_list.InsertItem(i, str(d))
            if m != -1:
                self.devices_list.SetItem(m, 1, str(device_name))
                self.devices_list.SetItem(m, 2, str(state))
                self.devices_list.SetItem(m, 3, str(location_name))
                self.devices_list.SetItem(m, 4, str(autoboot))
            i += 1

    def on_list_drag(self, event):  # wxGlade: DeviceManager.<event_handler>
        pass

    def on_list_right_click(self, event):  # wxGlade: DeviceManager.<event_handler>
        uid = event.GetLabel()
        # If the device is booted change the autoboot settings.
        context_obj = self.context.get_context("/%s" % uid)
        context_obj.setting(bool, "autoboot", True)
        context_obj.autoboot = not context_obj.autoboot
        context_obj._kernel.write_persistent(
            context_obj.abs_path("autoboot"), context_obj.autoboot
        )
        self.refresh_device_list()

    def on_list_item_activated(self, event):  # wxGlade: DeviceManager.<event_handler>
        uid = event.GetLabel()
        context = self.context.get_context("/%s" % uid)
        context_name = context.setting(str, "device_name", "Lhystudios")
        if context._state == STATE_UNKNOWN:
            context.boot()
        else:
            dlg = wx.MessageDialog(
                None,
                _("That device already booted."),
                _("Cannot Boot Selected Device"),
                wx.OK | wx.ICON_WARNING,
            )
            result = dlg.ShowModal()
            dlg.Destroy()

    def on_button_new(self, event):  # wxGlade: DeviceManager.<event_handler>
        names = [name[7:] for name in self.context._kernel.match("device")]
        dlg = wx.SingleChoiceDialog(
            None, _("What type of device is being added?"), _("Device Type"), names
        )
        dlg.SetSelection(0)
        if dlg.ShowModal() == wx.ID_OK:
            device_type = dlg.GetSelection()
            device_type = names[device_type]
        else:
            dlg.Destroy()
            return
        dlg.Destroy()
        device_uid = 0
        devices = list(self.context.derivable())
        while device_uid <= 100:
            device_uid += 1
            if str(device_uid) not in devices:
                break
        settings = self.context.get_context("%d" % device_uid)
        settings.setting(str, "device_name", device_type)
        settings.setting(bool, "autoboot", True)
        settings.flush()
        self.refresh_device_list()

    def on_button_remove(self, event):  # wxGlade: DeviceManager.<event_handler>
        item = self.devices_list.GetFirstSelected()
        uid = self.devices_list.GetItem(item).Text
        settings = self.context.derive(str(uid))
        settings._kernel.clear_persistent(settings._path)
        try:
            device = self.context._kernel.contexts[uid]
            del self.context._kernel.contexts[uid]
            device.opened["window/MeerK40t"].Close()
        except (KeyError, AttributeError):
            pass

        self.refresh_device_list()

    def on_button_properties(self, event):  # wxGlade: DeviceManager.<event_handler>
        item = self.devices_list.GetFirstSelected()
        if item == -1:
            return
        uid = self.devices_list.GetItem(item).Text
        context = self.context.get_context("/%s" % uid)
        context.open("window/Preferences", self)
