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
WATCH_PATHS = ["path_to_downloads_folder", "path_to_desktop_folder"]
WATCH_PATHS = data["watch_paths"]

class FileEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        new_file_path = event.src_path
        if self.is_valid_file(new_file_path):
            print(f'File modified: {new_file_path}')
            self.call_main(new_file_path)

    def call_main(self, file_path):
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


def start_file_watcher(paths):
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
    start_file_watcher(WATCH_PATHS)
if __name__ == "__main__":
    print("Watching specified folders for new files...")
    start_file_watcher(WATCH_PATHS)

def test_file_watcher():
    # Create a test file
    with open("test_file.txt", "w") as f:
        f.write("This is a test file.")

    # Start a download (simulated by a delay)
    time.sleep(2)

    # Check that the file is correctly added to the list of files being watched
    assert "test_file.txt" in WATCH_PATHS

if __name__ == "__main__":
    print("Watching specified folders for new files...")
    start_file_watcher(WATCH_PATHS)
    test_file_watcher()
