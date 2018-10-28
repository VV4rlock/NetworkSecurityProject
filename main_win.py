
from PyQt5.QtWidgets import QWidget, QTextEdit, QGridLayout, QApplication, QPushButton, QHBoxLayout, QLabel, QMessageBox
import sys
from profile import Profile
from server_api import ServerAPI

class Main_win(QWidget):
    def __init__(self,win_manager,user):
        super().__init__()

        self.user=user
        self.wm = win_manager
        self.wm.add("main", self)
        self.setWindowTitle("Main window")
        self.db=win_manager.get_window('db')


        grid=QGridLayout()
        self.setLayout(grid)

        self.message=QTextEdit()
        self.message.setPlainText("message")
        grid.addWidget(self.message,0,0)

        self.result_text = QTextEdit()
        self.result_text.setPlainText("answer")
        grid.addWidget(self.result_text,0,1)

        hbox = QHBoxLayout()

        send_btn = QPushButton("send")

        send_btn.clicked.connect(self.on_send_clicked)

        profile_btn = QPushButton("profile")

        profile_btn.clicked.connect(self.on_profile_clicked)


        hbox.addStretch()
        hbox.addWidget(send_btn)
        hbox.addWidget(profile_btn)


        grid.addLayout(hbox, 3, 0, 1, 3)


        self.show()


    def on_profile_clicked(self):
        self.setVisible(False)
        profile_win=self.wm.get_window('profile')
        if profile_win is None:
            profile_win=Profile(self.wm, self.user)
        else:
            profile_win.setVisible(True)


    def on_send_clicked(self):
        data=self.message.toPlainText()
        self.result_text.setPlainText(self.db.send_str(data))




    def get_connection_params(self):
        a=(self.ip.toPlainText(), int(self.port.toPlainText()))
        return a

