import sys
from auth import Login
from server_api import ServerAPI
from PyQt5.QtWidgets import QApplication
from window_manager import WindowsManager


app = QApplication(sys.argv)
wm = WindowsManager()
wm.add("db", ServerAPI())
ex = Login(wm)
sys.exit(app.exec_())