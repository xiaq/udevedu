"""
udevedu is a little tool that allows you to call a Python function on udev
events.
"""

__version__ = '0.1dev'

import os
import sys
import imp
import glob
import logging
from threading import Thread
from functools import partial

import pyudev
from xdg.BaseDirectory import load_first_config, save_config_path

import udevedu.hooks


def spawn_partial(f, *args, **kwargs):
    Thread(target=partial(f, *args, **kwargs)).start()


def process_hook(h, args):
    if not hasattr(h, 'react'):
        return
    if hasattr(h, 'check') and not h.check(*args):
        return
    h.react(*args)


def main():
    loglevel = logging.WARN
    if len(sys.argv) == 2 and sys.argv[1] == '-d':
        loglevel = logging.INFO
    logging.basicConfig(
        level=loglevel,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%F %T'
    )

    save_config_path('udevedu', 'hooks')
    hooks_dir = load_first_config('udevedu', 'hooks')

    hooks = []

    # Load all hooks
    for fname in sorted(glob.glob(os.path.join(hooks_dir, '*.py'))):
        if not os.path.isfile(fname):
            continue
        logging.info('Loading source %s', fname)

        mod = os.path.splitext(os.path.basename(fname))[0]
        try:
            hooks.append(imp.load_source('udevedu.hooks.%s' % mod, fname))
        except Exception as e:
            logging.error('Loading of %s failed', fname)
            logging.exception(e)

    while True:
        try:
            context = pyudev.Context()
            monitor = pyudev.Monitor.from_netlink(context)

            for args in monitor:
                # args is (action, device)
                for h in hooks:
                    spawn_partial(process_hook, h, args)
        except KeyboardInterrupt:
            logging.warn('User interrupt, exiting')
            break
        except IOError as e:
            logging.warn('Recovering from IOError, continue polling')
            logging.exception(e)
