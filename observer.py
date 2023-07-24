import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pymssql
import pandas as pd
import psutil
import os

class Watcher:
    DIRECTORY_TO_WATCH = "/var/opt/mssql/csv"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(
            event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print("Received created event - %s." % event.src_path)
            file_name = event.src_path.split('/')[-1]

            if file_name == "stop_process":
              stop_process()

            insertToMSSQL(event.src_path)

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print("Received modified event - %s." % event.src_path)

def stop_process():
  for proc in psutil.process_iter():
    if proc.name() == "python3":
      proc.kill()
      os.remove('/var/opt/mssql/csv/stop_process')
      print(f"Stopped process: {proc.name()}")

def insertToMSSQL(f):
    data = pd.read_csv(f)
    df = pd.DataFrame(data)

    conn = pymssql.connect(host=r"(local)", database="smartfactory", charset="utf8", port=6001, user="sa", password="rkskekfk1!")

    cursor = conn.cursor()

    # cursor.execute("select * from sf_business;")
    query = "insert into sf_testest(name) values(%s);"
    cursor.executemany(query, df["name"])
    conn.commit()

    # print(cursor.fetchone())

    cursor.close()
    conn.close()

if __name__ == '__main__':
    w = Watcher()
    w.run()
