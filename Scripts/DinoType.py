class DinoType:
    def __init__(self):
        self.undefined, self.omnivore, self.herbivore, self.carnivore = 0, 1, 2, 3
        self.state = self.undefined

    def get_state(self):
        return self.state

    def set_state(self, new_type):
        self.state = new_type