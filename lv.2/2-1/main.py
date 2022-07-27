from pynput import keyboard
from err import NotNumErr, NumRngErr
from puzzle_runner import NPuzzleRunner, NPuzzlePrinter

def on_press(key):
    end = False
    if key == keyboard.Key.esc:
        return False

    #player 1
    try:
        if key.char == 'w':
            end, map = players[0].mv_up()
            printer.update_map(0, map)
            return True
        elif key.char == 'a':
            end, map = players[0].mv_left()
            printer.update_map(0, map)
            return True
        elif key.char == 's':
            end, map = players[0].mv_down()
            printer.update_map(0, map)
            return True
        elif key.char == 'd':
            end, map = players[0].mv_right()
            printer.update_map(0, map)
            return True
        elif key.char == '`':
            print(players[0].hint())
            return True
        # elif key.char == '1': # move auto
        #     end = players[1].auto_move()
        elif key.char == '2': # save
            players[0].save()
            return True
        elif key.char == '3': # load
            players_map[0] = players[0].load()
            printer.update_map(0, map)
            return True
    except:
        None

    #player2 - if not have array, raise error
    try:
        if key == keyboard.Key.up:
            end, map = players[1].mv_up()
            printer.update_map(1, map)
            return True
        elif key == keyboard.Key.down:
            end, map = players[1].mv_down()
            printer.update_map(1, map)
            return True
        elif key == keyboard.Key.left:
            end, map = players[1].mv_left()
            printer.update_map(1, map)
            return True
        elif key == keyboard.Key.right:
            end, map = players[1].mv_right()
            printer.update_map(1, map)
            return True

        if key.char == 'u':
            print(players[1].hint())
            return True
        # elif key.char == 'i':
            # end = players[1].auto_move()
        elif key.char == 'o':
            players[1].save()
            return True
        elif key.char == 'p':
            players_map[1] = players[1].load()
            printer.update_map(1, map)
            return True
    except:
        return True

    if end == True:
        return False

if __name__ == "__main__":
    players_map = []
    players = []
    while True:
        while True:
            sl = input("시작 : s, 로드 : l, 종료 : e >> ")
            if sl.lower() == 's':
                size = int(input('퍼즐 가로 크기 입력 >> '))
                while True:
                    try:
                        player_cnt = input("플레이어 수 입력(1 or 2) >> ")
                        if not player_cnt.isdecimal():
                            raise NotNumErr(player_cnt)

                        player_cnt = int(player_cnt)
                        if player_cnt > 2:
                            raise NumRngErr(player_cnt)
                        if player_cnt < 1:
                            raise NumRngErr(player_cnt)

                        break
                    except NotNumErr as err:
                        print(err)
                        continue
                    except NumRngErr as err:
                        print(err)
                        continue

                for i in range(player_cnt):
                    test = NPuzzleRunner(size, i)
                    players.append(test)
                    players_map.append(test.mv_start())
                break

            elif sl.lower() == 'l':
                test = NPuzzleRunner(2, 0)
                if test.load():
                    break
            elif sl.lower() == 'e':
                exit()
        printer = NPuzzlePrinter(players_map)
        printer.print_puzzle()
        print('start', len(players_map))
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
        if input("exit?(Y/n) >> ").lower() == 'y':
            exit()
# 기본
#   ▪메뉴 방식으로 프로그램이 실행된다. - 완료
#   ▪2개 이상의 소스파일과 1개 이상의 헤더파일을 사용한다. - 완료
#   ▪초기 상태 생성 문제 해결 : - 0~8까지의 숫자 생성 후 위치 옮기기로 초기상태 생성
#     9개의 위치에 1부터 8까지의 숫자를 무작위로 위치시키면 풀 수 있는 퍼즐의 초기 상태가 만들어질까?
#     다음과 같은 3-puzzle로부터 해답을 구해보고, 무작위가 아닌 어떤 방법으로 초기 상태를 생성해야 하는지 고안하라.
#   ▪전역 변수 사용은 가급적 자제한다. - 클래스 내부에서 쓰는 전역변수는 없음
#   ▪키보드(또는 마우스)를 통해 다음 상태로의 이동이 가능하다. - 완료
#   ▪현재 상태를 알기 쉽게 표현할 수 있다. - 완료
#   ▪게임이 끝났는지(최종 상태와 같은지) 알 수 있다. - 완료
#   ▪게임판의 크기를 조정할 수 있다. - 완료

# 심화
#    ① 현재 상태를 파일로 저장한 후 나중에 이 상태로부터 다시 시작할 수 있다. - 완료
#    ② GUI 방식으로 구현한다. - GUI는 버린다
#    ③ 2인용 모드 : 두 명이 동시에 게임을 진행할 수 있다. - 완료
#       (동일한 상태로부터 출발하여 누가 빨리 끝낼 수 있는지 대결)
#    ④ 컴퓨터가 스스로 이동하여 최종 상태를 만들 수 있다. - 함수는 구현 완료.
#           렉이 너무 심해 제거
#    ⑤ 컴퓨터가 최단 경로를 계산하여 스스로 게임을 실행하거나,
#       사용자 요구 시 힌트를 보여 주는 기능을 추가한다. (본 기능이 구현되는 경우 상대평가 시 반영)
#           1) 컴퓨터 스스로 실행 - 함수는 구현 완료. 게임 초반에 shuffle 반대 방향으로 이동하면 됨
#               렉이 너무 심해 제거
#           2) 힌트 제공 - 완료