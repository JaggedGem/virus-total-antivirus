import logger
import requests
import hash_calculator
import sys
import tkinter as tk
import os
import time
import json_reader
import inspect
import subprocess

# Define the VirusTotal API key
api_key = "Your API Key" # api_key

# Define the headers for the request
headers = {"x-apikey": api_key}


def handle_report(file_report_data, file_path):
    
    # Get the current frame
    current_frame = inspect.currentframe()
    # Get the outer frame (the caller's frame)
    outer_frame = inspect.getouterframes(current_frame, 2)
    # Get the name of the calling function
    caller_name = outer_frame[1][3]
    
    if file_report_data.status_code == 200:
        if caller_name == 'upload_file_smaller_32':
            logger.my_logger.info("Got report(<32 MB)")
        else:
            logger.my_logger.info("Got report(>32 MB)")
            
            
        file_report_data = file_report_data.json()
        file_name = os.path.basename(file_path)
        analysis_report_data = json_reader.reader(file_report_data)

        if analysis_report_data is None:
            sys.exit(1)
            
        elif analysis_report_data == 'queued':
            if caller_name == 'upload_file_smaller_32':
                upload_file_smaller_32(file_path)
            else:
                upload_file_bigger_32(file_path)
            
        else:
            detections, total = analysis_report_data
        return (file_name, detections, total)
    else:
        logger.my_logger.error("Could not get the analysis report")
        print("Could not get the analysis report")
        sys.exit(1)

        
# Define a function to get the file report by hash
def get_file_report_by_hash(file_hash, file_path):
    if file_hash is None:
        return None
    else:
        # Define the VirusTotal API endpoint for file report
        file_report_url = "https://www.virustotal.com/api/v3/files/" + file_hash

        # Define the headers for the request
        headers = {"x-apikey": api_key}

        # Send a GET request to the file report endpoint
        file_report_response = requests.get(file_report_url, headers=headers)

        # Check the status code of the response
        if file_report_response.status_code == 200:
            logger.my_logger.info("File hash report found")
            # The file report was found
            # Parse the JSON response
            file_report_data = file_report_response.json()
            # Get the file name from the response
            # print(file_report_data)
            # file_name = file_report_data["data"]["attributes"]["names"][0]
            file_name = os.path.basename(file_path)

            analysis_report_data = json_reader.reader(file_report_data)
            if analysis_report_data is None:
                logger.my_logger.critical("Could not get the analysis report")
                print("Could not get the analysis report")
                sys.exit(1)
            
            elif analysis_report_data == 'queued':
                get_file_report_by_hash(file_hash, file_path)

            else:
                detections, total = analysis_report_data
            
            
            # Return the file name, detections and total as a tuple
            return (file_name, detections, total)
        elif file_report_response.status_code == 404:
            # The file report was not found
            return None
        else:
            # The file report request failed or there was an error
            logger.my_logger.error("Could not get the file report")
            print("Could not get the file report")
            subprocess.Popen(["python", "main copy 2.py"])
            sys.exit(1)

# Define a function to upload a file and get the analysis report by ID
def upload_file_smaller_32(file_path):

    # Get the file size in bytes
    file_size = os.path.getsize(file_path)

    if file_size <= 32 * 1024 * 1024:
        logger.my_logger.info("Uploading file(<32 MB)")
        # The file size is less than or equal to 32 MB
        # Define the VirusTotal API endpoint for file upload
        file_upload_url = "https://www.virustotal.com/api/v3/files"
        # Define the files for the request
        files = {"file": (file_path, open(file_path, "rb"))}
        # Send a POST request to the file upload endpoint
        file_upload_response = requests.post(file_upload_url, headers=headers, files=files)
        # Check the status code of the response
        file_report_data = file_upload_response
        handled_data = handle_report(file_report_data, file_path)
        
        return handled_data
    
    elif file_size <= 650 * 1024 * 1024:
        upload_file_bigger_32(file_path)
    else:
        # The file size is greater than 650 MB
        logger.my_logger.error("The file is too large to be uploaded to VirusTotal")
        print("The file is too large to be uploaded to VirusTotal")
        sys.exit(1)
        
        
