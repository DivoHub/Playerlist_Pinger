from .colour import Colour
import logging


#appends each status into log file in local folder. Creates log file if none exists
def logger(status_string):
    try:
        log_file = open('log.txt', 'a')
    except FileNotFoundError:
        log_file = open('log.txt', 'x')
    finally:
        log_file.write(status_string + "\n")
        log_file.close()

#reintiates another log file
def refresh_log():
    try:
        log_file = open('log.txt', 'w')
    except FileNotFoundError:
        log_file = open('log.txt', 'x')
    finally:
        print ("Starting new log file...")
        log_file.write("")
        log_file.close()
        print ("Success!")

def log_and_print(message, severity_level):
    logging.basicConfig(filename='errors.log', level=logging.ERROR)

    logging_levels = {
        1: logging.DEBUG,
        2: logging.INFO,
        3: logging.WARNING,
        4: logging.ERROR,
        5: logging.CRITICAL
    }

    print(message)
    if severity_level >= 4:
        logging.log(logging_levels[severity_level], message)