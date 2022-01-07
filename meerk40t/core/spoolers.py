from threading import Lock

from meerk40t.svgelements import Length

from ..device.lasercommandconstants import *


def plugin(kernel, lifecycle):
    if lifecycle == "register":
        _ = kernel.translation

        @kernel.console_argument("op", type=str, help=_("unlock, origin, home, etc"))
        @kernel.console_command(
            "send",
            help=_("send a plan-command to the spooler"),
            input_type="spooler",
            output_type="spooler",
        )
        def spooler_send(
            command, channel, _, data_type=None, op=None, data=None, **kwgs
        ):
            spooler = data
            if op is None:
                raise SyntaxError
            try:
                for plan_command, command_name, suffix in kernel.find("plan", op):
                    spooler.job(plan_command)
                    return data_type, spooler
            except (KeyError, IndexError):
                pass
            channel(_("No plan command found."))
            return data_type, spooler

        @kernel.console_command(
            "list",
            help=_("spool<?> list"),
            input_type="spooler",
            output_type="spooler",
        )
        def spooler_list(command, channel, _, data_type=None, data=None, **kwgs):
            spooler = data
            channel(_("----------"))
            channel(_("Spoolers:"))
            for d, d_name in enumerate(kernel.match("device", suffix=True)):
                channel("%d: %s" % (d, d_name))
            channel(_("----------"))
            channel(_("Spooler on device %s:" % str(kernel.device.label)))
            for s, op_name in enumerate(spooler.queue):
                channel("%d: %s" % (s, op_name))
            channel(_("----------"))
            return data_type, spooler

        @kernel.console_command(
            "clear",
            help=_("spooler<?> clear"),
            input_type="spooler",
            output_type="spooler",
        )
        def spooler_clear(command, channel, _, data_type=None, data=None, **kwgs):
            spooler = data
            spooler.clear_queue()
            return data_type, spooler

        def execute_absolute_position(position_x, position_y):
            x_pos = Length(position_x).value(
                ppi=1000.0, relative_length=kernel.device.bedwidth
            )
            y_pos = Length(position_y).value(
                ppi=1000.0, relative_length=kernel.device.bedheight
            )

            def move():
                yield COMMAND_SET_ABSOLUTE
                yield COMMAND_MODE_RAPID
                yield COMMAND_MOVE, int(x_pos), int(y_pos)

            return move

        def execute_relative_position(position_x, position_y):
            x_pos = Length(position_x).value(
                ppi=1000.0, relative_length=kernel.device.bedwidth
            )
            y_pos = Length(position_y).value(
                ppi=1000.0, relative_length=kernel.device.bedheight
            )

            def move():
                yield COMMAND_SET_INCREMENTAL
                yield COMMAND_MODE_RAPID
                yield COMMAND_MOVE, int(x_pos), int(y_pos)
                yield COMMAND_SET_ABSOLUTE

            return move

        @kernel.console_command(
            "+laser",
            hidden=True,
            input_type=("spooler", None),
            output_type="spooler",
            help=_("turn laser on in place"),
        )
        def plus_laser(data, **kwgs):
            if data is None:
                data = kernel.device.spooler
            spooler = data
            spooler.job(COMMAND_LASER_ON)
            return "spooler", spooler

        @kernel.console_command(
            "-laser",
            hidden=True,
            input_type=("spooler", None),
            output_type="spooler",
            help=_("turn laser off in place"),
        )
        def minus_laser(data, **kwgs):
            if data is None:
                data = kernel.device.spooler
            spooler = data
            spooler.job(COMMAND_LASER_OFF)
            return "spooler", spooler

        @kernel.console_argument(
            "amount", type=Length, help=_("amount to move in the set direction.")
        )
        @kernel.console_command(
            ("left", "right", "up", "down"),
            input_type=("spooler", None),
            output_type="spooler",
            help=_("cmd <amount>"),
        )
        def direction(command, channel, _, data=None, amount=None, **kwgs):
            if data is None:
                data = kernel.device.spooler
            spooler = data
            if amount is None:
                amount = Length("1mm")
            max_bed_height = kernel.device.bedheight
            max_bed_width = kernel.device.bedwidth
            if not hasattr(spooler, "_dx"):
                spooler._dx = 0
            if not hasattr(spooler, "_dy"):
                spooler._dy = 0
            if command.endswith("right"):
                spooler._dx += amount.value(ppi=1000.0, relative_length=max_bed_width)
            elif command.endswith("left"):
                spooler._dx -= amount.value(ppi=1000.0, relative_length=max_bed_width)
            elif command.endswith("up"):
                spooler._dy -= amount.value(ppi=1000.0, relative_length=max_bed_height)
            elif command.endswith("down"):
                spooler._dy += amount.value(ppi=1000.0, relative_length=max_bed_height)
            kernel.console(".timer 1 0 spool jog\n")
            return "spooler", spooler

        @kernel.console_option("force", "f", type=bool, action="store_true")
        @kernel.console_command(
            "jog",
            hidden=True,
            input_type=("spooler", None),
            output_type="spooler",
            help=_("executes outstanding jog buffer"),
        )
        def jog(command, channel, _, data, force=False, **kwgs):
            if data is None:
                data = kernel.device.spooler
            spooler = data
            try:
                idx = int(spooler._dx)
                idy = int(spooler._dy)
            except AttributeError:
                return
            if idx == 0 and idy == 0:
                return
            if force:
                spooler.job(execute_relative_position(idx, idy))
            else:
                if spooler.job_if_idle(execute_relative_position(idx, idy)):
                    channel(_("Position moved: %d %d") % (idx, idy))
                    spooler._dx -= idx
                    spooler._dy -= idy
                else:
                    channel(_("Busy Error"))
            return "spooler", spooler

        @kernel.console_option("force", "f", type=bool, action="store_true")
        @kernel.console_argument("x", type=Length, help=_("change in x"))
        @kernel.console_argument("y", type=Length, help=_("change in y"))
        @kernel.console_command(
            ("move", "move_absolute"),
            input_type=("spooler", None),
            output_type="spooler",
            help=_("move <x> <y>: move to position."),
        )
        def move(channel, _, x, y, data=None, force=False, **kwgs):
            if data is None:
                data = kernel.device.spooler
            spooler = data
            if y is None:
                raise SyntaxError
            if force:
                spooler.job(execute_absolute_position(x, y))
            else:
                if not spooler.job_if_idle(execute_absolute_position(x, y)):
                    channel(_("Busy Error"))
            return "spooler", spooler

        @kernel.console_option("force", "f", type=bool, action="store_true")
        @kernel.console_argument("dx", type=Length, help=_("change in x"))
        @kernel.console_argument("dy", type=Length, help=_("change in y"))
        @kernel.console_command(
            "move_relative",
            input_type=("spooler", None),
            output_type="spooler",
            help=_("move_relative <dx> <dy>"),
        )
        def move_relative(channel, _, dx, dy, data=None, force=False, **kwgs):
            if data is None:
                data = kernel.device.spooler
            spooler = data
            if dy is None:
                raise SyntaxError
            if force:
                spooler.job(execute_relative_position(dx, dy))
            else:
                if not spooler.job_if_idle(execute_relative_position(dx, dy)):
                    channel(_("Busy Error"))
            return "spooler", spooler

        @kernel.console_argument("x", type=Length, help=_("x offset"))
        @kernel.console_argument("y", type=Length, help=_("y offset"))
        @kernel.console_command(
            "home",
            input_type=("spooler", None),
            output_type="spooler",
            help=_("home the laser"),
        )
        def home(x=None, y=None, data=None, **kwgs):
            if data is None:
                data = kernel.device.spooler
            spooler = data
            if x is not None and y is not None:
                x = x.value(ppi=1000.0, relative_length=kernel.device.bedwidth)
                y = y.value(ppi=1000.0, relative_length=kernel.device.bedheight)
                spooler.job(COMMAND_HOME, int(x), int(y))
                return "spooler", spooler
            spooler.job(COMMAND_HOME)
            return "spooler", spooler

        @kernel.console_command(
            "unlock",
            input_type=("spooler", None),
            output_type="spooler",
            help=_("unlock the rail"),
        )
        def unlock(data=None, **kwgs):
            if data is None:
                data = kernel.device.spooler
            spooler = data
            spooler.job(COMMAND_UNLOCK)
            return "spooler", spooler

        @kernel.console_command(
            "lock",
            input_type=("spooler", None),
            output_type="spooler",
            help=_("lock the rail"),
        )
        def lock(data, **kwgs):
            if data is None:
                data = kernel.device.spooler
            spooler = data
            spooler.job(COMMAND_LOCK)
            return "spooler", spooler

        @kernel.console_command(
            "test_dot_and_home",
            input_type=("spooler", None),
            hidden=True,
        )
        def run_home_and_dot_test(data, **kwgs):
            if data is None:
                data = kernel.device.spooler
            spooler = data

            def home_dot_test():
                for i in range(25):
                    yield COMMAND_SET_ABSOLUTE
                    yield COMMAND_MODE_RAPID
                    yield COMMAND_HOME
                    yield COMMAND_LASER_OFF
                    yield COMMAND_WAIT_FINISH
                    yield COMMAND_MOVE, 3000, 3000
                    yield COMMAND_WAIT_FINISH
                    yield COMMAND_LASER_ON
                    yield COMMAND_WAIT, 0.05
                    yield COMMAND_LASER_OFF
                    yield COMMAND_WAIT_FINISH
                yield COMMAND_HOME
                yield COMMAND_WAIT_FINISH

            spooler.job(home_dot_test)
            return "spooler", spooler