def upload_file_bigger_32(file_path):
    logger.my_logger.info("Getting upload URL(>32 MB)")
    # The file size is greater than 32 MB and less than or equal to 650 MB
    # Define the VirusTotal API endpoint for upload URL request
    upload_url_request_url = "https://www.virustotal.com/api/v3/files/upload_url"
    # Send a GET request to the upload URL request endpoint
    upload_url_request_response = requests.get(upload_url_request_url, headers=headers)
    # Check the status code of the response
    if upload_url_request_response.status_code == 200:
        logger.my_logger.info("Got upload URL(>32 MB)")
        # The upload URL request was successful
        # Parse the JSON response 
        upload_url_request_data = upload_url_request_response.json()
        # Get the upload URL from the response
        upload_url = upload_url_request_data["data"]
        # Define the files for the request
        files = {"file": (file_path, open(file_path, "rb"))}
        # Send a POST request to the upload URL
        upload_url_response = requests.post(upload_url, headers=headers, files=files)
        # Check the status code of the response
        if upload_url_response.status_code == 200:
            logger.my_logger.info("Uploaded file(>32 MB)")
            # The file upload was successful
            # Parse the JSON response
            upload_url_data = upload_url_response.json()
            # Get the analysis ID from the response
            analysis_id = upload_url_data.get("data").get("id")
            # Define the VirusTotal API endpoint for analysis report
            analysis_report_url = "https://www.virustotal.com/api/v3/analyses/" + analysis_id
            
            # Wait for some time for the analysis to complete
            time.sleep(20)
            
            # Send a GET request to the analysis report endpoint
            file_report_data = requests.get(analysis_report_url, headers=headers)
            # Check the status code of the response
            handled_data = handle_report(file_report_data, file_path)
            return handled_data
        
        else:
            # The file upload failed or there was an error
            logger.my_logger.error("Could not upload the file")
            print("Could not upload the file")
            sys.exit(1)
    else:
        # The upload URL request failed or there was an error
        logger.my_logger.error("Could not get the upload URL")
        print("Could not get the upload URL")
        sys.exit(1)

# Define a function to delete the file and exit the program
def delete_file(file_path):
    try:
        os.remove(file_path)
        logger.my_logger.info(f"Deleted {file_path}")
        print(f"Deleted {file_path}")
    except OSError as e:
        logger.my_logger.critical(f"Could not delete {file_path}: {e}")
        print(f"Could not delete {file_path}: {e}")
    finally:
        sys.exit(0)

# Define a function to exit the program without deleting the file
def exit_program():
    logger.my_logger.info("Exiting program")
    sys.exit(0)

# Define a function to create a window to display the virus report and the options
def create_window(file_path, file_name, detections, total):
    # Create a tkinter window to display the virus report and the options
    window = tk.Tk()
    window.title("Virus Report")
    window.geometry("300x200")

    # Create a label to show the file name and the virus report
    label = tk.Label(window, text=f"{file_name}: {detections}/{total}", font=("Arial", 16))
    label.pack(pady=20)

    # Create a button to delete the file and exit the program
    delete_button = tk.Button(window, text="Delete File", command=lambda: delete_file(file_path), bg="red", fg="white")
    delete_button.pack(pady=10)

    # Create a button to exit the program without deleting the file
    exit_button = tk.Button(window, text="Exit Program", command=exit_program, bg="green", fg="white")
    exit_button.pack(pady=10)

    # Start the window main loop
    window.mainloop()
        
        
def main(file_path):
    
    file_hash = hash_calculator.calculate_hash(file_path)

    if file_hash is None:
        sys.exit(1)
        
        
    # Try to get the file report by hash
    file_report = get_file_report_by_hash(file_hash, file_path)

    # Check if the file report was found
    if file_report is not None:
        # Unpack the file report tuple
        file_name, detections, total = file_report
    else:
        # Retry opening the file a few times with a delay between each attempt
        for _ in range(5):  # Retry 5 times
            try:
                # Try to upload the file and get the analysis report by ID
                analysis_report = upload_file_smaller_32(file_path)
                break
            except FileNotFoundError:
                time.sleep(1)  # Wait for 1 second before retrying
        else:
            print(f'File {file_path} does not exist.')
            return

        # Check if the analysis report was found
        if analysis_report is not None:
            # Unpack the analysis report tuple
            file_name, detections, total, *_ = analysis_report
        else:
            # No report was found or there was an error
            logger.my_logger.error("Could not get any report")
            print("Could not get any report")
            sys.exit(1)

    # Create a window to display the virus report and the options
    if int(detections) > 0:
        create_window(file_path, file_name=file_name, detections=detections, total=total)
    else:
        logger.my_logger.info("No virus was detected")
        print("No virus was detected")
        sys.exit(0)
        
        
        
        
if __name__ == "__main__":
    file_path = "E:\\Downloads\\1wWJvm"
    main(file_path)