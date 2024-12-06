import unittest
from car import Car
from car_controller import CarController
from main import execute_command_callback

global left_temp #왼쪽 문이 열린 상태에서 문을 잠그는 동작을 저장하는 임시 변수
global right_temp #오른쪽 문이 열린 상태에서 문을 잠그는 동작을 저장하는 임시 변수
left_temp = "LOCKED"  # 왼쪽 문 상태 초기화
right_temp = "LOCKED"  # 오른쪽 문 상태 초기화

class TestEngineToggle(unittest.TestCase):
    def setUp(self):
        self.car = Car()  # Car 클래스 인스턴스 생성
        self.car_controller = CarController(self.car)  # CarController 인스턴스 생성

    def test_engine_start_with_brake(self):
        """브레이크를 밟은 상태에서 엔진 버튼을 누르면 엔진이 켜져야 함."""
        self.car_controller.unlock_vehicle()
        self.assertFalse(self.car_controller.get_engine_status())

        execute_command_callback("BRAKE ENGINE_BTN", self.car_controller)

        self.assertTrue(self.car_controller.get_engine_status())

    def test_engine_start_without_brake(self):
        """브레이크를 밟지 않고 엔진 버튼을 누르면 엔진이 켜지지 않아야 함."""
        self.car_controller.unlock_vehicle()
        self.assertFalse(self.car_controller.get_engine_status())

        execute_command_callback("ENGINE_BTN", self.car_controller)

        self.assertFalse(self.car_controller.get_engine_status())

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
        self.assertFalse(self.car_controller.get_engine_status())


class TestSOS(unittest.TestCase):
    """
    1. 차를 정지(speed=0)시켜야 함
    2. 모든 문의 잠금 상태를 열림(left_door_lock="UNLOCKED"&right_door_lock="UNLOCKED")으로
    3. 모든 문을 열어야 함(left_door_status="OPEN"&right_door_status="OPEN")
    4. 트렁크가 열려야 함(trunk_status=false)
    """

    def setUp(self):
        self.car = Car()
        self.car_controller = CarController(self.car)

    def test_sos_normal(self):
        """
        가속상황에서
        SOS 기능 정상 작동 테스트: 정지, 모든 문/트렁크 열림
        """
        execute_command_callback("UNLOCK", self.car_controller)
        execute_command_callback("ENGINE_BTN", self.car_controller)
        execute_command_callback("ACCELERATE", self.car_controller)

        execute_command_callback("SOS", self.car_controller)

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

        execute_command_callback("SOS", self.car_controller)

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
        self.car_controller = CarController(self.car)

    def test_lock_normal(self):
        """정상적인 LOCK 조건: 엔진 꺼짐, 모든 문/트렁크 닫힘 -> 잠김"""
        execute_command_callback("UNLOCK", self.car_controller)
        execute_command_callback("ENGINE_BTN", self.car_controller)
        execute_command_callback("LEFT_DOOR_CLOSE", self.car_controller)
        execute_command_callback("RIGHT_DOOR_CLOSE", self.car_controller)
        execute_command_callback("RIGHT_DOOR_CLOSE", self.car_controller)
        execute_command_callback("TRUNK_CLOSE", self.car_controller)
        self.assertFalse(self.car_controller.get_lock_status())

    def test_lock_engine_on(self):
        """LOCK 실패 조건: 엔진 켜짐 -> 잠기지 않음"""
        execute_command_callback("UNLOCK", self.car_controller)
        execute_command_callback("ENGINE_BTN", self.car_controller)
        execute_command_callback("LOCK", self.car_controller)
        self.assertFalse(self.car_controller.get_lock_status())

    def test_lock_left_door_open(self):
        """LOCK 실패 조건: 왼쪽 문 열림 -> 잠기지 않음"""
        execute_command_callback("UNLOCK", self.car_controller)
        execute_command_callback("ENGINE_BTN", self.car_controller)
        execute_command_callback("LEFT_DOOR_OPEN", self.car_controller)
        execute_command_callback("LOCK", self.car_controller)
        self.assertFalse(self.car_controller.get_lock_status())

    def test_lock_right_door_open(self):
        """LOCK 실패 조건: 오른쪽 문 열림 -> 잠기지 않음"""
        execute_command_callback("UNLOCK", self.car_controller)
        execute_command_callback("ENGINE_BTN", self.car_controller)
        execute_command_callback("RIGHT_DOOR_OPEN", self.car_controller)
        execute_command_callback("LOCK", self.car_controller)
        self.assertFalse(self.car_controller.get_lock_status())

    def test_lock_trunk_open(self):
        """LOCK 실패 조건: 트렁크 열림 -> 잠기지 않음"""
        execute_command_callback("UNLOCK", self.car_controller)
        execute_command_callback("ENGINE_BTN", self.car_controller)
        execute_command_callback("TRUNK_OPEN", self.car_controller)
        execute_command_callback("LOCK", self.car_controller)
        self.assertFalse(self.car_controller.get_lock_status())

