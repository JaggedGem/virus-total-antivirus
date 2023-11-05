import logger
import time
       
def reader(file_report_data):
    try:
        if file_report_data and \
           file_report_data.get('data') and \
           file_report_data.get('data').get('attributes') and \
           file_report_data.get('data').get('attributes').get('status') == 'queued':
            logger.my_logger.warn(f'File queued for analysis(external)')
            print('File queued for analysis, please wait...')
            time.sleep(10)
            return 'queued'

        # Extract the items
        data = file_report_data.get('data') if file_report_data else None
        attributes = data.get('attributes') if data else None
        last_analysis_stats = attributes.get('last_analysis_stats') if attributes else None

        detections = last_analysis_stats.get('malicious') if last_analysis_stats else None
        undetected = last_analysis_stats.get('undetected') if last_analysis_stats else None

        if detections is not None and undetected is not None:
            total = detections + undetected
            logger.my_logger.info(f'JSON file read successfully(external)')
            return (detections, total)
        else:
            return None
    except Exception as e:
        logger.my_logger.critical(f'Error while reading JSON file: {str(e)}')
        print(f'Error while reading JSON file: {str(e)}')
        return None
    