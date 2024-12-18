import threading
import unittest
from car import Car
from car_controller import CarController
from gui import CarSimulatorGUI

global left_temp #왼쪽 문이 열린 상태에서 문을 잠그는 동작을 저장하는 임시 변수
global right_temp #오른쪽 문이 열린 상태에서 문을 잠그는 동작을 저장하는 임시 변수
left_temp = "UNLOCKED"  # 왼쪽 문 상태 초기화
right_temp = "UNLOCKED"  # 오른쪽 문 상태 초기화

def get_left_temp():
    return left_temp

def get_right_temp():
    return right_temp


# execute_command를 제어하는 콜백 함수
# -> 이 함수에서 시그널을 입력받고 처리하는 로직을 구성하면, 알아서 GUI에 연동이 됩니다.

def execute_command_callback(command, car_controller):
    global left_temp, right_temp

    commands = command.strip().split(' ')
    brake_applied_in_line = False

    length = len(commands)

    for cmd in commands:
        cmd = cmd.strip()

        if cmd == "ENGINE_BTN":
            # 현재 줄에서 브레이크가 적용된 상태에서만 엔진 동작
            if car_controller.get_lock_status(): # 차량 전체 잠금이 Locked 인 경우
                return
            elif not car_controller.get_lock_status():
                if car_controller.get_speed() == 0:
                    if not car_controller.get_engine_status():
                        if brake_applied_in_line:
                            car_controller.toggle_engine()  # 엔진 상태 변경
                            return
                    else:
                        car_controller.toggle_engine()  # 엔진 상태 변경
                        return

        elif cmd == "ACCELERATE":
            # 1. 엔진 체크 / OFF 상태면 바로 함수 종료
            if not car_controller.get_engine_status(): # 엔진이 꺼진 경우
                return
            elif car_controller.get_engine_status(): # 엔진이 켜진 경우
                # 2. 현재 속도 체크
                # 2-1. 현재 속도가 200 이상이면 가속하지 않음
                if car_controller.get_speed() >= 200:  # car_controller.get_speed() 자동차의 속도 읽기
                    return

                # 2-2. 10km 초과 시 문 닫힘
                if car_controller.get_speed() >= 10:
                    if car_controller.get_left_door_status() == "OPEN":
                        car_controller.close_left_door()
                    if car_controller.get_right_door_status() == "OPEN":
                        car_controller.close_right_door()

                # 2-3. 현재 속도가 20 이상이면 문 잠금 상태 확인 후 잠금
                if car_controller.get_speed() >= 20:
                    if car_controller.get_left_door_lock(): # 왼쪽 차 문 잠금이 해제된 경우
                        car_controller.lock_left_door() # 왼쪽 문 잠금장치 잠금
                    if car_controller.get_right_door_lock(): # 오른쪽 차 문 잠금이 해제된 경우
                        car_controller.lock_right_door() # 오른쪽 문 잠금장치 잠금

                # 2-4. 트렁크가 열려있다면 최대 제한 속도를 30km로 변경
                if car_controller.get_speed() >= 30: # 현재 속도가 30km 이상이면 가속하지 않음
                    if not car_controller.get_trunk_status():
                        return
                car_controller.accelerate() # 속도 +10
                return

        elif cmd == "BRAKE":
            # 1. 엔진 체크 / OFF 상태면 바로 함수 종료
            if not car_controller.get_engine_status(): # 엔진이 꺼진 경우
                brake_applied_in_line = True
                continue
            car_controller.brake()  # 속도 -10
            return

        elif cmd == "LOCK":
            if not car_controller.get_engine_status() and \
                car_controller.get_left_door_status() == "CLOSED" and \
                car_controller.get_right_door_status() == "CLOSED" and \
                car_controller.get_trunk_status():
                car_controller.lock_left_door()
                car_controller.lock_right_door()
                car_controller.lock_vehicle() # 차량잠금
                return

        elif cmd == "UNLOCK":
            if car_controller.get_lock_status():
                car_controller.unlock_vehicle()  # 차량잠금해제
                return

        #to discuss - SOS의 우선 순위 높이는 게 좋을 지 고민 - 전체 locked 상태에서도 하는 게 좋을지
        elif cmd == "SOS":
            while car_controller.get_speed() > 0:
                car_controller.brake()
            car_controller.unlock_left_door()
            car_controller.unlock_right_door()
            car_controller.open_left_door()
            car_controller.open_right_door()
            car_controller.open_trunk()
            return

        elif cmd == "LEFT_DOOR_LOCK":
            #차량 잠금이 열려있고, 왼쪽 문이 열린 상태에서 잠금 시도
            if left_temp  == "UNLOCKED" and \
                car_controller.get_left_door_status() == "OPEN":
                left_temp = "LOCKED"
                return

            # 차량이 전체가 잠겨있거나,
            # 왼쪽 문이 이미 잠겨 있는 경우 기존 상태를 유지.
            if car_controller.get_lock_status() or \
                car_controller.get_left_door_lock() == "LOCKED":
                return

            car_controller.lock_left_door() # 왼쪽문 잠금
            return

        elif cmd == "RIGHT_DOOR_LOCK":
            #차량 잠금이 열려있고, 오른쪽 문이 열린 상태에서 잠금 시도
            if right_temp == "UNLOCKED" and \
                car_controller.get_right_door_status() == "OPEN":
                right_temp = "LOCKED"
                return

            # 차량이 전체가 잠겨있거나,
            # 오른쪽 문이 이미 잠겨 있는 경우 기존 상태를 유지.
            if car_controller.get_lock_status() or \
                car_controller.get_right_door_lock == "LOCKED":
                return

            car_controller.lock_right_door() # 오른쪽문 잠금
            return

        elif cmd == "LEFT_DOOR_UNLOCK":
            #차량 잠금이 열려있고, 왼쪽 문이 열린 상태에서 잠금해제 시도
            if left_temp == "LOCKED" and \
                car_controller.get_left_door_status() == "OPEN":
                left_temp = "UNLOCKED"
                return

            # 차량이 전체가 잠겨있거나,
            # 왼쪽 문이 이미 잠금해제 되어있거나,
            # 속도가 20km/h 초과인 경우 기존 상태를 유지.
            if car_controller.get_lock_status() or \
                car_controller.get_left_door_lock() == "UNLOCKED" or \
                car_controller.get_speed() > 20:
                return

            car_controller.unlock_left_door() # 왼쪽문 잠금해제
            return

        elif cmd == "RIGHT_DOOR_UNLOCK":
            #차량 잠금이 열려있고, 오른쪽 문이 열린 상태에서 잠금해제 시도
            if right_temp == "LOCKED" and\
                car_controller.get_right_door_status() == "OPEN":
                right_temp = "UNLOCKED"
                return

            # 차량이 전체가 잠겨있거나,
            # 오른쪽 문이 이미 잠금해제 되어있거나,
            # 속도가 20km/h 초과인 경우 기존 상태를 유지.
            if car_controller.get_lock_status() or \
                car_controller.get_right_door_lock() == "UNLOCKED" or \
                car_controller.get_speed() > 20:
                return

            car_controller.unlock_right_door() # 오른쪽 잠금해제
            return

        elif cmd == "LEFT_DOOR_OPEN":
            if car_controller.get_left_door_lock() == "UNLOCKED" and car_controller.get_left_door_status() == "CLOSED": # 왼쪽문 잠금이 열린 경우
                car_controller.open_left_door() # 왼쪽문 열기
                left_temp = "UNLOCKED"
            return
        elif cmd == "RIGHT_DOOR_OPEN":
            if car_controller.get_right_door_lock() == "UNLOCKED" and car_controller.get_right_door_status() == "CLOSED": # 오른쪽문 잠금이 열린 경우
                car_controller.open_right_door() # 오른쪽문 열기
                right_temp = "UNLOCKED"
            return
        elif cmd == "LEFT_DOOR_CLOSE":
            if car_controller.get_left_door_status() == "OPEN": # 왼쪽문이 열린 경우
                car_controller.close_left_door() # 왼쪽문 닫기
                if left_temp == "LOCKED":
                    car_controller.lock_left_door()
            return
        elif cmd == "RIGHT_DOOR_CLOSE":
            if car_controller.get_right_door_status() == "OPEN": # 오른쪽문이 열린 경우
                car_controller.close_right_door() # 오른쪽문 닫기
                if right_temp == "LOCKED":
                    car_controller.lock_right_door()
            return
        elif cmd == "TRUNK_OPEN":
            if not car_controller.get_lock_status() and \
                car_controller.get_trunk_status() == True and \
                    car_controller.get_speed() == 0: # 차량이 잠겨 있지 않은 상태이면서 트렁크가 닫혀 있는 경우
                car_controller.open_trunk() # 트렁크 열기
            return
        elif cmd == "TRUNK_CLOSE":
            if car_controller.get_trunk_status() == False: #차량이 잠긴 상태이면서 트렁크가 열려 있는 경우
                car_controller.close_trunk() # 트렁크 닫기
            return

