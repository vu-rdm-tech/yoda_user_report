import logging
from datetime import datetime

def get_logger():
    LOGFILE = f"./log/datamamager-report_{datetime.now().strftime('%Y%m%d')}.log"
    logger = logging.getLogger('yoda_datamanager_report')
    logger.propagate = False
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr = logging.FileHandler(LOGFILE)
    hdlr.setFormatter(formatter)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(hdlr)
        logger.addHandler(ch)
    return logger

logger = get_logger()

