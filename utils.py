import re
import socket


def parse_argv(buf):
    argv = re.split(' ', buf)
    return argv, len(argv)


def check_parameter(argv):
    if len(argv) != 2:
        return False
    else:
        return True


def get_constants(prefix):
    return dict(
        (getattr(socket, n), n)
        for n in dir(socket)
        if n.startswith(prefix)
    )
