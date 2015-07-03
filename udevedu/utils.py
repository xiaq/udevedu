import os
import errno
import logging
import subprocess


def invoke(*args):
    logging.info('invoking %s', args)
    try:
        return subprocess.check_output(args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        dump_process_error(e)
        return e
    else:
        logging.info('%s success', args)
        return None


def dump_process_error(e):
    print(
        "---------------------------------------------\n"
        "Exit code: %d\n"
        "Captured output:\n"
        "%s\n"
        "---------------------------------------------"
        % (e.returncode, e.output.strip())
    )


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
