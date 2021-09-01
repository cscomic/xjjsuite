import linecache
import os
import random

from lib.core.data import paths


def setPaths(rootPath):
    # path
    paths.ROOT_PATH = rootPath
    paths.DATA_PATH = os.path.join(paths.ROOT_PATH, "data")
    paths.VULNS_PATH = os.path.join((paths.ROOT_PATH, "vulns"))
    paths.REPORT_PATH = os.path.join((paths.ROOT_PATH, "reports"))

    # file
    paths.USER_AGENTS = os.path.join(paths.DATA_PATH, "user-agents.txt")


def desensitization(s):
    """ Hide sensitive information.
    """
    s = str(s)
    return (
            s[:len(s) // 4 if len(s) < 30 else 8] +
            '***' +
            s[len(s) * 3 // 4:]
    )
