import hashlib
import logger

def calculate_hash(file_path):
    try:
        logger.my_logger.info(f"Calculating hash of {file_path}")
        # Open the file in binary mode and calculate its hash
        with open(file_path, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        return file_hash
    except PermissionError:
        print(f'Permission denied: {file_path}')
        return None
    except Exception as e:
        print(f'Error while calculating hash for file {file_path}: {str(e)}')
        return None