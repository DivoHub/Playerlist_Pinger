from time import sleep

# Halts program for configured time before making another request
def wait(continue_condition, config):
    for timer in range(config.interval):
        if continue_condition:
            sleep(1)
        else:
            break