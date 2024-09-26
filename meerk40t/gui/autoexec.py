"""
This module offers the opportunity to define a couple of commands that will automatically be executed on a (main) file load
"""
import wx
from wx import aui

from .icons import STD_ICON_SIZE, icons8_comments
from .mwindow import MWindow
from .wxutils import wxCheckBox

_ = wx.GetTranslation


def register_panel(window, context):
    panel = AutoExecPanel(window, wx.ID_ANY, context=context, pane=True)
    pane = (
        aui.AuiPaneInfo()
        .Float()
        .MinSize(100, 100)
        .FloatingSize(170, 230)
        .MaxSize(500, 500)
        .Caption(_("Notes"))
        .CaptionVisible(not context.pane_lock)
        .Name("notes")
        .Hide()
    )
    pane.dock_proportion = 100
    pane.control = panel
    pane.submenu = "_50_" + _("Tools")

    window.on_pane_create(pane)
    context.register("pane/autoexec", pane)


class AutoExecPanel(wx.Panel):
    def __init__(self, *args, context=None, pane=False, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.context = context
        self.SetHelpText("autoexec")
        self.pane = pane
        self.text_autoexec = wx.TextCtrl(
            self,
            wx.ID_ANY,
            "",
            style=wx.TE_BESTWRAP | wx.TE_MULTILINE | wx.TE_WORDWRAP | wx.TE_RICH,
        )
        self.check_auto_startup = wxCheckBox(self, wx.ID_ANY, _("Execute on load"))
        self.button_execute = wx.Button(self, wx.ID_ANY, _("Execute commands"))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TEXT, self.on_text_autoexec, self.text_autoexec)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_text_autoexec, self.text_autoexec)
        self.Bind(wx.EVT_BUTTON, self.on_execute, self.button_execute)
        self.Bind(wx.EVT_CHECKBOX, self.on_check, self.check_auto_startup)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_context_menu, self)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_context_menu, self)

    def on_execute(self, event):
        self.context(".file_startup\n")

    def on_check(self, event):
        self.context.elements.auto_startup = self.check_auto_startup.GetValue()

    def __set_properties(self):
        self.text_autoexec.SetToolTip(
            _("List of commands that will be immediately executed after the file has been loaded") + "\n" +
            _("While this might be useful to immediately change a device, it can also be dangerous if you e.g. chose to start a burn.") + "\n" +
            _("Use with care, please!") + "\n" +
            _("Tip 1: click on the form background to get a list of useful commands...") + "\n" +
            _("Tip 2: you can deactivate any command by starting the line with a '#'")
        )
        self.check_auto_startup.SetToolTip(_("The autoexec content of any file (not just this one) will be executed/ignored if this option is active/deactive"))
        self.button_execute.SetToolTip(_("Execute the commands"))

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.text_autoexec, 1, wx.EXPAND, 0)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.check_auto_startup, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_2.AddStretchSpacer(1)
        sizer_2.Add(self.button_execute, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_1.Add(sizer_2, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()

    def pane_show(self, *args):
        text = self.context.elements.autoexec
        if text is None:
            text = ""
        self.text_autoexec.SetValue(text)
        self.check_auto_startup.SetValue(self.context.elements.auto_startup)
        self.context.listen("autoexec", self.on_autoexec_listen)

    def pane_hide(self):
        self.context.unlisten("autoexec", self.on_autoexec_listen)

    def on_context_menu(self, event):
        def _clear_all(event):
            self.text_autoexec.SetValue("")

        def _execute(command):
            def handler(event):
                t = self.text_autoexec.GetValue()
                if t:
                    t+= "\n"
                t += command
                self.text_autoexec.SetValue(t)
                self.text_autoexec.SetInsertionPointEnd()

            return handler

        useful = [
            ("clear", _("Clear console")),
            ("planz clear copy preprocess validate blob preopt optimize", _("Start simulation")),
            ("burn", _("Burn content on current device")),
        ]
        kernel = self.context.kernel
        dev_infos = list(kernel.find("dev_info"))
        dev_infos.sort(key=lambda e: e[0].get("priority", 0), reverse=True)
        for device in kernel.services("device"):
            label = device.label
            msg = label
            type_info = getattr(device, "name", device.path)
            family_default = ""
            for obj, name, sname in dev_infos:
                if device.registered_path == obj.get("provider", ""):
                    if "choices" in obj:
                        for prop in obj["choices"]:
                            if (
                                "attr" in prop
                                and "default" in prop
                                and prop["attr"] == "source"
                            ):
                                family_default = prop["default"]
                                break
                if family_default:
                    break

            family_info = device.setting(str, "source", family_default)
            if family_info:
                family_info = family_info.capitalize()

            msg += f" - {type_info} - {family_info}"

            useful.append( (f"device activate {label}", _("Activate {info}").format(info=msg)))

        menu = wx.Menu()
        item = wx.MenuItem(menu, wx.ID_ANY, _("Clear all"))
        menu.Append(item)
        self.Bind(wx.EVT_MENU, _clear_all, item)
        menu.AppendSeparator()
        for command, info in useful:
            item = wx.MenuItem(menu, wx.ID_ANY, info)
            menu.Append(item)
            self.Bind(wx.EVT_MENU, _execute(command), item)
        self.PopupMenu(menu)
        menu.Destroy()

    def on_text_autoexec(self, event=None):
        if len(self.text_autoexec.GetValue()) == 0:
            self.context.elements.autoexec = None
            self.button_execute.Enable(False)
        else:
            self.context.elements.autoexec = self.text_autoexec.GetValue()
            self.button_execute.Enable(True)
        self.context.elements.signal("autoexec", self)

    def on_autoexec_listen(self, origin, source):
        if source is self:
            return
        commands = self.context.elements.autoexec
        if self.context.elements.autoexec is None:
            commands = ""
        if self.text_autoexec.GetValue() != commands:
            self.text_autoexec.SetValue(commands)


class AutoExec(MWindow):
    def __init__(self, *args, **kwds):
        super().__init__(450, 350, *args, **kwds)

        self.panel = AutoExecPanel(self, wx.ID_ANY, context=self.context)
        self.sizer.Add(self.panel, 1, wx.EXPAND, 0)
        self.add_module_delegate(self.panel)
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(icons8_comments.GetBitmap())
        self.SetIcon(_icon)
        self.SetTitle(_("File startup commands"))
        self.Children[0].SetFocus()
        self.restore_aspect(honor_initial_values=True)

    @staticmethod
    def sub_register(kernel):
        kernel.register("wxpane/AutoExec", register_panel)
        kernel.register(
            "button/project/Startup",
            {
                "label": _("Startup"),
                "icon": icons8_comments,
                "tip": _("Edit file startup commands"),
                "help": "autoexec",
                "action": lambda v: kernel.console("window toggle AutoExec\n"),
                "size": STD_ICON_SIZE,
            },
        )

    def window_open(self):
        self.context.close(self.name)
        self.panel.pane_show()

    def window_close(self):
        self.panel.pane_hide()
