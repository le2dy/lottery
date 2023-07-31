import sys
import time
import paramiko
from scp import SCPClient, SCPException
from PyQt5.QtWidgets import *
from PyQt5 import uic
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class SSHManager:
    def __init__(self) -> None:
        self.ssh_client = None
    
    def create_ssh_client(self, hostname, username, password, port):
        if self.ssh_client is None:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(hostname, username=username, password=password,port=port)
            self.msg = "연결 성공"
            self.connect_status = True
        else: 
            self.connect_status = False
            self.ssh_client.close_ssh_client()
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
    def on_created(self, event):
        self.ui.log_text.append('Directory created: ' + event.src_path)
        self.ssh_manager.send_file(event.src_path, file_path)  # replace file_path to actual file path.


class MainWindow(QMainWindow):
    global ssh_manager
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("IP_insert.ui", self)

    def ipCheck(self):
        ssh_manager = SSHManager()
        [IP, PORT] = self.ui.IP_input.text().split(':')
        USER = self.ui.user.text()
        PWD = self.ui.pwd.text()
        PORT = 22 if PORT == None else PORT
        try:
            ssh_manager.create_ssh_client(IP, USER, PWD, PORT)
        except Exception:
            self.ui.status_label.setText("연결 실패")
            self.ui.status_label.setStyleSheet("Color : red")
            return
        self.ui.status_label.setText(ssh_manager.msg)
        if ssh_manager.connect_status:
            self.ui.status_label.setStyleSheet("Color : green")
        else:
            self.ui.status_label.setStyleSheet("Color : red")
        time.sleep(.5)
        self.changeUI()

    def changeUI(self):
        cur_index = self.tabWidget.currentIndex()
        self.ui.tabWidget.setCurrentIndex(cur_index + 1)
    
    def back(self):
        cur_index = self.tabWidget.currentIndex()
        self.ui.tabWidget.setCurrentIndex(cur_index - 1)

    def filePath(self):
        fpath = QFileDialog.getExistingDirectory(self, "Open path", './')
        self.ui.file_path.setText(fpath)
        self.ui.log_text.setText('')
        self.activateObserver()

    def activateObserver(self):
        path_to_monitor = self.ui.file_path.text()  # Change this to the directory you want to monitor
        event_handler = Handler()
        observer = Observer()
        observer.schedule(event_handler, path=path_to_monitor, recursive=True)
        observer.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())