import logger
import time


def reader(file_report_data):
    try:
        file_report_data = file_report_data.json()
        data = file_report_data.get('data', {})
        attributes = data.get('attributes', {})
        last_analysis_stats = attributes.get('last_analysis_stats', {})

        detections = last_analysis_stats.get('malicious')
        undetected = last_analysis_stats.get('undetected')
        status = attributes.get('status')
        
        
        if (status == 'queued' or status is None) and \
        (detections is None or detections == 0) and \
        (undetected is None or undetected == 0):
            logger.my_logger.warning('File queued for analysis(external)')
            print('File queued for analysis, please wait...')
            return 'queued'

        if detections is not None and undetected is not None and (status is None or status == 'completed'):
            total = detections + undetected
            logger.my_logger.info('JSON file read successfully(external)')
            print((detections, total))
            return (detections, total)
        else:
            logger.my_logger.warning('File queued for analysis(external)')
            print('File queued for analysis, please wait...')
            return 'queued'
    except Exception as e:
        logger.my_logger.critical(f'Error while reading JSON file: {str(e)}')
        print(f'Error while reading JSON file: {str(e)}')
        return None
    