import os
import platform
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logger
import sys
import re
import threading
from main import main
from queue import Queue
import mimetypes
import time
import hash_calculator


class FileEventHandler(FileSystemEventHandler):
    def __init__(self, batch_size):
        super().__init__()
        self.file_queue = Queue()
        self.batch_size = batch_size
        
    def on_created(self, event):
        new_file_path = event.src_path
        if self.is_valid_file(new_file_path):
            try:
                logger.my_logger.info(f'New file created: {new_file_path}')
                print(f'New file created: {new_file_path}')
                self.file_queue.put(new_file_path)
                self.process_files()
            except Exception as e:
                logger.my_logger.critical(f'Error while processing file: {str(e)}')
                print(f'Error while processing file: {str(e)}')
                sys.exit(1)
    
    def process_files(self):
        file_batch = []
        while not self.file_queue.empty():
            file_path = self.file_queue.get()
            # Sanitize file path
            file_path = re.sub(r'[<>"|?*]', '', file_path)
            file_batch.append(file_path)
        self.call_main(file_batch)

    def is_valid_file(self, file_path):
        try:
            if os.path.exists(file_path):
                if not file_path.endswith(('.tmp', '.crdownload')):
                    file_type = mimetypes.guess_type(file_path)[0]
                    file_size = os.path.getsize(file_path)
                    if file_size <= 650 * 1024 * 1024:  # 650MB
                        # Check if the file is still being written to
                        while True:
                            try:
                                with open(file_path, 'a') as file:
                                    break
                            except PermissionError:
                                time.sleep(1)  # wait for 1 second before trying again
                        return True
                    else:
                        logger.my_logger.warning(f'File {file_path} is too large. Skipping...')
                        print(f'File {file_path} is too large. Skipping...')
                        return False
                else:
                    return False
            else:
                return True
        except Exception as e:
            logger.my_logger.critical(f'Error while validating file: {str(e)}')
            print(f'Error while validating file: {str(e)}')
            sys.exit(1)
            

    def call_main(self, file_batch):
        semaphore = threading.Semaphore(self.batch_size)
        try:
            for file_path in file_batch:
                # Acquire the semaphore
                semaphore.acquire()
                file_hash = hash_calculator.calculate_hash(file_path)
                def run_and_release(file_path, file_hash):
                    try:
                        main(file_path=file_path, file_hash=file_hash)
                    finally:
                        # Release the semaphore when the function finishes
                        semaphore.release()
                thread = threading.Thread(target=run_and_release, args=(file_path,file_hash))
                thread.start()
        except Exception as e:
            logger.my_logger.critical(f'Error while running subprocess: {str(e)}')
            print(f'Error while running subprocess: {str(e)}')
            sys.exit(1)


def start_file_watcher(paths):
    try:
        event_handler = FileEventHandler(1)
        observer = Observer()
        os_name = platform.system()
        for path in paths:
            if os.path.exists(path):
                observer.schedule(event_handler, path, recursive=True)
                logger.my_logger.info(f'Watching folder: {path}')
                print(f'Watching folder: {path}')
            else:
                logger.my_logger.warning(f'Invalid path: {path}')
                print(f'Invalid path: {path}')
                sys.exit(1)
        observer.start()
    except Exception as e:
        logger.my_logger.critical(f'Error while starting file watcher: {str(e)}')
        print(f'Error while starting file watcher: {str(e)}')
        sys.exit(1)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

def main_watch(WATCH_PATHS):
    if __name__ == "__main__":
        try:
            logger.my_logger.info("Watching specified folders for new files...")
            print("Watching specified folders for new files...")
            start_file_watcher(WATCH_PATHS)
        except Exception as e:
            logger.my_logger.critical(f'Error while watching specified folders: {str(e)}')
            print(f'Error while watching specified folders: {str(e)}')
            sys.exit(1)
            
            
WATCH_PATHS = [
    "E:\\Downloads\\",
    "C:\\Users\\orlet\\OneDrive\\Desktop",
               ]
# handler = FileEventHandler(1)  # Set batch size to 10
main_watch(WATCH_PATHS)