import threading
import unittest
import logging
from car import Car
from car_controller import CarController
from gui import CarSimulatorGUI

global left_temp #왼쪽 문이 열린 상태에서 문을 잠그는 동작을 저장하는 임시 변수
global right_temp #오른쪽 문이 열린 상태에서 문을 잠그는 동작을 저장하는 임시 변수
left_temp = "UNLOCKED"  # 왼쪽 문 상태 초기화
right_temp = "UNLOCKED"  # 오른쪽 문 상태 초기화

# 로그 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# execute_command를 제어하는 콜백 함수
# -> 이 함수에서 시그널을 입력받고 처리하는 로직을 구성하면, 알아서 GUI에 연동이 됩니다.

def execute_command_callback(command, car_controller):
    global left_temp, right_temp
    logging.info(f"명령 수신: {command}")

    if command == "ENGINE_BTN":
        if car_controller.get_lock_status(): # 차량 전체 잠금이 Locked 인 경우
            logging.info("잠긴 상태에서 엔진 시작 시도 - 무시됨")
            return # 엔진을 가동하지 않는다.
        elif not car_controller.get_lock_status(): # 차량 전체 잠금이 Unlocked 인 경우
            if car_controller.get_speed() == 0:
                car_controller.toggle_engine() # 시동 ON / OFF
                logging.info(f"엔진 상태 변경: {'ON' if car_controller.get_engine_status() else 'OFF'}")
            else:
                logging.info("가속 중인 상태에서 엔진 정지 시도 - 무시됨")
    
    elif command == "ACCELERATE":
        # 1. 엔진 체크 / OFF 상태면 바로 함수 종료
        if not car_controller.get_engine_status(): # 엔진이 꺼진 경우
            logging.info("엔진이 꺼진 상태에서 가속 시도 - 무시됨")
            return
        elif car_controller.get_engine_status(): # 엔진이 켜진 경우 
            # 2. 현재 속도 체크
            # 2-1. 현재 속도가 200 이상이면 가속하지 않음
            if car_controller.get_speed() == 200:  # car_controller.get_speed() 자동차의 속도 읽기
                logging.info("속도가 이미 200 이상임 - 추가 가속 불가")
                return
            
            # 2-2. 10km 초과 시 문 닫힘
            elif car_controller.get_speed() == 10:
                if car_controller.get_left_door_status() == "Opened" or car_controller.get_right_door_status() == "Opened":
                    car_controller.close_left_door()
                    car_controller.close_right_door()
                    car_controller.accelerate()
                    logging.info("속도가 10 km/h를 초과하여 문 닫힘 / 가속됨 - 현재 속도: {car_controller.get_speed()} km/h ")
                    return
                else:
                    car_controller.accelerate()
                    logging.info(f"가속됨 - 현재 속도: {car_controller.get_speed()} km/h")
                    return
                
            # 2-3. 트렁크가 열려있다면 최대 제한 속도를 30km로 변경
            elif car_controller.get_speed() == 30: # 현재 속도가 20km 이하인 경우 가속
                if not car_controller.get_trunk_status():
                    logging.info("트렁크가 열려 있음 - 가속이 30 km/h로 제한됨")
                    return
                else:
                    car_controller.accelerate() # 속도 +10
                    logging.info(f"가속됨 - 현재 속도: {car_controller.get_speed()} km/h")
                    return
            
            # 2-4. 현재 속도가 20 이상이면 문 잠금 상태 확인 후 잠금 후 가속
            elif car_controller.get_speed() == 20:
                if car_controller.get_left_door_lock(): # 왼쪽 차 문 잠금이 해제된 경우
                    car_controller.lock_left_door() # 왼쪽 문 잠금장치 잠금
                    logging.info("속도가 20 km/h를 초과하여 왼쪽 문 잠김")
                if car_controller.get_right_door_lock(): # 오른쪽 차 문 잠금이 해제된 경우 
                    #elif -> if 이유) elif  사용하면 둘다 해제되어 있는 경우 하나만 잠금
                    car_controller.lock_right_door() # 오른쪽 문 잠금장치 잠금
                    logging.info("속도가 20 km/h를 초과하여 오른쪽 문 잠김")
                if car_controller.get_left_door_lock() == "LOCKED" and car_controller.get_right_door_lock() == "LOCKED": # 다 잠겨있으면
                    car_controller.accelerate() # 속도 +10
                    logging.info(f"가속됨 - 현재 속도: {car_controller.get_speed()} km/h")
            else: # 모든 경우에 포함 안되면 가속
                car_controller.accelerate() # 속도 +10
                logging.info(f"가속됨 - 현재 속도: {car_controller.get_speed()} km/h")
                return

    elif command == "BRAKE":
        # 1. 엔진 체크 / OFF 상태면 바로 함수 종료
        if not car_controller.get_engine_status(): # 엔진이 꺼진 경우
            logging.info("엔진이 꺼진 상태에서 브레이크 시도 - 무시됨")
            return
        elif car_controller.get_engine_status(): # 엔진이 켜진 경우 
            car_controller.brake() # 속도 -10
            logging.info(f"감속됨 - 현재 속도: {car_controller.get_speed()} km/h")
            return

    elif command == "LOCK":
        if not car_controller.get_engine_status() and \
            car_controller.get_left_door_status() == "CLOSED" and \
            car_controller.get_right_door_status() == "CLOSED" and \
            car_controller.get_trunk_status():
            car_controller.lock_left_door()
            car_controller.lock_right_door()
            car_controller.lock_vehicle() # 차량잠금
            logging.info("차량 잠김")
            return

    elif command == "UNLOCK":
        if car_controller.get_lock_status() == True:
            car_controller.unlock_vehicle()  # 차량잠금해제
            logging.info("차량 잠금 해제")
            logging.info(f"현재 잠금 상태: {car_controller.get_lock_status()}")
            return

    #to discuss - SOS의 우선 순위 높이는 게 좋을 지 고민 - 전체 locked 상태에서도 하는 게 좋을지
    elif command == "SOS":
        while car_controller.get_speed() > 0:
            car_controller.brake()
        logging.info("비상 브레이크 작동 - 속도 0 km/h로 감소")
        car_controller.unlock_left_door()
        car_controller.unlock_right_door()
        car_controller.open_left_door()
        car_controller.open_right_door()
        car_controller.open_trunk()
        logging.info("SOS 작업 완료 - 문 잠금 해제, 문 열기 및 트렁크 열림")
        return
    
    elif command == "LEFT_DOOR_LOCK":
        #차량 잠금이 열려있고, 왼쪽 문이 열린 상태에서 잠금 시도
        if car_controller.get_lock_status() == "UNLOCKED" and \
            car_controller.get_left_door_status() == "OPEN":
                left_temp = "LOCKED"
                return
        
        # 차량이 전체가 잠겨있거나, 
        # 왼쪽 문이 이미 잠겨 있는 경우 기존 상태를 유지.
        if car_controller.get_lock_status() == "LOCKED" or \
            car_controller.get_left_door_lock() == "LOCKED":
                logging.info("왼쪽 문 잠금 시도 무시됨 - 이미 잠겨 있거나 차량 전체가 잠겨 있음")
                return
        
        car_controller.lock_left_door() # 왼쪽문 잠금
        logging.info("왼쪽 문 잠김")

    elif command == "RIGHT_DOOR_LOCK":
        #차량 잠금이 열려있고, 오른쪽 문이 열린 상태에서 잠금 시도
        if right_temp == "UNLOCKED" and \
            car_controller.get_right_door_status() == "OPEN":
                right_temp = "LOCKED"
                return
        
        # 차량이 전체가 잠겨있거나, 
        # 오른쪽 문이 이미 잠겨 있는 경우 기존 상태를 유지.
        if car_controller.get_lock_status() == "LOCKED" or \
            car_controller.get_right_door_lock == "LOCKED":
                logging.info("오른쪽 문 잠금 시도 무시됨 - 이미 잠겨 있거나 차량 전체가 잠겨 있음")
                return
        
        car_controller.lock_right_door() # 오른쪽문 잠금
        logging.info("오른쪽 문 잠김")
        
    elif command == "LEFT_DOOR_UNLOCK":
        #차량 잠금이 열려있고, 왼쪽 문이 열린 상태에서 잠금해제 시도
        if left_temp == "UNLOCKED" and \
            car_controller.get_left_door_status() == "OPEN":
                left_temp = "UNLOCKED"
                return
        
        # 차량이 전체가 잠겨있거나,
        # 왼쪽 문이 이미 잠금해제 되어있거나,
        # 속도가 20km/h 초과인 경우 기존 상태를 유지.
        if car_controller.get_lock_status() == "LOCKED" or \
            car_controller.get_left_door_lock() == "UNLOCKED" or \
            car_controller.get_speed() > 20:
                logging.info("왼쪽 문 잠금 해제 시도 무시됨 - 조건이 충족되지 않음")
                return
        
        car_controller.unlock_left_door() # 왼쪽문 잠금해제
        logging.info("왼쪽 문 잠금 해제됨")

    elif command == "RIGHT_DOOR_UNLOCK":
        #차량 잠금이 열려있고, 오른쪽 문이 열린 상태에서 잠금해제 시도
        if car_controller.get_lock_status() == "UNLOCKED" and \
            car_controller.get_right_door_status() == "OPEN":
                right_temp = "UNLOCKED"
                return
        
        # 차량이 전체가 잠겨있거나,
        # 오른쪽 문이 이미 잠금해제 되어있거나,
        # 속도가 20km/h 초과인 경우 기존 상태를 유지.
        if car_controller.get_lock_status() == "LOCKED" or \
            car_controller.get_right_door_lock() == "UNLOCKED" or \
            car_controller.get_speed() > 20:
            logging.info("오른쪽 문 잠금 해제 시도 무시됨 - 조건이 충족되지 않음")
            return

        car_controller.unlock_right_door() # 오른쪽 잠금해제
        logging.info("오른쪽 문 잠금 해제됨")

    elif command == "LEFT_DOOR_OPEN":
        if car_controller.get_left_door_lock() == "UNLOCKED" and car_controller.get_left_door_status() == "CLOSED" and car_controller.get_speed() < 20: # 왼쪽문 잠금이 열린 경우
            car_controller.open_left_door() # 왼쪽문 열기
            left_temp = "UNLOCKED"
            logging.info("왼쪽 문 열림")
    elif command == "RIGHT_DOOR_OPEN":
        if car_controller.get_right_door_lock() == "UNLOCKED" and car_controller.get_right_door_status() == "CLOSED" and car_controller.get_speed() < 20: # 오른쪽문 잠금이 열린 경우
            car_controller.open_right_door() # 오른쪽문 열기
            right_temp = "UNLOCKED"
            logging.info("오른쪽 문 열림")
    elif command == "LEFT_DOOR_CLOSE":
        if car_controller.get_left_door_status() == "OPEN": # 왼쪽문이 열린 경우
            car_controller.close_left_door() # 왼쪽문 닫기
            logging.info("왼쪽 문 닫힘")
            if left_temp == "LOCKED":
                car_controller.lock_left_door()
                logging.info("왼쪽 문 잠김")
    elif command == "RIGHT_DOOR_CLOSE":
        if car_controller.get_right_door_status() == "OPEN": # 오른쪽문이 열린 경우
            car_controller.close_right_door() # 오른쪽문 닫기
            logging.info("오른쪽 문 닫힘")
            if right_temp == "LOCKED":
                car_controller.lock_right_door()
                logging.info("오른쪽 문 잠김")
    elif command == "TRUNK_OPEN": 
        if car_controller.get_lock_status() == "UNLOCKED" and car_controller.get_trunk_status() == "CLOSE" and car_controller.get_speed() <= 30: # 차량이 잠겨 있지 않은 상태이면서 트렁크가 닫혀 있는 경우 
            car_controller.open_trunk() # 트렁크 열기 
    elif command == "TRUNK_CLOSE": 
    # car_controller.get_lock_status() == "LOCKED" 이 부분 삭제했습니다.
        if car_controller.get_trunk_status() == "OPEN": #차량이 잠긴 상태이면서 트렁크가 열려 있는 경우
            car_controller.close_trunk() # 트렁크 닫기

