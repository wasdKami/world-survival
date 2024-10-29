class DinoState:
    def __init__(self):
        self.wander, self.chase, self.run, self.sleep = 0, 1, 2, 3
        self.state = self.wander

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state