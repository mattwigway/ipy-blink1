# Load the extension - main code is in class file
from ipy_blink1.blink_interface import BlinkInterface


def load_ipython_extension(ipython):
    BlinkInterface(ipython)
