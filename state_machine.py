from pico2d import SDL_KEYDOWN, SDLK_SPACE


# 이벤트는 (종류, 값) 튜플이다.
#   ('INPUT', SDL 이벤트), ('DIR', 방향키 합), ('TIME_OUT', None)

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def time_out(e):
    return e[0] == 'TIME_OUT'


def move_start(e):
    return e[0] == 'DIR' and e[1] != 0


def move_stop(e):
    return e[0] == 'DIR' and e[1] == 0


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
