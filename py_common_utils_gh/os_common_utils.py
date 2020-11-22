import logging
import sys

default_log_formatter = logging.Formatter("[%(asctime)s] %(levelname)s | %(module)s:%(lineno)s | %(funcName)s | %(message)s")


def setup_logger(name, log_file_path, duplicate_to_stdout=False, formatter = default_log_formatter, level=logging.INFO):
    """[summary]

    Args:
        name (str): name of the logger
        log_file_path (str) absolute file path where the logger will output
        duplicate_to_stdout (boolean) indicates whether the log message will be sent to the standard output in addition to the log file
        formatter (logging.Formatter, optional): Optional format for the logs. Defaults to default_log_formatter.
        level (int, optional): logging level filter. Defaults to logging.INFO.

    Raises:
        ValueError: name has to be specified.
        ValueError: cannot setup a logger that already exists. Instead retreive it from the logging manager and modify it.

    Returns:
        [logging.Logger]: the created logger
    """

    if name is None:
        raise ValueError("name parameter must be specified.")

    #logger already exists and setup called, reset it
    if name in logging.Logger.manager.loggerDict:
        logger = logging.getLogger(name)
        while logger.hasHandlers() and len(logger.handlers) > 0:
            logger.removeHandler(logger.handlers[0])

    handler = logging.FileHandler(log_file_path)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    
    if duplicate_to_stdout:
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(formatter)
        logger.addHandler(logging.StreamHandler(sys.stdout))

    return logger


    
if __name__ == "__main__":
    try:
        logger = setup_logger(None, '/home/ghelie/fin_app_logs')
        logger.info("Info")
        logger.error("Err")
        logger.critical("Critical")
    except ValueError as val_err: 
        print(str(val_err))
    
    logger = setup_logger('logger_1', '/home/ghelie/fin_app_logs')
    logger.info("Info")
    logger.error("Err")
    logger.critical("Critical")

    logger = setup_logger('logger_1', '/home/ghelie/fin_app_logs', True)
    logger.info("Info")
    logger.error("Err")
    logger.critical("Critical")

    print(logging.Logger.manager.loggerDict)

    try:
       logger = setup_logger('logger_1', '/home/ghelie/fin_app_logs') 
    except ValueError as val_err:
        print(str(val_err))

    logger2 = logging.getLogger('logger_1')
    print(logger is logger2)
    logger2.info("Info2")
    logger2.error("Err2")
    logger2.critical("Critical2")

    formatter = logging.Formatter("%(message)s")
    logger3 = setup_logger('logger_2', '/home/ghelie/fin_app_logs2', formatter, logging.CRITICAL)
    logger3.info("Info3")
    logger3.error("Err3")
    logger3.critical("Critical3")

    logger4 = logging.getLogger('logger_2')
    print(logger4 is logger3)
    print(logger4 is logger2)
    logger4.info("Info2")
    logger4.error("Err2")
    logger4.critical("Critical4")
