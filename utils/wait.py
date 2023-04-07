from time import sleep

# Halts program for configured time before making another request
def wait(continue_condition, time):
    for timer in range(time):
        if continue_condition:
            sleep(1)
        else:
            break