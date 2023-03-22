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
        log_file.write("")
        log_file.close()

#turn off and on logger module.
def toggle_logger():
    global logger_is_on
    if (logger_is_on):
        logger_is_on = False
        print (f"{colour.red} Logger turned off.{colour.default}")
    else:
        logger_is_on = True
        print (f"{colour.green} logger turned on.{colour.default}")
    return
