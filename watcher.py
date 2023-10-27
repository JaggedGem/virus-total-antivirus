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
DIRECTORIES_TO_MONITOR = ["path_to_downloads_folder", "path_to_desktop_folder"]
DIRECTORIES_TO_MONITOR = data["watch_paths"]

class FileEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        new_file_path = event.src_path
        if self.check_file_validity(new_file_path):
            print(f'File modified: {new_file_path}')
            self.execute_main_script(new_file_path)

    def execute_main_script(self, file_path):
        subprocess.run(["python", "main.py", file_path])

    def check_file_validity(self, file_path):
        if os.path.exists(file_path):
            if not file_path.endswith(('.tmp', '.crdownload', '.part')):
                return True
            else:
                return False
        else:
            return True

    def call_main(self, file_path):
        subprocess.run(["python", "main.py", file_path])

def initialize_file_monitoring(paths):
    event_handler = FileEventHandler()
    observer = Observer()
    for path in paths:
        observer.schedule(event_handler, path, recursive=True)
        print(f'Watching folder: {path}')
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    print("Watching specified folders for new files...")
    initialize_file_monitoring(DIRECTORIES_TO_MONITOR)
if __name__ == "__main__":
    print("Watching specified folders for new files...")
    start_file_watcher(WATCH_PATHS)

def test_file_monitoring():
    # Start a download (simulated by a delay)
    time.sleep(2)

    # Create a mock file event
    mock_event = FileSystemEvent("mock_file.txt")
    event_handler = FileEventHandler()
    
    # Check if the system responds correctly to the mock event
    assert event_handler.on_modified(mock_event) is None

if __name__ == "__main__":
    print("Watching specified folders for new files...")
    initialize_file_monitoring(DIRECTORIES_TO_MONITOR)
    test_file_monitoring()
