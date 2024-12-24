import sys
import threading
import socket
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class ChatClient(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

        # Networking
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nickname = None

    def init_ui(self):
        self.setWindowTitle("User Chat")
        self.resize(700, 1000)

        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Status bar
        self.status_label = QLabel("Disconnected")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Arial", 10))
        self.status_label.setStyleSheet("background-color: #444; color: #fff; padding: 3px; border-radius: 5px;")
        main_layout.addWidget(self.status_label)

        # Chat display area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("background-color: #f9f9f9; font-size: 30px; padding: 10px; border: 1px solid #ccc;")
        main_layout.addWidget(self.chat_display)

        # Message input area
        input_layout = QHBoxLayout()

        self.message_input = QLineEdit()
        self.message_input.setStyleSheet("padding: 10px; font-size: 30px; border: 1px solid #ccc; border-radius: 5px;")
        input_layout.addWidget(self.message_input)

        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet(
            "background-color: #007bff; color: #fff; padding: 10px; font-weight: bold; border-radius: 5px;"
        )
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)

        main_layout.addLayout(input_layout)

    def connect_to_server(self, host, port, nickname):
        try:
            self.client.connect((host, port))
            self.nickname = nickname
            self.client.send(self.nickname.encode('ascii'))
            self.status_label.setText(f"Connected as {self.nickname}")
            self.status_label.setStyleSheet("background-color: #28a745; color: #fff; padding: 3px; border-radius: 5px;")

            # Start a thread to receive messages
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            self.chat_display.append(f"Error connecting to server: {e}")
            self.status_label.setText("Error: Unable to connect")
            self.status_label.setStyleSheet("background-color: #dc3545; color: #fff; padding: 3px; border-radius: 5px;")

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode('ascii')
                self.chat_display.append(message)
            except:
                self.chat_display.append("Connection lost.")
                self.client.close()
                break

    def send_message(self):
        message = self.message_input.text().strip()
        if message:
            formatted_message = f"{self.nickname}: {message}"
            self.client.send(formatted_message.encode('ascii'))
            self.message_input.clear()


def main():
    app = QApplication(sys.argv)

    # Get nickname before starting
    from PyQt5.QtWidgets import QInputDialog

    nickname, ok = QInputDialog.getText(None, "Enter Nickname", "Nickname:")
    if not ok or not nickname:
        sys.exit()

    # Create chat client
    client = ChatClient()
    client.connect_to_server("Server's  IP Address", 31260, nickname)
    client.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
