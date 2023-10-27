import os
import sys
import time
import logging
import paramiko
from scp import SCPClient, SCPException
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logging.basicConfig(
    filename="log_file.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)
logger.info(
    f"======================================= {datetime.now()} ======================================="
)


class SSHManager:
    def __init__(self) -> None:
        self.ssh_client = None
        self.retry_counter = 0

    def create_ssh_client(self, hostname, username, password, port):
        if self.ssh_client is None:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                self.ssh_client.connect(
                    hostname,
                    username=username,
                    password=password,
                    port=port,
                    timeout=2,
                )
            except Exception as e:
                logger.error(e)
                self.ssh_client = None
                self.retry_counter = self.retry_counter + 1
                logger.debug("Retry count {}".format(self.retry_counter))
                if e.errno:
                    time.sleep(2)
                self.create_ssh_client(hostname, username, password, port)
            self.msg = "연결 성공"
            self.connect_status = True

            if self.ssh_client.get_transport().is_active():
                tranport_info = self.ssh_client.get_transport()

                f = open("connection_test.txt", "w")
                f.write(
                    "Connection Success. IP: "
                    + ":".join(map(str, tranport_info.getpeername()))
                    + ", User Name: "
                    + tranport_info.get_username()
                    + "\n"
                )
                f.close()

                self.send_file(
                    "connection_test.txt", "/home/msol1/문서/bhmetal_machine_data"
                )
                os.remove("connection_test.txt")
        else:
            self.connect_status = False
            if self.ssh_client.get_transport():
                self.ssh_client.close_ssh_client()
            else:
                self.ssh_client = None
            print("SSH client session exist. Try again.")

    def close_ssh_client(self):
        """Close SSH client session"""
        self.ssh_client.close()

    def send_file(self, local_path, remote_path):
        """Send a single file to remote path"""
        try:
            with SCPClient(self.ssh_client.get_transport()) as scp:
                scp.put(local_path, remote_path, preserve_times=True)
        except SCPException:
            raise SCPException.message

    def get_file(self, remote_path, local_path):
        """Get a single file from remote path"""
        try:
            with SCPClient(self.ssh_client.get_transport()) as scp:
                scp.get(remote_path, local_path)
        except SCPException:
            raise SCPException.message

    def send_command(self, command):
        """Send a single command"""
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        return stdout.readlines()


class Handler(FileSystemEventHandler):
    def __init__(self, ssh_manager):
        self.ssh_manager = ssh_manager
        self.ui = None

    def set_ui(self, ui):
        self.ui = ui

    def on_created(self, event):
        self.ui.log_text.appendPlainText("Directory created: " + event.src_path)
        self.ssh_manager.send_file(
            event.src_path, "file_path"
        )  # replace file_path to actual file path.


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("IP_insert.ui", self)
        self.ssh_manager = None
        # self.ipCheck()
        self.setup_system_tray()

    def setup_system_tray(self):
        # Create a system tray icon
        self.tray_icon = QSystemTrayIcon(QIcon("Observe.ico"), self)

        # Create a context menu for the tray icon
        self.tray_menu = QMenu(self)

        # Add an action to show/hide the main window when tray icon is clicked
        show_hide_action = self.tray_menu.addAction("Show/Hide")
        show_hide_action.triggered.connect(self.toggle_main_window)

        # Add an action to quit the application when clicked on the tray icon
        quit_action = self.tray_menu.addAction("Quit")
        quit_action.triggered.connect(self.quit_application)

        # Set the context menu for the tray icon
        self.tray_icon.setContextMenu(self.tray_menu)

        # Show the tray icon
        self.tray_icon.show()

    def toggle_main_window(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()

    def quit_application(self):
        # Perform any cleanup or saving before quitting (if necessary)
        self.tray_icon.hide()
        QApplication.quit()

    def ipCheck(self):
        self.ssh_manager = SSHManager()
        [IP, PORT] = self.ui.IP_input.text().split(":")
        USER = self.ui.user.text()
        PWD = self.ui.pwd.text()
        PORT = 22 if PORT == None else PORT

        try:
            self.ssh_manager.create_ssh_client(IP, USER, PWD, PORT)
        except:
            self.ui.status_label.setText("연결 실패")
            self.ui.status_label.setStyleSheet("Color : red")
            return
        self.ui.status_label.setText(self.ssh_manager.msg)
        if self.ssh_manager.connect_status:
            self.ui.status_label.setStyleSheet("Color : green")
        else:
            self.ui.status_label.setStyleSheet("Color : red")
        self.ui.log_text.setPlainText("")
        time.sleep(0.5)
        self.changeUI()

    def changeUI(self):
        cur_index = self.tabWidget.currentIndex()
        self.ui.tabWidget.setCurrentIndex(cur_index + 1)

    def back(self):
        cur_index = self.tabWidget.currentIndex()
        self.ui.tabWidget.setCurrentIndex(cur_index - 1)

    def filePath(self):
        fpath = QFileDialog.getExistingDirectory(self, "Open path", "./")
        self.ui.file_path.setText(fpath)
        self.ui.log_text.setPlainText("")
        self.activateObserver()

    def activateObserver(self):
        path_to_monitor = (
            self.ui.file_path.text()
        )  # Change this to the directory you want to monitor
        event_handler = Handler(self.ssh_manager)
        event_handler.set_ui(self.ui)
        observer = Observer()
        observer.schedule(event_handler, path=path_to_monitor, recursive=True)
        observer.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())