class Spooler:
    """
    A spooler stores spoolable lasercode events as a synchronous queue.

    * peek()
    * pop()
    * job(job)
    * jobs(iterable<job>)
    * job_if_idle(job) -- Will enqueue the job if the device is currently idle.
    * clear_queue()
    * remove(job)
    """

    def __init__(self, context, *args, **kwargs):
        self.context = context
        self.queue_lock = Lock()
        self._queue = []

    def __repr__(self):
        return "Spooler(%s)" % str(self.context)

    def __del__(self):
        self.name = None
        self.queue_lock = None
        self._queue = None

    def __len__(self):
        return len(self._queue)

    def as_device(self):
        links = []
        obj = self
        while obj is not None:
            links.append(str(obj))
            obj = obj.next
        return " -> ".join(links)

    @property
    def queue(self):
        return self._queue

    def append(self, item):
        self.job(item)

    def peek(self):
        if len(self._queue) == 0:
            return None
        return self._queue[0]

    def pop(self):
        if len(self._queue) == 0:
            self.context.signal("spooler;queue", len(self._queue))
            return None
        self.queue_lock.acquire(True)
        queue_head = self._queue[0]
        del self._queue[0]
        self.queue_lock.release()
        self.context.signal("spooler;queue", len(self._queue))
        return queue_head

    def job(self, *job):
        """
        Send a single job event with parameters as needed.

        The job can be a single command with (COMMAND_MOVE 20 20) or without parameters (COMMAND_HOME), or a generator
        which can yield many lasercode commands.

        :param job: job to send to the spooler.
        :return:
        """
        self.queue_lock.acquire(True)

        if len(job) == 1:
            self._queue.extend(job)
        else:
            self._queue.append(job)
        self.queue_lock.release()
        self.context.signal("spooler;queue", len(self._queue))

    def jobs(self, jobs):
        """
        Send several jobs generators to be appended to the end of the queue.

        The jobs parameter must be suitable to be .extended to the end of the queue list.
        :param jobs: jobs to extend
        :return:
        """
        self.queue_lock.acquire(True)
        if isinstance(jobs, (list, tuple)):
            self._queue.extend(jobs)
        else:
            self._queue.append(jobs)
        self.queue_lock.release()
        self.context.signal("spooler;queue", len(self._queue))

    def job_if_idle(self, element):
        if len(self._queue) == 0:
            self.job(element)
            return True
        else:
            return False

    def clear_queue(self):
        self.queue_lock.acquire(True)
        self._queue = []
        self.queue_lock.release()
        self.context.signal("spooler;queue", len(self._queue))

    def remove(self, element, index=None):
        self.queue_lock.acquire(True)
        if index is None:
            self._queue.remove(element)
        else:
            del self._queue[index]
        self.queue_lock.release()
        self.context.signal("spooler;queue", len(self._queue))