# 파일 경로를 입력받는 함수
# -> 가급적 수정하지 마세요.
#    테스트의 완전 자동화 등을 위한 추가 개선시에만 일부 수정이용하시면 됩니다. (성적 반영 X)
def file_input_thread(gui):
    while True:
        file_path = input("Please enter the command file path (or 'exit' to quit): ")

        if file_path.lower() == 'exit':
            logging.info("프로그램 종료 중.")
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

class TestSOS(unittest.TestCase):
    """
    1. 차를 정지(speed=0)시켜야 함
    2. 모든 문의 잠금 상태를 열림(left_door_lock="UNLOCKED"&right_door_lock="UNLOCKED")으로
    3. 모든 문을 열어야 함(left_door_status="OPEN"&right_door_status="OPEN")
    4. 트렁크가 열려야 함(trunk_status=false)
    """

    def setUp(self):
        self.car = Car()
        self.controller = CarController(self.car)

    def test_sos_normal(self):
        """
        가속상황에서
        SOS 기능 정상 작동 테스트: 정지, 모든 문/트렁크 열림
        """
        self.controller.unlock_vehicle()
        self.controller.toggle_engine()
        self.controller.accelerate()

        execute_command_callback("SOS", self.controller)

        self.assertEqual(self.car.speed, 0)
        self.assertEqual(self.car.left_door_lock, "UNLOCKED")
        self.assertEqual(self.car.right_door_lock, "UNLOCKED")
        self.assertEqual(self.car.left_door_status, "OPEN")
        self.assertEqual(self.car.right_door_status, "OPEN")
        self.assertFalse(self.car.trunk_status)

    def test_sos_already_stopped(self):
        """
        정지상황에서
        SOS 기능: 이미 정지 상태일 때도 모든 문/트렁크 열림
        """

        execute_command_callback("SOS", self.controller)

        self.assertEqual(self.car.speed, 0)
        self.assertEqual(self.car.left_door_lock, "UNLOCKED")
        self.assertEqual(self.car.right_door_lock, "UNLOCKED")
        self.assertEqual(self.car.left_door_status, "OPEN")
        self.assertEqual(self.car.right_door_status, "OPEN")
        self.assertFalse(self.car.trunk_status)

