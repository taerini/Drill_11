class StateMachine:
    def __init__(self, start_state):
        self.cur_state = start_state
        self.cur_state.enter()

    def update(self):
        self.cur_state.do()

    def draw(self):
        self.cur_state.draw()
