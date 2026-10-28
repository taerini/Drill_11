from pico2d import (load_image, get_time,
                    SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT)

from state_machine import StateMachine, space_down, time_out


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


class Sleep:
    def __init__(self, boy):
        self.boy = boy

    def enter(self):
        self.boy.frame = 0

    def exit(self):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8

    def draw(self):
        # 90도 회전시켜 누운 모습으로 그린다.
        if self.boy.face_dir == 1:
            self.boy.image.clip_composite_draw(self.boy.frame * 100, 300, 100, 100,
                                               3.141592 / 2, '',
                                               self.boy.x - 25, self.boy.y - 25, 100, 100)
        else:
            self.boy.image.clip_composite_draw(self.boy.frame * 100, 200, 100, 100,
                                               -3.141592 / 2, '',
                                               self.boy.x + 25, self.boy.y - 25, 100, 100)


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0        # 눌려 있는 방향키의 합: 오른쪽 +1, 왼쪽 -1
        self.face_dir = 1   # 바라보는 방향: 오른쪽 1, 왼쪽 -1
        self.image = load_image('animation_sheet.png')

        self.IDLE = Idle(self)
        self.SLEEP = Sleep(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {time_out: self.SLEEP},
                self.SLEEP: {space_down: self.IDLE},
            }
        )

    def handle_event(self, event):
        if event.type in (SDL_KEYDOWN, SDL_KEYUP) and event.key in (SDLK_LEFT, SDLK_RIGHT):
            # 키를 누를 때와 뗄 때 dir 을 반대로 바꿔서, 양쪽을 동시에 누르면 0 이 된다.
            sign = 1 if event.type == SDL_KEYDOWN else -1
            self.dir += sign if event.key == SDLK_RIGHT else -sign
            if self.dir != 0:
                self.face_dir = self.dir
            self.state_machine.handle_event(('DIR', self.dir))
        else:
            self.state_machine.handle_event(('INPUT', event))

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
