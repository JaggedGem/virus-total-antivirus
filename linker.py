import os
import json
import tkinter as tk
from tkinter import Entry, Label, Button, messagebox
import sys

# Function to save the API key and watch paths to config.json
def save_settings():
    api_key = api_key_entry.get()
    watch_paths = watch_paths_entry.get().split('\n')

    if not api_key or not watch_paths:
        messagebox.showerror("Error", "API Key and Watch Paths are required")
        return

    config_data = {
        "api_key": api_key,
        "watch_paths": watch_paths
    }

    with open("config.json", "w") as config_file:
        json.dump(config_data, config_file, indent=4)
    
    settings_window.destroy()

# Function to start monitoring
def start_monitoring():
    if not os.path.exists("config.json"):
        messagebox.showerror("Error", "Config file not found. Please configure settings first.")
        return
    print("Starting monitoring...")

# Check if config.json is properly configured
if not os.path.exists("config.json"):
    settings_window = tk.Tk()
    settings_window.title("Settings")
    
    api_key_label = Label(settings_window, text="VirusTotal API Key:")
    api_key_label.pack(pady=10)
    api_key_entry = Entry(settings_window)
    api_key_entry.pack(pady=5)
    
    watch_paths_label = Label(settings_window, text="Watch Paths (one per line):")
    watch_paths_label.pack(pady=10)
    watch_paths_entry = Entry(settings_window, text="")
    watch_paths_entry.pack(pady=5)

    save_button = Button(settings_window, text="Save Settings", command=save_settings)
    save_button.pack(pady=10)

    settings_window.mainloop()
else:
    start_monitoring()
