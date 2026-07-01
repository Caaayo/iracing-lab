import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

DOWNLOADS_DIR = os.path.expanduser("~/Downloads")
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "cache")

class ResultHandler(FileSystemEventHandler):
    def on_created(self, event):

        if event.is_directory:
            return 

        filename = os.path.basename(event.src_path)

        if filename.startswith("eventresult-") and filename.endswith(".json"):
            time.sleep(1)
            new_path = os.path.join(CACHE_DIR, f"iracing-{filename}")
            shutil.move(event.src_path, new_path)
            print(f"Moved {filename} -> data/cache/iracing-{filename}")
        
def process_existing():
    for filename in os.listdir(DOWNLOADS_DIR):
        if filename.startswith("eventresult-") and filename.endswith(".json"):
            new_path = os.path.join(CACHE_DIR, f"iracing-{filename}")

            # Skip if it exists in cache/
            if os.path.exists(new_path):
                print(f"Already exists, skipping: iracing-{filename}")
                continue

            if ' (' in filename:
                print(f"Skipping duplicate: {filename}")
                continue

            src_path = os.path.join(DOWNLOADS_DIR, filename)
            shutil.move(src_path, new_path)
            print(f"Moved {filename} -> data/cache/iracing-{filename}")

if __name__ == "__main__":
    print(f"Watching {DOWNLOADS_DIR} for new and existing iRacing result exports...")
    process_existing()
    observer = Observer()
    observer.schedule(ResultHandler(), DOWNLOADS_DIR, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
