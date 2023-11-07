# Automatic Virus Detection and Cleanup

This Python project automates the detection of new files in the specified folders, leveraging VirusTotal's V3 API to check for potential viruses. When a new file is detected and a virus is found, a pop-up window displays the file name, the number of detections out of the total number of scanners, and provides options to either delete the file or leave it.

## Features

- Monitors the selected folders for new files.
- Utilizes VirusTotal's V3 API for virus scanning.
- Presents a pop-up window upon virus detection, showing file information.
- Allows users to choose whether to delete or keep the infected file.

## Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/JaggedGem/virus-total-antivirus.git
cd virus-total-antivirus
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the Python script:

```bash
python linker.py
```

2. The program will automatically monitor the folders specified in the `config.json` file for new files and perform virus scans using the VirusTotal API.

3. If a virus is detected, a pop-up window will display the file name, number of detections, and options to delete or leave the file.
   - [x] Allow users to easily input file paths and view scan results.

- [x] **Refactor Code for Modularity:**
   - [x] Refactor the code to improve modularity and reusability.
   - [x] Split functions into separate modules for better organization.

- [x] **Optimize API Requests:**
   - [x] Optimize API requests for faster scanning.
   - [x] Implement batch processing for multiple files.

- [x] **Improve Error Handling:**
   - [x] Enhance error handling and provide clearer error messages for users.

- [x] **Expand Documentation:**
## Configuration

- The `config.json` file should contain your [VirusTotal API Key](https://www.virustotal.com/gui/my-apikey) and the paths you want the script to watch for new files. Here is an example of how the `config.json` file should look:
