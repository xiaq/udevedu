"""
Mount and unmount MTP devices automatically.
"""

#---- conf begin
mp_root = '~/mtp'
#---- conf end

import os
import os.path

from udevedu.utils import mkdir_p, invoke

mounted = set()
mp_root = os.path.expanduser(mp_root)

def check(action, device):
    return device.get('ID_MTP_DEVICE')

def react(action, device):
    print 'MTP device %s,' % action,

    try:
        bus = device['BUSNUM']
        dev = device['DEVNUM']
        model = device['ID_MODEL']
    except KeyError as e:
        print 'but %s key missing' % e.args[0]
        return

    print 'model is %s,' % model,

    mp = os.path.join(mp_root, model)

    if action == 'add':
        try:
            mkdir_p(mp)
        except OSError as e:
            print 'but failed to create mountpoint %s' % mp
            return
        else:
            print 'created mountpoint %s, mouting' % mp

        e = invoke('jmtpfs', '-device=%s,%s' % (bus, dev), mp)
        if e is None:
            mounted.add((bus, dev))

    elif action == 'remove':
        if (bus, dev) not in mounted:
            print "but I didn't seem to have mounted it, unmounting anyway"
        else:
            print 'unmounting'
            mounted.remove((bus, dev))
        invoke('fusermount', '-u', mp)
