import os
import subprocess
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QCheckBox, QFileDialog, QHBoxLayout, QVBoxLayout, QGridLayout, QMessageBox, QGroupBox

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("phBot Manager")
        self.setFixedSize(700, 500)
        self.setStyleSheet("font-size: 14px;")

        self.create_username_input()
        self.create_password_input()
        self.create_server_input()
        self.create_character_name_input()
        self.create_passcode_input()
        self.create_options_group()
        self.create_bot_dir_button()
        self.create_save_button()
        self.create_load_groups_button()
        self.create_groups_layout()
        self.create_start_all_button()

        self.db_conn = sqlite3.connect("phbot_manager.db")
        self.c = self.db_conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS characters
                          (id INTEGER PRIMARY KEY,
                           username TEXT,
                           password TEXT,
                           server TEXT,
                           character_name TEXT,
                           passcode TEXT,
                           options TEXT)""")
        self.c.execute("""CREATE TABLE IF NOT EXISTS groups
                          (id INTEGER PRIMARY KEY,
                           name TEXT,
                           characters TEXT)""")

    def create_username_input(self):
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")

    def create_password_input(self):
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)

    def create_server_input(self):
        self.server_label = QLabel("Server:")
        self.server_input = QLineEdit()
        self.server_input.setPlaceholderText("Enter server IP or name")

    def create_character_name_input(self):
        self.character_name_label = QLabel("Character Name:")
        self.character_name_input = QLineEdit()
        self.character_name_input.setPlaceholderText("Enter your character name")

    def create_passcode_input(self):
        self.passcode_label = QLabel("Passcode:")
        self.passcode_input = QLineEdit()
        self.passcode_input.setPlaceholderText("Enter passcode if exists")
        self.passcode_input.setEchoMode(QLineEdit.Password)

    def create_options_group(self):
        self.options_group = QGroupBox("Options")

        self.loginserver_checkbox = QCheckBox("Login Server")
        self.locale_checkbox = QCheckBox("Locale")
        self.minimize_checkbox = QCheckBox("Minimize")
        self.clientless_checkbox = QCheckBox("Clientless")
        self.hide_checkbox = QCheckBox("Hide")

        layout = QVBoxLayout()
        layout.addWidget(self.loginserver_checkbox)
        layout.addWidget(self.locale_checkbox)
        layout.addWidget(self.minimize_checkbox)
        layout.addWidget(self.clientless_checkbox)
        layout.addWidget(self.hide_checkbox)

        self.options_group.setLayout(layout)

    def create_bot_dir_button(self):
        self.bot_dir_label = QLabel("Bot Directory:")
        self.bot_dir_input = QLineEdit()
        self.bot_dir_input.setReadOnly(True)
        self.bot_dir_button = QPushButton("Select")

        self.bot_dir_button.clicked.connect(self.select_bot_dir)

    def select_bot_dir(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Bot Directory")
        self.bot_dir_input.setText(directory)

    def create_save_button(self):
        self.save_button = QPushButton("Save Character")
        self.save_button.clicked.connect(self.save_character)

    def save_character(self):
        username = self.username_input.text()
        password = self.password_input.text()
        server = self.server_input.text()
        charname = self.charname_input.text()
        passcode = self.passcode_input.text()

        options = []
        if self.loginserver_checkbox.isChecked():
            options.append("--loginserver")
        if self.locale_checkbox.isChecked():
            options.append("--locale")
        if self.minimize_checkbox.isChecked():
            options.append("--minimize")
        if self.clientless_checkbox.isChecked():
            options.append("--clientless")
        if self.hide_checkbox.isChecked():
            options.append("--hide")

        options_str = " ".join(options)

        groups = self.get_selected_groups()

        bot_dir = self.bot_dir_lineedit.text()

        conn = sqlite3.connect('phbot_manager.db')
        c = conn.cursor()

        c.execute(
            "INSERT INTO characters (username, password, server, charname, passcode, options, groups, bot_dir) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (username, password, server, charname, passcode, options_str, groups, bot_dir))

        conn.commit()
        conn.close()
