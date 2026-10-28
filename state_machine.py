# 이벤트는 (종류, 값) 튜플이다.
#   ('INPUT', SDL 이벤트), ('TIME_OUT', None)

def time_out(e):
    return e[0] == 'TIME_OUT'


class StateMachine:
    def __init__(self, start_state, rules):
        self.cur_state = start_state
        self.rules = rules  # {상태: {이벤트 검사 함수: 다음 상태}}
        self.cur_state.enter()

    def update(self):
        self.cur_state.do()

    def draw(self):
        self.cur_state.draw()

    def handle_event(self, e):
        for check, next_state in self.rules[self.cur_state].items():
            if check(e):
                self.cur_state.exit()
                self.cur_state = next_state
                self.cur_state.enter()
                return
