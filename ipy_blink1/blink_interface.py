# main interface to blink(1)

from blink1.blink1 import blink1
import atexit
from random import random


class BlinkInterface(object):
    def __init__(self, ipython):
        self.ipython = ipython

        # send patterns to blink1, and store indices into pattern memory
        self.executing_pattern = (1, 2)
        with blink1(switch_off=False) as b1:
            b1.write_pattern_line(1000, "blue", 1)
            b1.write_pattern_line(1000, "darkblue", 2)

            self.error_pattern = (3, 6)
            # the fades to same color make the led blink - i.e. fades
            # have hard edges
            b1.write_pattern_line(0, "red", 3)
            b1.write_pattern_line(500, "red", 4)
            b1.write_pattern_line(0, "black", 5)
            b1.write_pattern_line(500, "black", 6)

            self.complete_pattern = (7, 7)
            b1.write_pattern_line(100, "green", 7)

        # set up event listeners
        ipython.events.register("pre_run_cell", self.pre_run_cell)
        ipython.events.register("post_run_cell", self.post_run_cell)
        atexit.register(self.shutdown)


    def pre_run_cell(self):
        with blink1(switch_off=False) as b1:
            b1.play(*self.executing_pattern)

    def post_run_cell(self, result):
        with blink1(switch_off=False) as b1:
            if result.success:
                # there was no exception
                b1.play(*self.complete_pattern)
            else:
                # something went wrong
                b1.play(*self.error_pattern)

    def shutdown(self):
        with blink1(switch_off=False) as b1:
            b1.fade_to_color(0, "black")
            b1.close()
