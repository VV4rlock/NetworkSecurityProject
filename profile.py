

import sys
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QGridLayout, QLabel, QPushButton, \
    QMessageBox
from PyQt5.QtGui import QIcon

#from bills import Bills
from server_api import ServerAPI
from window_manager import WindowsManager


class Profile(QWidget):
    def __init__(self,win_manager,user):
        self.user=user
        self.wm=win_manager
        self.wm.add("profile", self)
        self.db=self.wm.get_window("db")
        super().__init__()
        self.title = 'Profile'
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
        login=self.db.get_account_by_id(self.user[0])
        login_label=QLabel("Login:")
        login_name=QLabel(login[0])
        pass_label=QLabel("Old password:")
        self.old_password_field=QLineEdit()
        new_pass_label = QLabel("New password:")
        self.new_pass = QLineEdit()

        change_btn = QPushButton('change_password', self)
        change_btn.clicked.connect(self.on_change_click)
        back_btn = QPushButton('Back', self)
        back_btn.clicked.connect(self.on_back_clicked)

        grid_layout.addWidget(login_label,0,0)
        grid_layout.addWidget(login_name, 0, 1)
        grid_layout.addWidget(pass_label, 1, 0)
        grid_layout.addWidget(self.old_password_field, 1, 1)
        grid_layout.addWidget(new_pass_label, 2, 0)
        grid_layout.addWidget(self.new_pass, 2, 1)
        grid_layout.addWidget(change_btn,3,0)
        grid_layout.addWidget(back_btn, 3, 1)



        self.show()


    def on_back_clicked(self):
        main=self.wm.get_window("main")
        main.setVisible(True)
        self.setVisible(False)



    def on_change_click(self):
        try:

            flag=self.db.change_pass(self.user[1],self.old_password_field.text(),self.new_pass.text())

        except:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.showMessage('Sorry!')
            return
        print(flag)
        #придумать как вернуться назад к ауфу
        QMessageBox.information(self,"Change pass", str("Password has been changed!"),QMessageBox.Ok)