class TestLock(unittest.TestCase):
    '''
    엔진 꺼져있고, 모든 문 닫혀 있고, 트렁크 닫혀 있으면 → 접근 제한 잠금 수행
    '''

    def setUp(self):
        self.car = Car()
        self.controller = CarController(self.car)

    def test_lock_normal(self):
        """정상적인 LOCK 조건: 엔진 꺼짐, 모든 문/트렁크 닫힘 -> 잠김"""
        self.controller.toggle_engine()
        self.controller.close_left_door()
        self.controller.close_right_door()
        self.controller.close_trunk()
        execute_command_callback("LOCK", self.controller)
        self.assertTrue(self.car.lock)

    def test_lock_engine_on(self):
        """LOCK 실패 조건: 엔진 켜짐 -> 잠기지 않음"""
        self.controller.toggle_engine()
        execute_command_callback("LOCK", self.controller)
        self.assertFalse(self.car.lock)

    def test_lock_left_door_open(self):
        """LOCK 실패 조건: 왼쪽 문 열림 -> 잠기지 않음"""
        self.controller.toggle_engine()
        self.controller.open_left_door()
        execute_command_callback("LOCK", self.controller)
        self.assertFalse(self.car.lock)

    def test_lock_right_door_open(self):
        """LOCK 실패 조건: 오른쪽 문 열림 -> 잠기지 않음"""
        self.controller.toggle_engine()
        self.controller.open_right_door()
        execute_command_callback("LOCK", self.controller)
        self.assertFalse(self.car.lock)

    def test_lock_trunk_open(self):
        """LOCK 실패 조건: 트렁크 열림 -> 잠기지 않음"""
        self.controller.toggle_engine()
        self.controller.open_trunk()
        execute_command_callback("LOCK", self.controller)
        self.assertFalse(self.car.lock)

