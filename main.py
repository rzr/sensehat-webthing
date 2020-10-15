#!/usr/bin/env python3
# -*- mode: python; python-indent-offset: 4; indent-tabs-mode: nil -*-
# SPDX-License-Indentifier: MPL-2.0

"""SenseHat adapter for WebThings Gateway."""

from os import path
import functools
import signal
import sys
import time

sys.path.append(path.join(path.dirname(path.abspath(__file__)), 'lib'))

from pkg.sense_hat_adapter import SenseHatAdapter

_DEBUG = False
_ADAPTER = None

print = functools.partial(print, flush=True)


def cleanup(signum, frame):
    """Clean up any resources before exiting."""
    if _ADAPTER is not None:
        _ADAPTER.close_proxy()
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)
    _ADAPTER = SenseHatAdapter(verbose=_DEBUG)

    # Wait until the proxy stops running, indicating that the gateway shut us
    # down.
    while _ADAPTER.proxy_running():
        time.sleep(2)
