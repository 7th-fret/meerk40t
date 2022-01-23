import wx

from .icons import icons8_comments_50
from .mwindow import MWindow
from .panes.notespanel import NotePanel

_ = wx.GetTranslation


class ConsoleProperty(MWindow):
    def __init__(self, *args, node=None, **kwds):
        super().__init__(730, 621, *args, **kwds)

        self.panel = ConsolePropertiesPanel(
            self, wx.ID_ANY, context=self.context, node=node)
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(icons8_comments_50.GetBitmap())
        self.SetIcon(_icon)
        self.SetTitle(_("Console Properties"))
        self.Children[0].SetFocus()

    # def window_open(self):
    #     self.context.close(self.name)
    #     self.panel.initialize()

    # def window_close(self):
    #     self.panel.finalize()


class ConsolePropertiesPanel(wx.Panel):
    def __init__(self, *args, context=None, node=None, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.context = context

        self.console_operation = node
        self.command_name = wx.TextCtrl(self, wx.ID_ANY, "")
        self.command_text = wx.TextCtrl(
            self,
            wx.ID_ANY,
            "Command text",
            style=wx.TE_BESTWRAP | wx.TE_MULTILINE | wx.TE_WORDWRAP
        )

        self.__set_properties()
        self.__do_layout()

        if node:
            self.command_name.SetValue(node.name)
            self.command_text.SetValue(node.command)

        self.Bind(wx.EVT_TEXT, self.on_change_name, self.command_name)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_change_name, self.command_name)
        self.Bind(wx.EVT_TEXT, self.on_change_command, self.command_text)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_change_command, self.command_text)
        # end wxGlade

    def __set_properties(self):
        pass

    def __do_layout(self):
        # begin wxGlade: NotePanel.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.command_name, 0, wx.EXPAND, 0)
        sizer_1.Add(self.command_text, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

    def on_change_name(self, event=None):
        self.console_operation.name = self.command_name.GetValue()
        self.console_operation.label = (
            self.console_operation.name or self.console_operation.command)
        self.context.signal("element_property_update", self.console_operation)

    def on_change_command(self, event=None):
        self.console_operation.command = self.command_text.GetValue()
        self.console_operation.label = (
            self.console_operation.name or self.console_operation.command)
        self.context.signal("element_property_update", self.console_operation)
