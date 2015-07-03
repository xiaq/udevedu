"""
Call `autorandr -c` on monitor changes.
"""

from udevedu.utils import invoke


def check(action, device):
    return device.get('DEVTYPE') == 'drm_minor'


def init():
    print('init autorandr')
    invoke('autorandr', '-c')


def react(action, device):
    print('monitor change')
    invoke('autorandr', '-c')
