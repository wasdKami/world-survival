class DinoEmotion:
    def __init__(self):
        self.happy, self.scared, self.sad, self.angry = 0, 1, 2, 3
        self.state = self.happy

    def get_state(self):
        return self.state

    def set_state(self, new_emotion):
        self.state = new_emotion