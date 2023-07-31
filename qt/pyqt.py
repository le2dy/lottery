import sys
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
        else: 
            print("SSH client session exist.")

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

# class Handler(FileSystemEventHandler):
#     def on_modified(self, event):
#         label.setText('Directory modified: ' + event.src_path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("parser/qt/IP_insert.ui", self)

    def ipCheck(self):
        ssh_manager = SSHManager()
        [IP, PORT] = self.ui.IP_input.text().split(':')
        ssh_manager.create_ssh_client(IP,'msol1','rkskekfk',PORT)
        self.ui.label.status_label.setText(ssh_manager.msg)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()

    path_to_monitor = '/home/leedongyun/Documents/연차/테스트/'  # Change this to the directory you want to monitor
    # event_handler = Handler()
    # observer = Observer()
    # observer.schedule(event_handler, path=path_to_monitor, recursive=True)
    # observer.start()

    sys.exit(app.exec_())