class TestUnlock(unittest.TestCase):

    def setUp(self):
        self.car = Car()
        self.controller = CarController(self.car)

    def test_unlock_normal(self):
        """UNLOCK 정상 조건: 잠김 상태 -> 잠금 해제"""
        self.controller.lock_vehicle()
        execute_command_callback("UNLOCK", self.controller)
        self.assertFalse(self.car.lock)

    def test_unlock_already_unlocked(self):
        """UNLOCK: 이미 잠금 해제 상태 -> 상태 변화 없음"""
        execute_command_callback("UNLOCK", self.controller)
        self.assertFalse(self.car.lock)


class TestAccelerate(unittest.TestCase): #가속 테스트 케이스
    def setUp(self):
        self.car = Car()
        self.car_controller = CarController(self.car)

    #test case1 : 시스템의 상태 여부 확인 / 10km 이상 속도 올라가면 문 닫기
    def test_Accelerate_when_unlocked(self):
        
        # 전체 잠금이 되어 있는 경우 
        execute_command_callback("LOCK", self.car_controller)
        self.assertTrue(self.car_controller.get_lock_status())
        execute_command_callback("ACCELERATE", self.car_controller)
        #속도 변화가 없어야 한다
        self.assertEqual(self.car_controller.get_speed(), 0) 

        # 전체 잠금이 해제 되어 있는 경우
        execute_command_callback("UNLOCK", self.car_controller)
        self.assertFalse(self.car_controller.get_lock_status())
        execute_command_callback("ENGINE_BTN", self.car_controller)
        
        #속도가 높아져야 한다 1 (현재 속도가 0인 경우)
        execute_command_callback("ACCELERATE", self.car_controller)
        self.assertEqual(self.car_controller.get_speed(), 10)

        #속도가 높아져야 한다 2 (현재 속도가 10인 경우)
        execute_command_callback("ACCELERATE", self.car_controller)
        self.assertEqual(self.car_controller.get_speed(), 20)

    #test case2 : 엔진의 상태 여부 확인
    def test_Accelerate_when_engine(self):

        # 엔진이 꺼져있는 경우
        execute_command_callback("UNLOCK", self.car_controller)
        self.assertFalse(self.car_controller.get_lock_status())

        #속도 변화가 없어야 한다
        execute_command_callback("ACCELERATE", self.car_controller)
        self.assertEqual(self.car_controller.get_speed(), 0) 
        
        execute_command_callback("ENGINE_BTN", self.car_controller)
        #속도가 높아져야 한다 1 (현재 속도가 0인 경우)
        execute_command_callback("ACCELERATE", self.car_controller)
        self.assertEqual(self.car_controller.get_speed(), 10)

        #속도가 높아져야 한다 2 (현재 속도가 10인 경우)
        execute_command_callback("ACCELERATE", self.car_controller)
        self.assertEqual(self.car_controller.get_speed(), 20)

    #test case3 : 문의 상태 확인 / 트렁크의 상태 확인 / 최대 제한 속도 확인 / 속도에 따른 여부 확인
    def test_Accelerate_when_trunk_door(self):

        execute_command_callback("UNLOCK", self.car_controller)
        execute_command_callback("ENGINE_BTN", self.car_controller)
        
        #문의 상태 확인 (현재 속도가 20km/h인 경우)
        for i in range(2):
            execute_command_callback("ACCELERATE", self.car_controller)
        self.assertEqual(self.car_controller.get_speed(), 20)
        #문이 제대로 닫혀있나 확인
        self.assertEqual(self.car_controller.get_left_door_lock(), "CLOSED")
        self.assertEqual(self.car_controller.get_left_door_lock(), "CLOSED")


        execute_command_callback("ACCELERATE", self.car_controller)
        #문 잠금 상태 확인 후 잠그기
        if(self.car_controller.get_left_door_lock() == "LOCKED" or self.car_controller.get_right_door_lock() == "LOCKED"):
             #문 잠긴 경우 속도 변함
            execute_command_callback("ACCELERATE", self.car_controller)
            self.assertEqual(self.car_controller.get_speed(), 40)
        else:
            #문 잠김 열린 경우 잠그고 속도 변경
            execute_command_callback("LEFT_DOOR_UNLOCK", self.car_controller)
            self.assertEqual(self.car_controller.get_left_door_lock(), "LOCKED")
            execute_command_callback("RIGHT_DOOR_UNLOCK", self.car_controller)
            self.assertEqual(self.car_controller.get_right_door_lock(), "LOCKED")
            execute_command_callback("ACCELERATE", self.car_controller)
            self.assertEqual(self.car_controller.get_speed(), 40)

        #현재 속도가 30km/h인 경우 트렁크 확인
        if(self.car_controller.get_trunk_status() == "TRUNK_CLOSE"):
            #트렁크 닫힌 경우 속도 변함
            execute_command_callback("ACCELERATE", self.car_controller)
            self.assertEqual(self.car_controller.get_speed(), 50)
        
        else:
            #트렁크 열린 경우 속도 안 변함
            execute_command_callback("ACCELERATE", self.car_controller)
            self.assertEqual(self.car_controller.get_speed(), 30)

            #트렁크 닫고 다시 가속하면 속도 변함
            execute_command_callback("TRUNK_CLOSE", self.car_controller)
            self.assertEqual(self.car_controller.get_trunk_status() , "TRUNK_CLOSE")
            execute_command_callback("ACCELERATE", self.car_controller)
            self.assertEqual(self.car_controller.get_speed(), 40)
            
        for i in range(16):
            execute_command_callback("ACCELERATE", self.car_controller)
        self.assertEqual(self.car_controller.get_speed(), 200)

        #속도가 높아지지 않는다 (최대 속도에 도달한 경우)
        execute_command_callback("ACCELERATE", self.car_controller)
        self.assertEqual(self.car_controller.get_speed(), 200)

