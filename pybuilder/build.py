#   -*- coding: utf-8 -*-
from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")



name = "pybuilder"
default_task = "publish"
version = "1.0"
url ="https://github.com/VelvetFractal/voila"
desciption = "Telegram bot that allows you to monitor wallets on Ethereum"
authors = "VelvetFractal"
license = "none"

@init
def set_properties():
    pass
