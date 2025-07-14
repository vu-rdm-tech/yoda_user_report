import logging
from datetime import datetime


def get_logger():
    """
    Initialize and configure the logger for the Yoda user & datamanager report.
    
    This function sets up logging with a file handler and a stream handler. It configures the log level to INFO and the log format. It returns the configured logger object.
    
    :return: logger object configured with file and stream handlers
    """
    LOGFILE = f"./log/user-report_{datetime.now().strftime('%Y%m%d')}.log"
    logger = logging.getLogger("yoda_user_report")
    logger.propagate = False
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    hdlr = logging.FileHandler(LOGFILE)
    hdlr.setFormatter(formatter)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(hdlr)
        logger.addHandler(ch)
    return logger


logger = get_logger()
