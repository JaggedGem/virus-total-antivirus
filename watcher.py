import time
import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json
import mimetypes
import requests
import queue
from threading import Thread
import sys

# Load the configuration data from the config.json file
with open("config.json", "r") as f:
    data = json.load(f)
    
# Paths to watch (Downloads and Desktop folders)
WATCH_PATHS = data["watch_paths"]

class FileEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        new_file_path = event.src_path
        if self.is_valid_file(new_file_path):
            try:
                print(f'New file created: {new_file_path}')
                self.file_queue.put(new_file_path)
                if self.file_queue.qsize() >= self.batch_size:
                    self.process_files()
            except Exception as e:
                print(f'Error while processing file: {str(e)}')
                sys.exit(1)
    def process_files(self):
        file_batch = []
        while not self.file_queue.empty():
            file_batch.append(self.file_queue.get())
        self.call_main(file_batch)

    def is_valid_file(self, file_path):
        try:
            if os.path.exists(file_path):
                if not file_path.endswith(('.tmp', '.crdownload')):
                    file_type = mimetypes.guess_type(file_path)[0]
                    if file_type is not None and 'text' in file_type:
                        file_size = os.path.getsize(file_path)
                        if file_size <= 5000000:  # 5MB
                            return True
                        else:
                            print(f'File {file_path} is too large. Skipping...')
                            return False
                    else:
                        print(f'File {file_path} is not a text file. Skipping...')
                        return False
                else:
                    return False
            else:
                return True
        except Exception as e:
            print(f'Error while validating file: {str(e)}')
            sys.exit(1)

    def call_main(self, file_batch):
        try:
            with requests.Session() as s:
                for file_path in file_batch:
                    subprocess.run(["python", "main.py", file_path, s])
        except Exception as e:
            print(f'Error while running subprocess: {str(e)}')
            sys.exit(1)


def start_file_watcher(paths):
    try:
        event_handler = FileEventHandler()
        observer = Observer()
        for path in paths:
            observer.schedule(event_handler, path, recursive=True)
            print(f'Watching folder: {path}')
        observer.start()
    except Exception as e:
        print(f'Error while starting file watcher: {str(e)}')
        sys.exit(1)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    try:
        print("Watching specified folders for new files...")
        start_file_watcher(WATCH_PATHS)
    except Exception as e:
        print(f'Error while watching specified folders: {str(e)}')
        sys.exit(1)
