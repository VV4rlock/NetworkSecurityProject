import sys
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QGridLayout, QLabel, QPushButton
from PyQt5.QtGui import QIcon
from signup import Signup
from server_api import ServerAPI
from window_manager import WindowsManager
from main_win import Main_win


class Login(QWidget):
    def __init__(self,win_manager):
        super().__init__()
        self.wm=win_manager
        self.wm.add("login",self)
        self.db=None#self.wm.get_window("db")
        self.title = 'Log In'
        self.left = 350
        self.top = 350
        self.width = 340
        self.height = 150
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        grid_layout = QGridLayout()  # Создаём QGridLayout

        self.setLayout(grid_layout)
        self.login_label=QLabel("Login:")
        self.login_field=QLineEdit()
        self.password_label=QLabel("Password:")
        self.password_field=QLineEdit()

        self.ip_label = QLabel("ip:")
        self.ip_field = QLineEdit()
        self.ip_field.setText("127.0.0.1")

        self.port_label = QLabel("port:")
        self.port_field = QLineEdit()
        self.port_field.setText("8888")

        self.signup_btn = QPushButton('Sign Up', self)
        self.login_btn = QPushButton('Log In', self)
        grid_layout.addWidget(self.login_label,0,0)
        grid_layout.addWidget(self.login_field, 0, 1)
        grid_layout.addWidget(self.password_label, 1, 0)
        grid_layout.addWidget(self.password_field, 1, 1)

        grid_layout.addWidget(self.ip_label, 2, 0)
        grid_layout.addWidget(self.ip_field, 2, 1)
        grid_layout.addWidget(self.port_label, 3, 0)
        grid_layout.addWidget(self.port_field, 3, 1)

        grid_layout.addWidget(self.signup_btn,4,0)
        grid_layout.addWidget(self.login_btn, 4, 1)

        self.login_btn.clicked.connect(self.on_log_in_btn_cklick)
        self.signup_btn.clicked.connect(self.on_signup_btn_clicked)

        self.password_field.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.show()


    def on_log_in_btn_cklick(self):
        login=self.login_field.text()
        password=self.password_field.text()

        if self.db is None:
            try:
                if 'db' not in self.wm.get_keys():
                    self.db=ServerAPI(self.ip_field.text(),int(self.port_field.text()))
                    self.wm.add('db',self.db)
                else:
                    self.db=self.wm.get_window('db')
            except:
                self.error_dialog = QtWidgets.QErrorMessage()
                self.error_dialog.showMessage('Invalid ip or port!')
                return
        try:
            account=self.db.auth(login,password)
        except:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.showMessage("Some error in auth!(")
            return

        if account is None:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.showMessage('Invalid login or password!')
            return

        self.setVisible(False)
        self.main_win=Main_win(self.wm,account)




    def on_signup_btn_clicked(self):
        if self.db is None:
            try:
                if 'db' not in self.wm.get_keys():
                    self.db=ServerAPI(self.ip_field.text(),int(self.port_field.text()))
                    self.wm.add('db',self.db)
                else:
                    self.db=self.wm.get_window('db')
            except:
                self.error_dialog = QtWidgets.QErrorMessage()
                self.error_dialog.showMessage('Invalid ip or port!')
                return

        self.sg=Signup(self.wm)
        self.sg.show()
        self.setVisible(False)






if __name__ == '__main__':
    app = QApplication(sys.argv)
    wm = WindowsManager()
    wm.add("db", ServerAPI())
    ex = Login(wm)
    sys.exit(app.exec_())