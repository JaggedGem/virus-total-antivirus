# Automatic Virus Detection and Cleanup

This Python project automates the detection of new files in the Downloads and Desktop folders, leveraging VirusTotal's V3 API to check for potential viruses. When a new file is detected and a virus is found, a pop-up window displays the file name, the number of detections out of the total number of scanners, and provides options to either delete the file or leave it.

## Features

- Monitors the Downloads and Desktop folders for new files.
- Utilizes VirusTotal's V3 API for virus scanning.
- Presents a pop-up window upon virus detection, showing file information.
- Allows users to choose whether to delete or keep the infected file.

## Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/automatic-virus-detection.git](https://github.com/JaggedGem/virus-total-antivirus.git
cd virus-total-antivirus
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the Python script:

```bash
python watcher.py
```

2. The program will automatically monitor the Downloads and Desktop folders for new files and perform virus scans using the VirusTotal API.

3. If a virus is detected, a pop-up window will display the file name, number of detections, and options to delete or leave the file.

## Configuration

- Modify the file paths and other settings in the `config.json` file as needed to customize folder locations or adjust behavior.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow the [contributing guidelines](CONTRIBUTING.md).

## License

This project is licensed under the [MIT License](LICENSE).
