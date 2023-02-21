"""
Newly Device
"""
import struct

from meerk40t.core.laserjob import LaserJob
from meerk40t.core.spoolers import Spooler
from meerk40t.core.units import ViewPort, UNITS_PER_MM, UNITS_PER_MIL
from meerk40t.kernel import CommandSyntaxError, Service, signal_listener
from meerk40t.newly.driver import NewlyDriver


class NewlyDevice(Service, ViewPort):
    """
    Newly Device
    """

    def __init__(self, kernel, path, *args, **kwargs):
        Service.__init__(self, kernel, path)
        self.name = "newly"
        self.extension = "nly"
        self.job = None

        _ = kernel.translation
        choices = [
            {
                "attr": "label",
                "object": self,
                "default": "newly-device",
                "type": str,
                "label": _("Label"),
                "tip": _("What is this device called."),
                "section": "_00_General",
                "priority": "10",
            },
            {
                "attr": "bedwidth",
                "object": self,
                "default": "310mm",
                "type": str,
                "label": _("Width"),
                "tip": _("Width of the laser bed."),
                "section": "_00_General",
                "priority": "20",
                "nonzero": True,
            },
            {
                "attr": "bedheight",
                "object": self,
                "default": "210mm",
                "type": str,
                "label": _("Height"),
                "tip": _("Height of the laser bed."),
                "section": "_00_General",
                "priority": "20",
                "nonzero": True,
            },
            {
                "attr": "home_bottom",
                "object": self,
                "default": False,
                "type": bool,
                "label": _("Home Bottom"),
                "tip": _("Indicates the device Home is on the bottom"),
                "subsection": "_50_Home position",
                "signals": "bedsize",
            },
            {
                "attr": "home_right",
                "object": self,
                "default": False,
                "type": bool,
                "label": _("Home Right"),
                "tip": _("Indicates the device Home is at the right side"),
                "subsection": "_50_Home position",
                "signals": "bedsize",
            },
            {
                "attr": "flip_x",
                "object": self,
                "default": False,
                "type": bool,
                "label": _("Flip X"),
                "tip": _("Flip the X axis for the device"),
                "section": "_10_Parameters",
                "subsection": "_10_Axis corrections",
                "signals": "bedsize",
            },
            {
                "attr": "flip_y",
                "object": self,
                "default": False,
                "type": bool,
                "label": _("Flip Y"),
                "tip": _("Flip the Y axis for the device"),
                "section": "_10_Parameters",
                "subsection": "_10_Axis corrections",
                "signals": "bedsize",
            },
            {
                "attr": "swap_xy",
                "object": self,
                "default": False,
                "type": bool,
                "label": _("Swap XY"),
                "tip": _("Swap the X and Y axis for the device"),
                "section": "_10_Parameters",
                "subsection": "_10_Axis corrections",
            },
            {
                "attr": "interpolate",
                "object": self,
                "default": 50,
                "type": int,
                "label": _("Curve Interpolation"),
                "section": "_10_Parameters",
                "tip": _("Number of curve interpolation points"),
            },
            {
                "attr": "mock",
                "object": self,
                "default": False,
                "type": bool,
                "label": _("Run mock-usb backend"),
                "tip": _(
                    "This starts connects to fake software laser rather than real one for debugging."
                ),
                "section": "_00_General",
                "priority": "30",
            },
            {
                "attr": "machine_index",
                "object": self,
                "default": 0,
                "type": int,
                "label": _("Machine index to select"),
                "tip": _(
                    "Which machine should we connect to? -- Leave at 0 if you have 1 machine."
                ),
                "section": "_00_General",
            },
            {
                "attr": "use_relative",
                "object": self,
                "default": True,
                "type": bool,
                "label": _("Use Relative Coordinates"),
                "tip": _(
                    "Should we use relative or absolute coordinates for the device."
                ),
            },
        ]
        self.register_choices("newly", choices)

        choices = [
            {
                "attr": "h_dpi",
                "object": self,
                "default": 1000,
                "type": float,
                "label": _("Horizontal DPI"),
                "tip": _("The Dots-Per-Inch across the X-axis"),
                "section": "_10_Parameters",
                "subsection": "_20_Axis DPI",
            },
            {
                "attr": "v_dpi",
                "object": self,
                "default": 1000,
                "type": float,
                "label": _("Vertical DPI"),
                "tip": _("The Dots-Per-Inch across the Y-axis"),
                "section": "_10_Parameters",
                "subsection": "_20_Axis DPI",
            },
            {
                "attr": "h_backlash",
                "object": self,
                "default": 0,
                "type": float,
                "label": _("Horizontal Backlash"),
                "tip": _("Backlash amount for the laser."),
                "trailer": "mm",
                "section": "_10_Parameters",
                "subsection": "_30_Backlash",
            },
            {
                "attr": "v_backlash",
                "object": self,
                "default": 0,
                "type": float,
                "label": _("Vertical Backlash"),
                "tip": _("Backlash amount for the laser."),
                "trailer": "mm",
                "section": "_10_Parameters",
                "subsection": "_30_Backlash",
            },
            {
                "attr": "max_power",
                "object": self,
                "default": 20.0,
                "type": float,
                "label": _("Max Power"),
                "trailer": "%",
                "tip": _("Maximum laser power, all other power will be a scale of this amount"),
                "section": "_10_Parameters",
                "subsection": "_40_Power",
            },
            {
                "attr": "pwm_enabled",
                "object": self,
                "default": False,
                "type": bool,
                "label": _("PWM Power"),
                "tip": _("Power Width Modulation enabled for device."),
                "section": "_10_Parameters",
                "subsection": "_40_Power",
            },
            {
                "attr": "pwm_frequency",
                "object": self,
                "default": 2,
                "type": int,
                "style": "combo",
                "choices": [
                    2,
                ],
                "conditional": (self, "pwm_enabled"),
                "label": _("PWM Frequency"),
                "trailer": "khz",
                "tip": _("Set the frequency of the PWM, how often the pulse width cycles"),
                "section": "_10_Parameters",
                "subsection": "_40_Power",
            },
        ]
        self.register_choices("newly-specific", choices)

        choices = [
            {
                "attr": "default_power",
                "object": self,
                "default": 1000.0,
                "type": float,
                "label": _("Laser Power"),
                "trailer": "/1000",
                "tip": _("How what power level do we cut at?"),
            },
            {
                "attr": "default_speed",
                "object": self,
                "default": 15.0,
                "type": float,
                "trailer": "mm/s",
                "label": _("Cut Speed"),
                "tip": _("How fast do we cut?"),
            },
            {
                "attr": "default_raster_speed",
                "object": self,
                "default": 200.0,
                "type": float,
                "trailer": "mm/s",
                "label": _("Raster Speed"),
                "tip": _("How fast do we raster?"),
            },
            {
                "attr": "default_acceleration",
                "object": self,
                "default": 24.0,
                "type": float,
                "trailer": "acc",
                "label": _("Acceleration"),
                "tip": _("Acceleration value"),
            },
        ]
        self.register_choices("newly-global", choices)

        self.state = 0

        ViewPort.__init__(
            self,
            self.bedwidth,
            self.bedheight,
            native_scale_x=UNITS_PER_MIL,
            native_scale_y=UNITS_PER_MIL,
            origin_x=1.0 if self.home_right else 0.0,
            origin_y=1.0 if self.home_bottom else 0.0,
            flip_x=self.flip_x,
            flip_y=self.flip_y,
            swap_xy=self.swap_xy,
        )
        self.spooler = Spooler(self)
        self.driver = NewlyDriver(self)
        self.spooler.driver = self.driver

        self.add_service_delegate(self.spooler)

        self.viewbuffer = ""

        @self.console_command(
            "estop",
            help=_("stops the current job, deletes the spooler"),
            input_type=(None),
        )
        def estop(command, channel, _, data=None, remainder=None, **kwgs):
            channel("Stopping Job")
            if self.job is not None:
                self.job.stop()
            self.spooler.clear_queue()
            self.driver.reset()

        @self.console_command(
            "pause",
            help=_("Pauses the currently running job"),
        )
        def pause(command, channel, _, data=None, remainder=None, **kwgs):
            if self.driver.paused:
                channel("Resuming current job")
            else:
                channel("Pausing current job")
            self.driver.pause()
            self.signal("pause")

        @self.console_command(
            "resume",
            help=_("Resume the currently running job"),
        )
        def resume(command, channel, _, data=None, remainder=None, **kwgs):
            channel("Resume the current job")
            self.driver.resume()
            self.signal("pause")

        @self.console_command(
            "usb_connect",
            help=_("connect usb"),
        )
        def usb_connect(command, channel, _, data=None, remainder=None, **kwgs):
            self.spooler.command("connect", priority=1)

        @self.console_command(
            "usb_disconnect",
            help=_("connect usb"),
        )
        def usb_disconnect(command, channel, _, data=None, remainder=None, **kwgs):
            self.spooler.command("disconnect", priority=1)

        @self.console_command("usb_abort", help=_("Stops USB retries"))
        def usb_abort(command, channel, _, **kwargs):
            self.spooler.command("abort_retry", priority=1)

        @self.console_argument("filename", type=str)
        @self.console_command("save_job", help=_("save job export"), input_type="plan")
        def newly_save(channel, _, filename, data=None, **kwargs):
            if filename is None:
                raise CommandSyntaxError
            try:
                with open(filename, "w") as f:
                    driver = NewlyDriver(self, force_mock=True)
                    job = LaserJob(filename, list(data.plan), driver=driver)

                    def write(index, cmd):
                        f.write(cmd)

                    driver.connection.connect_if_needed()
                    driver.connection.connection.write = write
                    job.execute()

            except (PermissionError, OSError):
                channel(_("Could not save: {filename}").format(filename=filename))

        @self.console_command(
            "viewport_update",
            hidden=True,
            help=_("Update newly flips for movement"),
        )
        def codes_update(**kwargs):
            self.realize()

    @signal_listener("flip_x")
    @signal_listener("flip_y")
    @signal_listener("swap_xy")
    def realize(self, origin=None, *args):
        self.width = self.bedwidth
        self.height = self.bedheight
        super().realize()

    @property
    def current(self):
        """
        @return: the location in nm for the current known x value.
        """
        return self.device_to_scene_position(
            self.driver.native_x,
            self.driver.native_y,
        )

    @property
    def native(self):
        """
        @return: the location in device native units for the current known position.
        """
        return self.driver.native_x, self.driver.native_y

    @property
    def calibration_file(self):
        return None
