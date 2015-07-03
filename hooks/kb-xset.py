"""
Call xset on keyboard changes.
"""

# ---- conf begin
xset_args = ['r', 'rate', '180', '60']
# ---- conf end

from udevedu.utils import invoke


def check(action, device):
    return device.get('ID_INPUT_KEYBOARD') and device.get('LED')


def react(action, device):
    print('new keyboard attached')
    invoke('xset', *xset_args)
