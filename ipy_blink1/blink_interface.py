# main interface to blink(1)

from blink1.blink1 import Blink1, Blink1ConnectionFailed
import atexit
from random import random


class Blink1NoClear(object):
    """
    This is similar to the blink1() context manager, but does not turn the LED off when exiting
    By using this context manager everywhere, multiple notebooks can access the Blink(1) mostly
    simultaneously (if they actually try to change state exactly simultaneously, one will win).

    The Blink1 is closed when not in use, but is not turned off - so it will display whatever happened
    most recently in any notebook.
    """
    def __init__ (self):
        for i in range(5):
            try:
                self.b1 = Blink1()
            except Blink1ConnectionFailed:
                pass
            else:
                break  # don't retry once connection succeeds
        else:
            print("Could not connect to Blink(1)")
            sleep(0.01 * i ** 2)  # exponential backoff to resolve resource contention
    
    def __enter__ (self):
        return self.b1

    def __exit__ (self, type, value, traceback):
        self.b1.close()

class BlinkInterface(object):
    def __init__(self, ipython):
        self.ipython = ipython

        # send patterns to blink1, and store indices into pattern memory
        self.executing_pattern = (1, 2)
        with Blink1NoClear() as b1:
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
        with Blink1NoClear() as b1:
            b1.play(*self.executing_pattern)

    def post_run_cell(self, result):
        with Blink1NoClear() as b1:
            if result.success:
                # there was no exception
                b1.play(*self.complete_pattern)
            else:
                # something went wrong
                b1.play(*self.error_pattern)

    def shutdown(self):
        with Blink1NoClear() as b1:
            b1.fade_to_color(0, "black")
            b1.close()
