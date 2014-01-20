# udevedu: udev Event Dispatcher for Unpriviledged user

udevedu is a little tool that allows you to call a Python function on udev
events.

## Usage

To install, run: `sudo pip install .` A script named `udevedu` will be put in
/usr/bin. (You can also do `pip install --user .`, which will put the script
`~/.local/bin`, and you need to take care to add that to your `$PATH`.)

Put hooks in `~/.config/udevedu/hooks`, which will be created the first time
`udevedu` is invoked. Some sample hooks (read: hooks used by me, xiaq) are
contained in the `hook/` directory of the repository.

## Anatomy of hook scripts

Three functions are looked for in hook scripts: `init`, `check` and `react`.
They are all optional.

`init` function is called after udevedu has started and collected all hook
scripts.

`check` and `react` is called when a udev event is received. If `check`
doesn't exist or returns a true value, `react` is called. Both are passed two
positional arguments, `action` and `device` which come from
[pyudev.Monitor.receive_device](http://pyudev.readthedocs.org/en/latest/api/pyudev.html#pyudev.Monitor.receive_device).

Notes:

* `check` is actually not necessary, but it would save you one level of
  indentation.
* `check` and `react` are called off the main thread, so that they may block.

## Why not just write [udev rules](http://www.freedesktop.org/software/systemd/man/udev.html)?

Because udevedu runs as an unpriviledged user in arbitrary environment - e.g.
from your WM script so that it can call `xset`, `notify-send` etc.

Other small bonuses:

* You don't need to learn yet another arcane configuration language - the
  information of the event is available as easy-to-use
  [pyudev](http://pyudev.readthedocs.org/) objects
* Hook functions are executed in separate threads, so that one blocking hook
  doesn't affect other hooks
* It's also much easier to experiment and debug - just put
  `from pdb import set_trace; set_trace()` anywhere in the `check` or `react`
  function.

## TODO

* Automatic reload of hook scripts

* `pyudev.Monitor.receive_device` is deprecated, should use new interface;
  maybe also use the asynchronous `pyudev.MonitorObserver`?
