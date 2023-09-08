from datetime import datetime
from .colour import Colour

def error_handler(error_count, status_log, interval):
    if (status_log != None and error_count == 0):
        return 0
    elif (status_log != None and error_count > 0):
        print(f"{Colour().success}Connection reestablished. Total time disconnected: {error_count * interval} seconds{Colour().default}")
        return 0
    elif (status_log == None and error_count < 3):
        print(f"{Colour().error} Error making HTTP request at {datetime.now().strftime('%D  %H:%M:%S')} {Colour().default}")
        return error_count + 1
    elif (status_log == None and error_count == 3):
        print(f"{Colour().error} Connection error persisting... Check connection {Colour().default}")
        return error_count + 1
    else:
        return error_count + 1