class TestBrake(unittest.TestCase): #감속 테스트 케이스
    def setUp(self):
        self.car = Car()
        self.car_controller = CarController(self.car)

    #test case1 : 시스템의 상태 여부 확인 / 속도에 따른 여부 확인
    def test_brake_when_unlocked(self):
        
        # 전체 잠금이 되어 있는 경우 
        execute_command_callback("LOCK", self.car_controller)
        self.assertTrue(self.car_controller.get_lock_status())
        execute_command_callback("BRAKE", self.car_controller)
        #속도 변화가 없어야 한다
        self.assertEqual(self.car_controller.get_speed(), 0) 

        # 전체 잠금이 해제 되어 있는 경우
        execute_command_callback("UNLOCK", self.car_controller)
        self.assertFalse(self.car_controller.get_lock_status())
        execute_command_callback("ENGINE_BTN", self.car_controller)
        
        #속도의 변화가 없어야 한다 (현재 속도가 0인 경우)
        execute_command_callback("BRAKE", self.car_controller)
        self.assertEqual(self.car_controller.get_speed(), 0)

        #속도가 줄어들어야 한다 1 (현재 속도가 10인 경우)
        execute_command_callback("ACCELERATE", self.car_controller)
        execute_command_callback("BRAKE", self.car_controller)
        self.assertEqual(self.car_controller.get_speed(), 0)

        #속도가 줄어들어야 한다 2 (현재 속도가 20인 경우)
        execute_command_callback("ACCELERATE", self.car_controller)
        execute_command_callback("ACCELERATE", self.car_controller)
        execute_command_callback("BRAKE", self.car_controller)
        self.assertEqual(self.car_controller.get_speed(), 10)

    #test case2 : 엔진의 상태 여부 확인 / 속도에 따른 여부 확인
    def test_brake_when_engine(self):
        # 엔진이 꺼져 있는 경우 
        execute_command_callback("UNLOCK", self.car_controller)
        execute_command_callback("BRAKE", self.car_controller)
        #속도 변화가 없어야 한다
        self.assertEqual(self.car_controller.get_speed(), 0) 

        # 엔진이 켜져 있는 경우
        execute_command_callback("ENGINE_BTN", self.car_controller)
        self.assertTrue(self.car_controller.get_engine_status())
        
        #속도가 줄어들어야 한다 1 (현재 속도가 0인 경우)
        execute_command_callback("BRAKE", self.car_controller)
        self.assertEqual(self.car_controller.get_speed(), 0)

        #속도가 줄어들어야 한다 2 (현재 속도가 10인 경우)
        execute_command_callback("ACCELERATE", self.car_controller)
        execute_command_callback("BRAKE", self.car_controller)
        self.assertEqual(self.car_controller.get_speed(), 0)

        #속도가 줄어들어야 한다 3 (현재 속도가 20인 경우)
        execute_command_callback("ACCELERATE", self.car_controller)
        execute_command_callback("ACCELERATE", self.car_controller)
        execute_command_callback("BRAKE", self.car_controller)
        self.assertEqual(self.car_controller.get_speed(), 10)


