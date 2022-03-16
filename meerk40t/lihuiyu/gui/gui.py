from meerk40t.kernel import signal_listener


def plugin(service, lifecycle):
    if lifecycle == "invalidate":
        return not service.has_feature("wx")

    if lifecycle == "service":
        return "provider/device/lhystudios"

    if lifecycle == "assigned":
        service("window toggle Configuration\n")

    if lifecycle == "added":
        from meerk40t.gui.icons import (
            icons8_computer_support_50,
            icons8_connected_50,
            icons8_emergency_stop_button_50,
            icons8_pause_50,
        )
        from meerk40t.lihuiyu.gui.lhyoperationproperties import LhyAdvancedPanel
        from meerk40t.lihuiyu.gui.lhystudiosaccel import LhystudiosAccelerationChart
        from meerk40t.lihuiyu.gui.lhystudioscontrollergui import LhystudiosControllerGui
        from meerk40t.lihuiyu.gui.lhystudiosdrivergui import LhystudiosDriverGui
        from meerk40t.lihuiyu.gui.tcpcontroller import TCPController

        service.register("window/Controller", LhystudiosControllerGui)
        service.register("window/Configuration", LhystudiosDriverGui)
        service.register("window/AccelerationChart", LhystudiosAccelerationChart)
        service.register("window/Network-Controller", TCPController)
        service.register("operationproperty/Lihuiyu", LhyAdvancedPanel)
        _ = service.kernel.translation

        def controller_click(i=None):
            if service.networked:
                service("window toggle Network-Controller\n")
            else:
                service("window toggle Controller\n")

        service.register(
            "button/control/Controller",
            {
                "label": _("Controller"),
                "icon": icons8_connected_50,
                "tip": _("Opens Controller Window"),
                "action": controller_click,
                "alt-action": (
                    (
                        _("Opens USB-Controller"),
                        lambda e: service("window toggle Controller\n"),
                    ),
                    (
                        _("Opens Network-Controller"),
                        lambda e: service("window toggle Network-Controller\n"),
                    ),
                ),
            },
        )
        service.register(
            "button/config/Configuration",
            {
                "label": _("Config"),
                "icon": icons8_computer_support_50,
                "tip": _("Opens device-specific configuration window"),
                "action": lambda v: service("window toggle Configuration\n"),
            },
        )
        service.register(
            "button/control/Pause",
            {
                "label": _("Pause"),
                "icon": icons8_pause_50,
                "tip": _("Pause the laser"),
                "action": lambda v: service("pause\n"),
            },
        )

        service.register(
            "button/control/Stop",
            {
                "label": _("Stop"),
                "icon": icons8_emergency_stop_button_50,
                "tip": _("Emergency stop the laser"),
                "action": lambda v: service("estop\n"),
            },
        )
        service.add_service_delegate(LihuiyuGui(service))


class LihuiyuGui:
    def __init__(self, context):
        self.context = context

    @signal_listener("controller")
    def on_controller(self, origin, original_origin, *args):
        self.context("window open Controller\n")
