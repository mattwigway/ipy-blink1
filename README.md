# ipy-blink1

This is an IPython extension to show kernel status on a [blink(1)](https://blink1.thingm.com/) USB LED. It shows green when the kernel is idle, pulsing blue when it is running code, and flashing red when an exception has occurred.

## Installation

This is not on PyPI yet, so a local install is necessary:

```
git clone https://github.com/mattwigway/ipy-blink1.git
cd ipy-blink1
pip install .
```

## Usage

Just add `%load_ext ipy_blink1` at the top of your notebook.