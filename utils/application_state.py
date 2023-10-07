class ApplicationState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ApplicationState, cls).__new__(cls)
            cls._instance.initialize()
        return cls

    def initialize(self):
        self.continuing = False
        self.currently_online = False
        self.target_reached = {}
        self.currently_online_list = {}

    def toggle_continue(self):
        if (self.continuing):
            self.continuing = False
        else:
            self.continuing = True

    def toggle_currently_online(self):
        if (self.currently_online):
            self.currently_online = False
        else:
            self.currently_online = True

    def toggle_target_reached(self, server):
        if (self.target_reached[server]):
            self.target_reached[server] = False
        else:
            self.target_reached[server] = True

    def append_current_list(self, server, player):
        self.currently_online_list[server].append(player)

    def remove_current_list(self, server, player):
        self.currently_online_list[server].remove(player)
