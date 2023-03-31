from checker import checker
from .logger import logger
from time import sleep

# Halts program for configured time before making another request
def wait():
    global continue_condition
    for timer in range(config.interval):
        if continue_condition:
            sleep(1)
        else:
            break

# iterative function, continues if user has not stopped
def looper():
    global config
    global continue_condition
    global logger_is_on
    while continue_condition:
        config.load_config()
        status_log = checker()
        for each_status in status_log:
            print(each_status)
            if (logger_is_on):
                logger(each_status)
        wait()