class TestUnlock(unittest.TestCase):

    def setUp(self):
        self.car = Car()
        self.car_controller = CarController(self.car)

    def test_unlock_normal(self):
        """UNLOCK 정상 조건: 잠김 상태 -> 잠금 해제"""
        execute_command_callback("LOCK", self.car_controller)
        execute_command_callback("UNLOCK", self.car_controller)
        self.assertFalse(self.car_controller.get_lock_status())

    def test_unlock_already_unlocked(self):
        """UNLOCK: 이미 잠금 해제 상태 -> 상태 변화 없음"""
        execute_command_callback("UNLOCK", self.car_controller)
        self.assertFalse(self.car_controller.get_lock_status())

class TestAccelerate(unittest.TestCase): #가속 테스트 케이스
    def setUp(self):
        self.car = Car()
        self.car_controller = CarController(self.car)

    #test case1 : 시스템의 상태 여부 확인하고 가속하는지 / 10km/h 초과 속도 올라가면 문 닫기
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

        #시속이 10km 초과한 경우이므로 문이 닫혀있어야 한다.
        self.assertEqual(self.car_controller.get_left_door_status(), "CLOSED")
        self.assertEqual(self.car_controller.get_right_door_status(), "CLOSED")


    #test case2 : 엔진의 상태 여부 확인하고 가속하는지 / 10km/h 이상 속도 올라가면 문 닫기
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

        #시속이 10km 초과한 경우이므로 문이 닫혀있어야 한다.
        self.assertEqual(self.car_controller.get_left_door_status(), "CLOSED")
        self.assertEqual(self.car_controller.get_right_door_status(), "CLOSED")

    #test case3 : 문의 상태 확인 / 트렁크의 상태 확인 / 최대 제한 속도 확인 / 속도에 따른 여부 확인
    def test_Accelerate_when_trunk_door(self):

        execute_command_callback("UNLOCK", self.car_controller)
        execute_command_callback("ENGINE_BTN", self.car_controller)
        #트렁크 상태에 따른 가속 명령을 확인 하기위해 열고 가속
        execute_command_callback("TRUNK_OPEN", self.car_controller)

        #문의 상태 확인 (현재 속도가 20km/h인 경우)
        for i in range(2):
            execute_command_callback("ACCELERATE", self.car_controller)
        self.assertEqual(self.car_controller.get_speed(), 20)

        #문이 제대로 닫혀있나 확인
        self.assertEqual(self.car_controller.get_left_door_status(), "CLOSED")
        self.assertEqual(self.car_controller.get_right_door_status(), "CLOSED")

        #문 잠금 상태 확인 후 잠그기 / 20km/h 일때 가속한 경우
        execute_command_callback("ACCELERATE", self.car_controller)
        self.assertEqual(self.car_controller.get_speed(), 30)

        #문은 잠김 상태여야 한다.
        self.assertEqual(self.car_controller.get_left_door_lock(), "LOCKED")
        self.assertEqual(self.car_controller.get_right_door_lock(), "LOCKED")

        #현재 속도가 30km/h인 경우 트렁크 확인 후 가속

        #현재 트렁크 열린 경우 이므로 속도 안 변함
        execute_command_callback("ACCELERATE", self.car_controller)
        self.assertEqual(self.car_controller.get_speed(), 30)

        #트렁크 닫고 다시 가속하면 속도 변함
        execute_command_callback("TRUNK_CLOSE", self.car_controller)
        self.assertTrue(self.car_controller.get_trunk_status(), "TRUNK_CLOSE")
        execute_command_callback("ACCELERATE", self.car_controller)
        self.assertEqual(self.car_controller.get_speed(), 40)

        #최대 제한 속도에 도달한 경우 확인
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
        execute_command_callback("RIGHT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car_controller.get_right_door_status(), "CLOSED")

        # 전체 잠금을 해제한 후 문을 열 수 있는지 확인
        execute_command_callback("UNLOCK", self.car_controller)
        self.assertFalse(self.car_controller.get_lock_status())
        execute_command_callback("LEFT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_status(), "CLOSED")
        execute_command_callback("RIGHT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car_controller.get_right_door_status(), "CLOSED")

        execute_command_callback("LEFT_DOOR_UNLOCK", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_lock(), "UNLOCKED")
        execute_command_callback("LEFT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_status(), "OPEN")

        execute_command_callback("RIGHT_DOOR_UNLOCK", self.car_controller)
        self.assertEqual(self.car_controller.get_right_door_lock(), "UNLOCKED")
        execute_command_callback("RIGHT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car_controller.get_right_door_status(), "OPEN")

    def test_door_operations_at_various_speeds(self):
    # 0km: 문을 열고 닫는 데 제한이 없는지 확인
        execute_command_callback("UNLOCK", self.car_controller)
        execute_command_callback("LEFT_DOOR_UNLOCK", self.car_controller)
        execute_command_callback("LEFT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_status(), "OPEN")
        execute_command_callback("LEFT_DOOR_CLOSE", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_status(), "CLOSED")

        execute_command_callback("RIGHT_DOOR_UNLOCK", self.car_controller)
        execute_command_callback("RIGHT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car_controller.get_right_door_status(), "OPEN")
        execute_command_callback("RIGHT_DOOR_CLOSE", self.car_controller)
        self.assertEqual(self.car_controller.get_right_door_status(), "CLOSED")

        # 10km: 문을 열고 닫는 데 제한이 없는지 확인
        self.assertEqual(self.car_controller.get_lock_status(), False)
        execute_command_callback("ENGINE_BTN", self.car_controller)
        execute_command_callback("ACCELERATE", self.car_controller)  # 속도 +10km
        self.assertEqual(self.car_controller.get_speed(), 10)
        execute_command_callback("LEFT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_status(), "OPEN")
        execute_command_callback("LEFT_DOOR_CLOSE", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_status(), "CLOSED")

        execute_command_callback("RIGHT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car_controller.get_right_door_status(), "OPEN")
        execute_command_callback("RIGHT_DOOR_CLOSE", self.car_controller)
        self.assertEqual(self.car_controller.get_right_door_status(), "CLOSED")

        # 20km 초과 (30km): 문이 잠기고 열리지 않아야 함
        execute_command_callback("ACCELERATE", self.car_controller)  # 속도 +10km
        execute_command_callback("ACCELERATE", self.car_controller)  # 속도 +10km (합계 30km)
        self.assertEqual(self.car_controller.get_speed(), 30)

        execute_command_callback("LEFT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_status(), "CLOSED")  # 열리지 않음
        self.assertEqual(self.car_controller.get_left_door_lock(), "LOCKED")  # 문이 잠겨야 함

        execute_command_callback("RIGHT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car_controller.get_right_door_status(), "CLOSED")  # 열리지 않음
        self.assertEqual(self.car_controller.get_right_door_lock(), "LOCKED")  # 문이 잠겨야 함

    # 3. 문이 잠겨있거나 잠금 해제된 상태 테스트
    def test_door_lock_unlock_status(self):
        # 왼쪽 문: 문이 잠금 해제된 상태에서 문 열기 시도
        execute_command_callback("UNLOCK", self.car_controller)
        self.car_controller.unlock_left_door()
        execute_command_callback("LEFT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_status(), "OPEN")
        execute_command_callback("LEFT_DOOR_CLOSE", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_status(), "CLOSED")

        # 오른쪽 문: 문이 잠금 해제된 상태에서 문 열기 시도
        self.car_controller.unlock_right_door()
        execute_command_callback("RIGHT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car_controller.get_right_door_status(), "OPEN")
        execute_command_callback("RIGHT_DOOR_CLOSE", self.car_controller)
        self.assertEqual(self.car_controller.get_right_door_status(), "CLOSED")

        # 문이 잠겨있는 상태에서 문 열기 시도
        self.car_controller.lock_left_door()
        execute_command_callback("LEFT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_status(), "CLOSED")  # 열리지 않아야 함

        self.car_controller.lock_right_door()
        execute_command_callback("RIGHT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car_controller.get_right_door_status(), "CLOSED")  # 열리지 않아야 함

    # 4. 문이 이미 열려있거나 닫혀있는 상태에서의 동작 확인
    def test_open_close_when_already_open_or_closed(self):
        # 왼쪽 문 검사
        execute_command_callback("UNLOCK", self.car_controller)
        self.car_controller.unlock_left_door()
        execute_command_callback("LEFT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_status(), "OPEN")
        execute_command_callback("LEFT_DOOR_OPEN", self.car_controller)  # 이미 열린 상태에서 열기 시도
        self.assertEqual(self.car_controller.get_left_door_status(), "OPEN")  # 상태 유지

        execute_command_callback("LEFT_DOOR_CLOSE", self.car_controller)
        self.assertEqual(self.car_controller.get_left_door_status(), "CLOSED")
        execute_command_callback("LEFT_DOOR_CLOSE", self.car_controller)  # 이미 닫힌 상태에서 닫기 시도
        self.assertEqual(self.car_controller.get_left_door_status(), "CLOSED")  # 상태 유지

        # 오른쪽 문 검사
        self.car_controller.unlock_right_door()
        execute_command_callback("RIGHT_DOOR_OPEN", self.car_controller)
        self.assertEqual(self.car_controller.get_right_door_status(), "OPEN")
        execute_command_callback("RIGHT_DOOR_OPEN", self.car_controller)  # 이미 열린 상태에서 열기 시도
        self.assertEqual(self.car_controller.get_right_door_status(), "OPEN")  # 상태 유지

        execute_command_callback("RIGHT_DOOR_CLOSE", self.car_controller)
        self.assertEqual(self.car_controller.get_right_door_status(), "CLOSED")
        execute_command_callback("RIGHT_DOOR_CLOSE", self.car_controller)  # 이미 닫힌 상태에서 닫기 시도
        self.assertEqual(self.car_controller.get_right_door_status(), "CLOSED")  # 상태 유지

class TestTempLockSystem(unittest.TestCase):

    def setUp(self):
        self.car = Car()
        self.car_controller = CarController(self.car)

    # 1. 왼쪽 문이 열린 상태에서 잠금 시도 시 temp_lock을 통해 잠금이 동작되는지 확인
    def test_left_door_temp_lock(self):
        global left_temp
        execute_command_callback("UNLOCK", self.car_controller)
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
        execute_command_callback("UNLOCK", self.car_controller)
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


class TestCarTrunk(unittest.TestCase):
    def setUp(self):
        self.car = Car()
        self.car_controller = CarController(self.car)

    def test_trunk_open_callback(self):
        execute_command_callback("UNLOCK", self.car_controller)
        self.assertTrue(self.car_controller.get_trunk_status())  # 초기 상태 확인
        execute_command_callback("TRUNK_OPEN", self.car_controller)  # 트렁크 열기
        self.assertFalse(self.car_controller.get_trunk_status())  # 트렁크 열린 상태 확인

    def test_trunk_close_directly(self):
        execute_command_callback("UNLOCK", self.car_controller)
        execute_command_callback("TRUNK_OPEN", self.car_controller)
        self.assertFalse(self.car_controller.get_trunk_status())  # 트렁크 열린 상태 확인
        execute_command_callback("TRUNK_CLOSE", self.car_controller)
        self.assertTrue(self.car_controller.get_trunk_status())  # 트렁크 닫힘 상태 확인

    def test_trunk_speed_limit_with_callback(self):
        execute_command_callback("UNLOCK", self.car_controller)
        execute_command_callback("TRUNK_OPEN", self.car_controller)
        self.assertFalse(self.car_controller.get_trunk_status())
        execute_command_callback("ENGINE_BTN", self.car_controller)
        execute_command_callback("ACCELERATE", self.car_controller)
        execute_command_callback("ACCELERATE", self.car_controller)
        execute_command_callback("ACCELERATE", self.car_controller)
        self.assertEqual(self.car_controller.get_speed(), 30)   # 속도 확인
        execute_command_callback("ACCELERATE", self.car_controller)  # 트렁크 열린 상태에서 가속 시도
        self.assertEqual(self.car_controller.get_speed(), 30)  # 속도 유지 확인
        execute_command_callback("TRUNK_CLOSE", self.car_controller)
        self.assertTrue(self.car_controller.get_trunk_status())
        execute_command_callback("ACCELERATE", self.car_controller)
        execute_command_callback("ACCELERATE", self.car_controller)
        self.assertEqual(self.car_controller.get_speed(), 50)
        

    def test_trunk_speed_allowance_below_limit_with_callback(self):
        execute_command_callback("UNLOCK", self.car_controller)
        execute_command_callback("TRUNK_OPEN", self.car_controller)
        self.assertFalse(self.car_controller.get_trunk_status())
        execute_command_callback("ENGINE_BTN", self.car_controller)
        execute_command_callback("ACCELERATE", self.car_controller)
        execute_command_callback("ACCELERATE", self.car_controller)
        self.assertEqual(self.car_controller.get_speed(), 20)
        execute_command_callback("ACCELERATE", self.car_controller)  # 트렁크 열린 상태에서 제한 속도 이내 가속 시도
        self.assertEqual(self.car_controller.get_speed(), 30)  # 속도가 10 증가했는지 확인
        
    def test_trunk_car_status_lock(self):
        execute_command_callback("LOCK", self.car_controller)
        execute_command_callback("TRUNK_OPEN", self.car_controller)
        self.assertTrue(self.car_controller.get_trunk_status())