# 파일 경로를 입력받는 함수
# -> 가급적 수정하지 마세요.
#    테스트의 완전 자동화 등을 위한 추가 개선시에만 일부 수정이용하시면 됩니다. (성적 반영 X)
def file_input_thread(gui):
    while True:
        file_path = input("Please enter the command file path (or 'exit' to quit): ")

        if file_path.lower() == 'exit':
            print("Exiting program.")
            break

        # 파일 경로를 받은 후 GUI의 mainloop에서 실행할 수 있도록 큐에 넣음
        gui.window.after(0, lambda: gui.process_commands(file_path))



# 메인 실행
# -> 가급적 main login은 수정하지 마세요.
# 테스트 코드 실행
if __name__ == "__main__":

    car = Car()
    car_controller = CarController(car)

    # GUI는 메인 스레드에서 실행
    gui = CarSimulatorGUI(car_controller, lambda command: execute_command_callback(command, car_controller))

    # 파일 입력 스레드는 별도로 실행하여, GUI와 병행 처리
    input_thread = threading.Thread(target=file_input_thread, args=(gui,))
    input_thread.daemon = True  # 메인 스레드가 종료되면 서브 스레드도 종료되도록 설정
    input_thread.start()

    # GUI 시작 (메인 스레드에서 실행)
    gui.start()

    unittest.main(module='test_car', exit=False)