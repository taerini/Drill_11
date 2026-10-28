from pico2d import load_image, get_time

from state_machine import StateMachine, time_out


class Idle:
    def __init__(self, boy):
        self.boy = boy

    def enter(self):
        self.boy.frame = 0
        self.start_time = get_time()

    def exit(self):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8
        if get_time() - self.start_time > 5:
            self.boy.state_machine.handle_event(('TIME_OUT', None))

    def draw(self):
        row = 300 if self.boy.face_dir == 1 else 200
        self.boy.image.clip_draw(self.boy.frame * 100, row, 100, 100,
                                 self.boy.x, self.boy.y)


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1   # 바라보는 방향: 오른쪽 1, 왼쪽 -1
        self.image = load_image('animation_sheet.png')

        self.IDLE = Idle(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {},
            }
        )

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