class TestEngineToggle(unittest.TestCase):
    def setUp(self):
        self.car = Car()  # Car 클래스 인스턴스 생성
        self.car_controller = CarController(self.car)  # CarController 인스턴스 생성
   
    # 차량 전체 잠금 해제 상태일 때, 엔진 토글이 작동하는 지 확인
    def test_engine_when_unlocked(self):
        self.car_controller.unlock_vehicle()
        self.assertFalse(self.car_controller.get_engine_status())

        execute_command_callback("ENGINE_BTN", self.car_controller)
        self.assertTrue(self.car_controller.get_engine_status())

        execute_command_callback("ENGINE_BTN", self.car_controller)
        self.assertFalse(self.car_controller.get_engine_status())

    # 차량 전체 잠금 상태일때, 엔진 토글이 작동하지 않음을 확인.
    def test_engine_when_locked(self):
        self.car_controller.lock_vehicle()
        self.assertFalse(self.car_controller.get_engine_status())
        
        execute_command_callback("ENGINE_BTN", self.car_controller)
        self.assertFalse(self.car_controller.get_engine_status())

    # 차량이 가속 중 일때, 엔진 토글이 작동하지 않음을 확인(엔진이 OFF 되는지)
    def test_engine_when_accelerating(self):
        self.car_controller.unlock_vehicle()
        self.assertFalse(self.car_controller.get_engine_status())
        
        execute_command_callback("ENGINE_BTN", self.car_controller)
        self.assertTrue(self.car_controller.get_engine_status())

        self.car_controller.accelerate()
        self.assertTrue(self.car_controller.get_engine_status())

        execute_command_callback("ENGINE_BTN", self.car_controller)
        self.assertTrue(self.car_controller.get_engine_status())

    # 차량이 가속 후 정지 했을 때, 엔진 토글이 작동하는지 확인
    def test_engine_when_stop(self):

        self.car_controller.unlock_vehicle()
        self.assertFalse(self.car_controller.get_engine_status())
        
        execute_command_callback("ENGINE_BTN", self.car_controller)
        self.assertTrue(self.car_controller.get_engine_status())

        self.car_controller.accelerate()
        self.assertTrue(self.car_controller.get_engine_status())

        execute_command_callback("ENGINE_BTN", self.car_controller)
        self.assertTrue(self.car_controller.get_engine_status())

        self.car_controller.brake()
        self.assertTrue(self.car_controller.get_engine_status())
        
        execute_command_callback("ENGINE_BTN", self.car_controller)
        self.assertTrue(self.car_controller.get_engine_status())
        
        
