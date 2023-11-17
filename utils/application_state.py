from datetime import datetime
from .colour import Colour
import logging

class ApplicationState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ApplicationState, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        self.continuing = False
        self.currently_online = False
        self.target_reached = {}
        self.currently_online_list = {}
        self.error_count = 0

    def toggle_continue(self):
        if (self.continuing):
            self.continuing = False
        else:
            self.continuing = True

    def toggle_target_reached(self, server):
        if (self.target_reached[server]):
            self.target_reached[server] = False
        else:
            self.target_reached[server] = True

    def append_current_list(self, server, player):
        self.currently_online_list[server].append(player)

    def remove_current_list(self, server, player):
        self.currently_online_list[server].remove(player)

    def reset_current_list(self, server):
        self.currently_online_list[server] = []

    def delete_current_list(self, server):
        del self.currently_online_list[server]

    def add_current_list(self, server):
        self.currently_online_list[server] = []

    def error_handler(self, status_log, interval):
        if (status_log != None and self.error_count == 0):
            self.error_count = 0
        elif (status_log != None and self.error_count > 0):
            print(f"{Colour().success}Connection reestablished. Total time disconnected: {self.error_count * interval} seconds{Colour().default}")
            logging.info(f"{Colour().success}Connection reestablished. Total time disconnected: {self.error_count * interval} seconds{Colour().default}")
            self.error_count = 0
        elif (status_log == None and self.error_count < 3):
            logging.error(f"{Colour().error} Error making HTTP request at {datetime.now().strftime('%D  %H:%M:%S')} {Colour().default}")
            self.error_count += 1
        elif (status_log == None and self.error_count == 3):
            logging.error(f"{Colour().error} Connection error persisting... Check connection {Colour().default}")
            self.error_count += 1
        else:
            self.error_count += 1
