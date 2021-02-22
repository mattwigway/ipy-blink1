# main interface to blink(1)

from blink1.blink1 import Blink1, Blink1ConnectionFailed
import atexit


class BlinkInterface(object):
    def __init__(self, ipython):
        self.ipython = ipython
        for i in range(5):
            try:
                self.b1 = Blink1()
            except Blink1ConnectionFailed:
                pass
            else:
                break  # don't retry once connection succeeds
        else:
            print("Could not connect to Blink(1)")
            return

        # send patterns to blink1, and store indices into pattern memory
        self.executing_pattern = (1, 2)
        self.b1.write_pattern_line(1000, "blue", 1)
        self.b1.write_pattern_line(1000, "darkblue", 2)

        self.error_pattern = (3, 6)
        # the fades to same color make the led blink - i.e. fades
        # have hard edges
        self.b1.write_pattern_line(0, "red", 3)
        self.b1.write_pattern_line(500, "red", 4)
        self.b1.write_pattern_line(0, "black", 5)
        self.b1.write_pattern_line(500, "black", 6)

        self.complete_pattern = (7, 7)
        self.b1.write_pattern_line(100, "green", 7)

        # set up event listeners
        ipython.events.register("pre_run_cell", self.pre_run_cell)
        ipython.events.register("post_run_cell", self.post_run_cell)
        atexit.register(self.shutdown)

    def pre_run_cell(self):
        self.b1.play(*self.executing_pattern)

    def post_run_cell(self, result):
        if result.success:
            # there was no exception
            self.b1.play(*self.complete_pattern)
        else:
            # something went wrong
            self.b1.play(*self.error_pattern)

    def shutdown(self):
        self.b1.fade_to_color(0, "black")
        self.b1.close()
