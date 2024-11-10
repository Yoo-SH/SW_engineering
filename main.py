import threading
from symbol import and_expr

from car import Car
from car_controller import CarController
from gui import CarSimulatorGUI


# execute_command를 제어하는 콜백 함수
# -> 이 함수에서 시그널을 입력받고 처리하는 로직을 구성하면, 알아서 GUI에 연동이 됩니다.

def execute_command_callback(command, car_controller):
    if command == "ENGINE_BTN":
        if car_controller.get_lock_status(): # 차량 전체 잠금이 Locked 인 경우
            return # 엔진을 가동하지 않는다.
        elif not car_controller.get_lock_status(): #차량 전체 잠금이 Unlocked 인 경우
            car_controller.toggle_engine # 시동 ON / OFF
    

    elif command == "ACCELERATE":
        # 1. 엔진 체크 / OFF 상태면 바로 함수 종료
        if not car_controller.get_engine_status(): #엔진이 꺼진 경우
            return
        elif car_controller.get_engine_status(): #엔진이 켜진 경우 
        
        # 2. 현재 속도 체크

            # 2-1. 현재 속도가 200 이상이면 가속하지 않음
            if car_controller.get_speed() > 200:  #car_controller.get_speed() 자동차의 속도 읽기
                return
            
            # 2-2. 트렁크가 열려있다면 최대 제한 속도를 30km로 변경 -> 트렁크가 열려있으면 30km 이상으로 올라가지 않음 -> 트렁크가 잠금 상태일 경우 열리는 것이라 설정되어 속도가 높아진 경우에 열리는 경우가 없을거 같음
            elif not car_controller.get_trunk_status():
                if car_controller.get_speed() <= 20: # 현재 속도가 20km 이하인 경우 가속
                    car_controller.accelerate() # 속도 +10
                else:
                    return
            
            # 2-3. 현재 속도가 20 이상이면 문 잠금 상태 확인 후 잠금
            elif car_controller.get_speed() > 20:
                if car_controller.get_left_door_lock(): # 왼쪽 차 문 잠금이 열린 경우
                    car_controller.lock_left_door() # 왼쪽 문 잠금장치 잠금
                elif car_controller.get_right_door_lock():# 오른쪽 차 문 잠금이 열린 경우
                    car_controller.lock_right_door() # 오른쪽 문 잠금장치 잠금
                else: # 다 잠겨있으면
                    car_controller.accelerate() # 속도 +10
    
            else: # 모든 경우에 포함 안되면 가속
                car_controller.accelerate() # 속도 +10

    elif command == "BRAKE":
        # 1. 엔진 체크 / OFF 상태면 바로 함수 종료
        if not car_controller.get_engine_status(): #엔진이 꺼진 경우
            return
        elif car_controller.get_engine_status(): #엔진이 켜진 경우 

        # 2. 현재 속도 체크
        # 2-1. 현재 속도가 0 이하이면 감속하지 않음 -> 이상인 경우만 감속
            if car_controller.get_speed() > 0:
                car_controller.brake() # 속도 -10
            else: # 이하인 경우 리턴
                return

    elif command == "LOCK":
        if not car_controller.get_engine_status() and \
            car_controller.get_left_door_status() == "CLOSED" and \
            car_controller.get_right_door_status() == "CLOSED" and \
            car_controller.get_trunk_status():
                car_controller.lock_vehicle() # 차량잠금
    elif command == "UNLOCK":
        car_controller.unlock_vehicle()  # 차량잠금해제
    elif command == "SOS":
        while car_controller.get_speed() > 0:
            car_controller.brake()
        car_controller.unlock_left_door()
        car_controller.unlock_right_door()
        car_controller.open_trunk()
    elif command == "LEFT_DOOR_LOCK":
        car_controller.lock_left_door() # 왼쪽문 잠금
    elif command == "LEFT_DOOR_UNLOCK":
        car_controller.unlock_left_door() # 왼쪽문 잠금해제
    elif command == "LEFT_DOOR_OPEN":
        car_controller.open_left_door() # 왼쪽문 열기
    elif command == "LEFT_DOOR_CLOSE":
        car_controller.close_left_door() # 왼쪽문 닫기
    elif command == "TRUNK_OPEN":
        car_controller.open_trunk() # 트렁크 열기


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