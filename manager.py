from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QCheckBox,
    QPushButton,
    QFileDialog,
    QGroupBox,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
    QWidget,
)
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("phBot Manager")
        self.setFixedSize(700, 500)
        self.setStyleSheet("font-size: 14px;")

        # Create input fields
        self.create_username_input()
        self.create_password_input()
        self.create_server_input()
        self.create_character_name_input()
        self.create_passcode_input()

        # Create options group
        self.create_options_group()

        # Create bot directory button
        self.create_bot_dir_button()

        # Create save button
        self.create_save_button()

        # Create load groups button
        self.create_load_groups_button()

        # Create groups layout
        self.create_groups_layout()

        # Create start all button
        self.create_start_all_button()

        # Add layout to window
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.username_group)
        main_layout.addWidget(self.password_group)
        main_layout.addWidget(self.server_group)
        main_layout.addWidget(self.character_name_group)
        main_layout.addWidget(self.passcode_group)
        main_layout.addWidget(self.options_group)
        main_layout.addWidget(self.bot_dir_group)
        main_layout.addWidget(self.save_button)
        main_layout.addWidget(self.load_groups_button)
        main_layout.addLayout(self.groups_layout)
        main_layout.addWidget(self.start_all_button)
        self.setLayout(main_layout)

    def create_username_input(self):
        self.username_group = QGroupBox("Username")
        layout = QHBoxLayout()
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)
        self.username_group.setLayout(layout)

    def create_password_input(self):
        self.password_group = QGroupBox("Password")
        layout = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)
        self.password_group.setLayout(layout)

    def create_server_input(self):
        self.server_group = QGroupBox("Server")
        layout = QHBoxLayout()
        self.server_input = QLineEdit()
        layout.addWidget(self.server_input)
        self.server_group.setLayout(layout)

    def create_character_name_input(self):
        self.character_name_group = QGroupBox("Character Name")
        layout = QHBoxLayout()
        self.character_name_input = QLineEdit()
        layout.addWidget(self.character_name_input)
        self.character_name_group.setLayout(layout)

    def create_passcode_input(self):
        self.passcode_group = QGroupBox("Passcode")
        layout = QHBoxLayout()
        self.passcode_input = QLineEdit()
        self.passcode_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.passcode_input)
        self.passcode_group.setLayout(layout)

    def create_options_group(self):
        self.options_group = QGroupBox("Options")
        layout = QVBoxLayout()

        self.loginserver_checkbox = QCheckBox("Login Server")
        layout.addWidget(self.loginserver_checkbox)

        self.locale_checkbox = QCheckBox("Locale")
        layout.addWidget(self.locale_checkbox)

        self.minimize_checkbox = QCheckBox("Minimize")
        layout.addWidget(self.minimize_checkbox)

        self.clientless_checkbox = QCheckBox("Clientless")
        layout.addWidget(self.clientless_checkbox)

        self.hide_checkbox = QCheckBox("Hide")
        layout.addWidget(self.hide_checkbox)

        self.options_group.setLayout(layout)

    def create_bot_dir_button(self):
        self.bot_dir_group = QGroupBox("Bot Directory")
        layout = QHBoxLayout()
        self.bot_dir_input = QLineEdit()
        self.bot_dir_input.setReadOnly(True)
        layout.addWidget(self.bot_dir_input)
        self.bot_dir_button = QPushButton("Select")
        self.bot_dir_button.clicked.connect(self.select_bot_dir)
        layout.addWidget(self.bot_dir_button)
        self.bot_dir_group.setLayout(layout)

    def create_save_button(self):
        self.save_button = QPushButton("Save Character")
        self.save_button.clicked.connect(self.save_character)

        self.save_character_checkbox = QCheckBox("Save this character to a group")
        self.save_character_checkbox.setChecked(False)
        self.save_character_checkbox.stateChanged.connect(self.enable_group_input)

        self.save_button_layout = QHBoxLayout()
        self.save_button_layout.addWidget(self.save_button)
        self.save_button_layout.addWidget(self.save_character_checkbox)

        self.main_layout.addLayout(self.save_button_layout)

    def create_load_groups_button(self):
        self.load_groups_button = QPushButton("Load Groups")
        self.load_groups_button.clicked.connect(self.load_groups)

        self.load_groups_layout = QHBoxLayout()
        self.load_groups_layout.addWidget(self.load_groups_button)

        self.main_layout.addLayout(self.load_groups_layout)

    def create_groups_layout(self):
        self.groups_layout = QVBoxLayout()
        self.groups_layout.setContentsMargins(0, 20, 0, 0)
        self.groups_layout.setAlignment(Qt.AlignTop)

        groups_label = QLabel("Groups:")
        self.groups_layout.addWidget(groups_label)

        self.group_buttons = []
        self.group_layouts = []

        c.execute("SELECT name FROM groups")
        results = c.fetchall()
        for result in results:
            name = result[0]
            group_layout = QHBoxLayout()
            group_button = QPushButton(name)
            group_button.clicked.connect(lambda _, name=name: self.start_group(name))
            group_delete_button = QPushButton("Delete")
            group_delete_button.clicked.connect(lambda _, name=name: self.delete_group(name))
            group_layout.addWidget(group_button)
            group_layout.addWidget(group_delete_button)
            self.group_buttons.append(group_button)
            self.group_layouts.append(group_layout)
            self.groups_layout.addLayout(group_layout)

        self.main_layout.addLayout(self.groups_layout)

    def create_start_all_button(self):
        self.start_all_button = QPushButton("Start All")
        self.start_all_button.clicked.connect(self.start_all)

    def start_all(self):
        c.execute("SELECT characters FROM groups")
        results = c.fetchall()
        for result in results:
            characters = result[0]
            if characters != "":
                subprocess.run(["phbot.exe", "-c", characters])
