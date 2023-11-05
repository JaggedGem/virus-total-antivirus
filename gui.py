import tkinter as tk
import os
import watcher
import main

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("VirusTotal File Watcher")
        self.geometry("800x600")

        self.file_paths_label = tk.Label(self, text="Enter file paths (comma-separated):")
        self.file_paths_label.grid(row=0, column=0, padx=10, pady=10)

        self.file_paths_entry = tk.Entry(self)
        self.file_paths_entry.grid(row=0, column=1, padx=10, pady=10)

        self.api_key_label = tk.Label(self, text="Enter API key:")
        self.api_key_label.grid(row=1, column=0, padx=10, pady=10)

        self.api_key_entry = tk.Entry(self)
        self.api_key_entry.grid(row=1, column=1, padx=10, pady=10)

        self.start_button = tk.Button(self, text="Start Watching", command=self.start_watcher)
        self.start_button.grid(row=2, column=0, padx=10, pady=10)

        self.status_label = tk.Label(self, text="Status: Not running", font=("Arial", 16))
        self.status_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.results_text = tk.Text(self)
        self.results_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.scrollbar = tk.Scrollbar(self, command=self.results_text.yview)
        self.scrollbar.grid(row=4, column=2, sticky='nsew')

        self.results_text['yscrollcommand'] = self.scrollbar.set

        self.watcher = None

    def start_watcher(self):
        file_paths = self.file_paths_entry.get().split(',')
        api_key = self.api_key_entry.get()

        # Validate API key and file paths
        if not self.validate_inputs(api_key, file_paths):
            self.status_label.config(text="Status: Invalid inputs")
            return

        # Initialize the watcher but don't start it yet
        self.watcher = watcher.Watcher(api_key, file_paths, self.run_main_script)
        self.status_label.config(text="Status: Ready")
        self.start_button.config(state="normal")

    def run_main_script(self, file_path):
        # Run the main script with the given file path
        main.main(file_path)

    def validate_inputs(self, api_key, file_paths):
        # Send a test request to the VirusTotal API
        if not main.test_api_key(api_key):
            return False

        # Check if the file paths exist
        for path in file_paths:
            if not os.path.exists(path):
                return False

        return True

    def display_results(self):
        # Open a new GUI window to display the output of the watcher
        output_window = tk.Toplevel(self)
        output_window.geometry("800x600")

        output_text = tk.Text(output_window)
        output_text.pack()

        start_stop_button = tk.Button(output_window, text="Start/Stop", command=self.toggle_watcher)
        start_stop_button.pack()

        back_button = tk.Button(output_window, text="Back", command=output_window.destroy)
        back_button.pack()

        # Update the output text with the results from the watcher
        output_text.insert(tk.END, self.watcher.get_results())

    def toggle_watcher(self):
        if self.watcher.is_running():
            self.watcher.stop()
            self.start_button.config(state="normal")
        else:
            self.watcher.start()
            self.start_button.config(state="disabled")

if __name__ == "__main__":
    app = Application()
    app.mainloop()