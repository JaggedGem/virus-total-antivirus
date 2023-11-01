import tkinter as tk
import subprocess

def run_watcher(file_paths):
    subprocess.run(["python", "watcher.py"] + file_paths)

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("VirusTotal File Watcher")
        self.geometry("500x300")
        self.file_paths_entry = tk.Entry(self)
        self.file_paths_entry.pack()
        self.start_button = tk.Button(self, text="Start Watching", command=self.start_watcher)
        self.start_button.pack()
        self.results_text = tk.Text(self)
        self.results_text.pack()

    def start_watcher(self):
        file_paths = self.file_paths_entry.get().split(',')
        run_watcher(file_paths)
        self.display_results()

    def display_results(self):
        with open("results.txt", "r") as f:
            results = f.read()
        self.results_text.insert(tk.END, results)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