class TestCarDoorLockSystem(unittest.TestCase):

    def setUp(self):
        self.car = Car()  # Car 클래스 인스턴스 생성
        self.car_controller = CarController(self.car)  # CarController 인스턴스 생성

    # 1. 전체 잠금 on/off 상태 테스트
    def test_lock_unlock_system(self):

        # 전체 잠금을 설정한 후 문을 열 수 없는지 확인
        execute_command_callback("LOCK", self.car_controller)
        self.assertTrue(self.car_controller.get_lock_status())
        execute_command_callback("LEFT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_status(), "CLOSED")

        # 전체 잠금을 해제한 후 문을 열 수 있는지 확인
        execute_command_callback("UNLOCK", self.car_controller)
        self.assertFalse(self.car_controller.get_lock_status())
        execute_command_callback("LEFT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_status(), "CLOSED")
        execute_command_callback("LEFT_DOOR_UNLOCK", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_lock(), "UNLOCKED")
        execute_command_callback("LEFT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_status(), "OPEN")

    # 2. 각 속도 조건에서 문 열기/닫기 시도
    def test_door_operations_at_various_speeds(self):
        # 0km: 문을 열고 닫는 데 제한이 없는지 확인
        execute_command_callback("LEFT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_status(), "OPEN")
        execute_command_callback("LEFT_DOOR_CLOSE", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_status(), "CLOSED")

        # 10km: 문을 열고 닫는 데 제한이 없는지 확인
        execute_command_callback("ENGINE_BTN", self.car_controller)
        execute_command_callback("ACCELERATE", self.car_controller)  # 속도 +10km
        self.assertEqual(self.car_controller.get_speed(), 10)
        execute_command_callback("LEFT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_status(), "OPEN")
        execute_command_callback("LEFT_DOOR_CLOSE", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_status(), "CLOSED")

        # 20km 초과 (30km): 문이 잠기고 열리지 않아야 함
        execute_command_callback("ACCELERATE", self.car_controller)  # 속도 +10km
        execute_command_callback("ACCELERATE", self.car_controller)  # 속도 +10km (합계 30km)
        self.assertEqual(self.car_controller.get_speed(), 30)
        execute_command_callback("LEFT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_status(), "CLOSED")  # 열리지 않음
        self.assertEqual(self.car_controller.get_left_door_lock(), "LOCKED")  # 문이 잠겨야 함

    # 3. 문이 잠겨있거나 잠금 해제된 상태 테스트
    def test_door_lock_unlock_status(self):
        # 문이 잠금 해제된 상태에서 문 열기 시도
        self.car_controller.unlock_left_door()
        execute_command_callback("LEFT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_status(), "OPEN")
        

        # 문을 닫고 나서 잠근 후, 다시 문 열기 시도
        execute_command_callback("LEFT_DOOR_CLOSE", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_status(), "CLOSED")  # 문이 닫힌 상태 확인

        # 문이 잠겨있는 상태에서 문 열기 시도
        self.car_controller.lock_left_door()
        execute_command_callback("LEFT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_status(), "CLOSED")  # 열리지 않아야 함

    # 4. 문이 이미 열려있거나 닫혀있는 상태에서의 동작 확인
    def test_open_close_when_already_open_or_closed(self):
        # 문이 이미 열려있는 상태에서 다시 열기 시도
        self.car_controller.unlock_left_door()
        execute_command_callback("LEFT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_status(), "OPEN")
        execute_command_callback("LEFT_DOOR_OPEN", self.car_controller)  # 이미 열린 상태에서 열기 시도
        self.assertEqual(self.car_controller.get_left_door_status(), "OPEN")  # 상태 유지

        # 문이 이미 닫혀있는 상태에서 다시 닫기 시도
        execute_command_callback("LEFT_DOOR_CLOSE", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_status(), "CLOSED")
        execute_command_callback("LEFT_DOOR_CLOSE", self.car_controller)  # 이미 닫힌 상태에서 닫기 시도
        self.assertEqual(self.car_controller.get_left_door_status(), "CLOSED")  # 상태 유지

        
class TestTempLockSystem(unittest.TestCase):

    def setUp(self):
        self.car = Car()
        self.car_controller = CarController(self.car)

    # 1. 왼쪽 문이 열린 상태에서 잠금 시도 시 temp_lock을 통해 잠금이 동작되는지 확인
    def test_left_door_temp_lock(self):
        global left_temp

        # 왼쪽 문 열기
        execute_command_callback("LEFT_DOOR_UNLOCK", self.car_controller)
        execute_command_callback("LEFT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_status(), "OPEN")

        # 열린 상태에서 잠금 시도하면 실제로 잠금되지 않고 temp만 잠금 되어야함-> temp_lock에 저장
        execute_command_callback("LEFT_DOOR_LOCK", self.car_controller)
        self.assertEqual(left_temp, "LOCKED")
        self.assertEqual(self.car_controller.get_left_door_lock(), "UNLOCKED")  

        # 왼쪽 문 닫기가 적용되어야함-> temp_lock 적용
        execute_command_callback("LEFT_DOOR_CLOSE", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_status(), "CLOSED")
        self.assertEqual(self.car_controller.get_left_door_lock(), "LOCKED")  # 문이 닫히면 잠금 적용됨

    # 2. 오른쪽 문이 열린 상태에서 잠금 시도 시 temp_lock을 통해 오른쪽 잠금이 동작되는지 확인
    def test_right_door_temp_lock(self):
        global right_temp

        # 오른쪽 문 열기
        execute_command_callback("RIGHT_DOOR_UNLOCK", self.car_controller)
        execute_command_callback("RIGHT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car_controller.get_right_door_status(), "OPEN")

        # 열린 상태에서 잠금 시도하면 실제로 잠금되지 않고 temp만 잠금 되어야함-> temp_lock에 저장
        execute_command_callback("RIGHT_DOOR_LOCK", self.car_controller)
        self.assertEqual(right_temp, "LOCKED")
        self.assertEqual(self.car_controller.get_right_door_lock(), "UNLOCKED") 

        # 오른쪽 문 닫기 -> temp_lock 적용
        execute_command_callback("RIGHT_DOOR_CLOSE", self.car_controller)
        self.assertEqual(self.car_controller.get_right_door_status(), "CLOSED")
        self.assertEqual(self.car_controller.get_right_door_lock(), "LOCKED")  # 문이 닫히면 잠금 적용됨


        # 테스트 코드 실행
if __name__ == "__main__":
    unittest.main()