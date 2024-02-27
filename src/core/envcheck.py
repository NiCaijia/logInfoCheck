import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from utils import logging_utils
import pip
import pkg_resources


def is_installed(package):
    try:
        pip.main(['freeze', '--local'])
    except:
        logging_utils.init_logger()
        return False

    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    for p in installed_packages:
        if p == package:
            return True

    return False


# Check if xlwt is installed
if is_installed("xlwt"):
    # Use xlwt to do something
    pass
    print("当前环境以存在xlwt环境。")
else:
    # Install xlwt from a local wheel file
    lib_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "libs")
    wheel_path = os.path.join(lib_path, "xlwt-1.3.0-py2.py3-none-any.whl")
    pip.main(['install', '--no-index', '--find-links', lib_path, wheel_path])
    print("已成功安装xlwt环境。")