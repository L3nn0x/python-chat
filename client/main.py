import socket
import select
from common.protocol import *
from common.packet import *

from client import Client

from window import MainWindow
from checker import Checker

window = MainWindow()
checker = Checker(window)
window.bind(checker.sendMsg)
checker.start()
window.mainloop()
checker.stop()
checker.join()
