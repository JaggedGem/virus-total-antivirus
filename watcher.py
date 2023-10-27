import time
import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json

# Load the configuration data from the config.json file
with open("config.json", "r") as f:
    data = json.load(f)
    
# Paths to watch (Downloads and Desktop folders)
PATHS_TO_WATCH = ["path_to_downloads_folder", "path_to_desktop_folder"]
PATHS_TO_WATCH = data["watch_paths"]

class FileEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        new_file_path = event.src_path
        if self.check_file_validity(new_file_path):
        self.execute_main_script(new_file_path)
            print(f'File modified: {new_file_path}')
            self.call_main(new_file_path)

    def execute_main_script(self, file_path):
    def check_file_validity(self, file_path):
        subprocess.run(["python", "main.py", file_path])

    def is_valid_file(self, file_path):
        if os.path.exists(file_path):
            if not file_path.endswith(('.tmp', '.crdownload', '.part')):
                return True
            else:
                return False
        else:
            return True

    def call_main(self, file_path):
        subprocess.run(["python", "main.py", file_path])


def initiate_file_watcher(paths):
initiate_file_watcher(PATHS_TO_WATCH)
    def test_file_watcher_functionality():
    test_file_watcher_functionality()
