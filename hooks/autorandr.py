"""
Call `autorandr -c` on monitor changes.
"""

from udevedu.utils import invoke

def check(action, device):
    print 'randr:', device.get('DEVTYPE')
    return device.get('DEVTYPE') == 'drm_minor'

def react(action, device):
    print 'monitor change'
    invoke('autorandr', '-c')
