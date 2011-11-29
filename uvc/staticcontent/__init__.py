import logging
logger = logging.getLogger('uvc.staticcontent')

def log(message, summary='', severity=logging.INFO):
    logger.log(severity, '%s %s', summary, message)
