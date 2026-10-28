# PRD — Drill #11 소년 자동 무적 런(AutoRun) 상태 추가

## 1. 개요

2D 게임 프로그래밍 실습 Drill #11 과제이다. pico2d로 만든 소년 캐릭터에 상태 머신 기반 캐릭터 컨트롤러를 구현하고,
새로운 상태인 **AutoRun(자동 무적 런)** 을 추가한다.

## 2. 목표

- 캐릭터의 상태를 클래스(`enter` / `exit` / `do` / `draw`)로 분리하고, 상태 전환은 규칙 테이블로 관리한다.
- AutoRun 상태를 **별도의 상태 클래스**로 구현한다.
- 상태 다이어그램을 그려 저장소에 이미지 파일로 포함한다.

## 3. 기능 요구사항

| ID | 요구사항 |
|---|---|
| F1 | Idle 상태에서 `a` 키를 누르면 AutoRun 상태가 되어, 키 조작 없이 계속 좌우로 이동한다. |
| F2 | AutoRun 상태에서 소년은 속도가 빨라지고 크기가 확대된다. |
| F3 | AutoRun 상태에서 화면의 좌우 끝에 닿으면 자동으로 방향을 바꾼다. |
| F4 | AutoRun 상태에서 5초 이상 지나면 Idle 상태로 돌아간다. |
| F5 | AutoRun 상태에서 방향키가 눌리면 무적 런이 취소되고, 눌린 방향으로 움직이는 Run 상태가 된다. |
| F6 | Idle 상태에서 5초가 지나면 Sleep 상태(누운 모습)가 되고, Sleep 상태에서 SPACE 키를 누르면 Idle로 돌아온다. |
| F7 | Idle / Sleep 상태에서 ← / → 키를 누르면 Run 상태가 되고, 방향키를 모두 떼면 Idle로 돌아온다. 좌우는 하나의 Run 상태로 처리하며, 화면 밖으로 나가지 않는다. |

## 4. 제약 사항

- 언어 / 라이브러리: Python 3, pico2d
- AutoRun은 반드시 별도의 상태 클래스로 구현한다.
- 상태 다이어그램 이미지 파일을 저장소에 포함한다.

## 5. 상태 정의

| 상태 | 모습 | 동작 |
|---|---|---|
| Idle | 서 있음 | 제자리 애니메이션. 진입 후 5초가 지나면 time_out 이벤트 발생 |
| Sleep | 90도 회전해 누운 모습 | 제자리에서 잠 |
| Run | 달리는 모습 | 눌린 방향키 방향으로 이동 (화면 안으로 제한) |
| AutoRun | 2배 크기로 달리는 모습 | 키 조작 없이 빠르게 이동, 좌우 끝에서 방향 전환. 진입 후 5초가 지나면 time_out 이벤트 발생 |

## 6. 상태 전환

![상태 다이어그램](state_diagram.png)

| 현재 상태 | 이벤트 | 다음 상태 |
|---|---|---|
| Idle | `time_out` (5초 경과) | Sleep |
| Idle | `move_start` (←/→ 누름) | Run |
| Idle | `a_down` (`a` 키) | AutoRun |
| Sleep | `space_down` (SPACE 키) | Idle |
| Sleep | `move_start` (←/→ 누름) | Run |
| Run | `move_stop` (방향키 모두 뗌) | Idle |
| AutoRun | `time_out` (5초 경과) | Idle |
| AutoRun | `move_start` (←/→ 누름) | Run |

방향키는 `dir` 값 하나로 관리한다. 오른쪽 키를 누르면 +1, 왼쪽 키를 누르면 -1이고 떼면 반대로 더한다.
양쪽 키를 동시에 누르면 `dir`이 0이 되어 Idle이 된다.

## 7. 수치

| 항목 | 값 |
|---|---|
| Run 속도 | 5 px / 프레임 |
| AutoRun 속도 | 15 px / 프레임 (Run의 3배) |
| 기본 크기 | 100 × 100 |
| AutoRun 크기 | 200 × 200 (2배, 발이 땅에 닿도록 위로 올려 그림) |
| Idle → Sleep, AutoRun → Idle 대기 시간 | 5초 |

## 8. 구현 구조

| 파일 | 내용 |
|---|---|
| `main.py` | 게임 루프, 키 이벤트를 소년에게 전달 |
| `state_machine.py` | `StateMachine` 클래스(규칙 테이블 기반 전환)와 이벤트 검사 함수 |
| `boy.py` | `Idle`, `Sleep`, `Run`, `AutoRun` 상태 클래스와 `Boy` 클래스 |
| `grass.py` | 배경 잔디 |
| `state_diagram.png` | 상태 다이어그램 |

## 9. 채점 기준 대응

| 채점 기준 | 구현 위치 |
|---|---|
| `a`를 누르면 AutoRun 상태로 이동 | `Boy` 규칙 테이블의 `self.IDLE: {a_down: self.AUTO_RUN}` |
| 5초 이상 지나면 Idle 복귀 | `AutoRun.do()`의 타이머, 규칙 `self.AUTO_RUN: {time_out: self.IDLE}` |
| AutoRun에서 속도가 빨라지고 크기가 커짐 | `AutoRun.SPEED`, `AutoRun.SIZE` |
| AutoRun에서 좌우 끝 자동 방향 전환 | `AutoRun.do()`의 경계 검사 |
| 상태 다이어그램 | `state_diagram.png` |

## 10. 테스트 시나리오

- [ ] 실행 직후 Idle 상태로 서 있다.
- [ ] Idle에서 `a`를 누르면 커진 소년이 빠르게 달리고, 화면 끝에서 방향을 바꾼다.
- [ ] AutoRun 5초 후 원래 크기로 Idle 상태가 된다.
- [ ] AutoRun 중 ←를 누르면 원래 크기로 왼쪽으로 달리고, 키를 떼면 Idle이 된다.
- [ ] Run 중 화면 끝에서 더 나가지 않는다.
- [ ] Idle 5초 후 누워서 자고, SPACE로 일어나며, 방향키로 바로 달린다.
