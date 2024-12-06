import unittest
from car import Car
from car_controller import CarController
from main import execute_command_callback
from main import get_left_temp, get_right_temp



# class TestEngineToggle(unittest.TestCase):
#     def setUp(self):
#         self.car = Car()  # Car 클래스 인스턴스 생성
#         self.car_controller = CarController(self.car)  # CarController 인스턴스 생성

#     def test_engine_start_with_brake(self):
#         """브레이크를 밟은 상태에서 엔진 버튼을 누르면 엔진이 켜져야 함."""
#         self.car_controller.unlock_vehicle()
#         self.assertFalse(self.car_controller.get_engine_status())

#         execute_command_callback("BRAKE ENGINE_BTN", self.car_controller)

#         self.assertTrue(self.car_controller.get_engine_status())

#     def test_engine_start_without_brake(self):
#         """브레이크를 밟지 않고 엔진 버튼을 누르면 엔진이 켜지지 않아야 함."""
#         self.car_controller.unlock_vehicle()
#         self.assertFalse(self.car_controller.get_engine_status())

#         execute_command_callback("ENGINE_BTN", self.car_controller)

#         self.assertFalse(self.car_controller.get_engine_status())

#     # 차량 전체 잠금 해제 상태일 때, 엔진 토글이 작동하는 지 확인
#     def test_engine_when_unlocked(self):
#         self.car_controller.unlock_vehicle()
#         self.assertFalse(self.car_controller.get_engine_status())

#         execute_command_callback("ENGINE_BTN", self.car_controller)
#         self.assertTrue(self.car_controller.get_engine_status())

#         execute_command_callback("ENGINE_BTN", self.car_controller)
#         self.assertFalse(self.car_controller.get_engine_status())

#     # 차량 전체 잠금 상태일때, 엔진 토글이 작동하지 않음을 확인.
#     def test_engine_when_locked(self):
#         self.car_controller.lock_vehicle()
#         self.assertFalse(self.car_controller.get_engine_status())

#         execute_command_callback("ENGINE_BTN", self.car_controller)
#         self.assertFalse(self.car_controller.get_engine_status())

#     # 차량이 가속 중 일때, 엔진 토글이 작동하지 않음을 확인(엔진이 OFF 되는지)
#     def test_engine_when_accelerating(self):
#         self.car_controller.unlock_vehicle()
#         self.assertFalse(self.car_controller.get_engine_status())

#         execute_command_callback("ENGINE_BTN", self.car_controller)
#         self.assertTrue(self.car_controller.get_engine_status())

#         self.car_controller.accelerate()
#         self.assertTrue(self.car_controller.get_engine_status())

#         execute_command_callback("ENGINE_BTN", self.car_controller)
#         self.assertTrue(self.car_controller.get_engine_status())

#     # 차량이 가속 후 정지 했을 때, 엔진 토글이 작동하는지 확인
#     def test_engine_when_stop(self):

#         self.car_controller.unlock_vehicle()
#         self.assertFalse(self.car_controller.get_engine_status())

#         execute_command_callback("ENGINE_BTN", self.car_controller)
#         self.assertTrue(self.car_controller.get_engine_status())

#         self.car_controller.accelerate()
#         self.assertTrue(self.car_controller.get_engine_status())

#         execute_command_callback("ENGINE_BTN", self.car_controller)
#         self.assertTrue(self.car_controller.get_engine_status())

#         self.car_controller.brake()
#         self.assertTrue(self.car_controller.get_engine_status())

#         execute_command_callback("ENGINE_BTN", self.car_controller)
#         self.assertFalse(self.car_controller.get_engine_status())


# class TestSOS(unittest.TestCase):
#     """
#     1. 차를 정지(speed=0)시켜야 함
#     2. 모든 문의 잠금 상태를 열림(left_door_lock="UNLOCKED"&right_door_lock="UNLOCKED")으로
#     3. 모든 문을 열어야 함(left_door_status="OPEN"&right_door_status="OPEN")
#     4. 트렁크가 열려야 함(trunk_status=false)
#     """

#     def setUp(self):
#         self.car = Car()
#         self.car_controller = CarController(self.car)

#     def test_sos_normal(self):
#         """
#         가속상황에서
#         SOS 기능 정상 작동 테스트: 정지, 모든 문/트렁크 열림
#         """
#         execute_command_callback("UNLOCK", self.car_controller)
#         execute_command_callback("ENGINE_BTN", self.car_controller)
#         execute_command_callback("ACCELERATE", self.car_controller)

#         execute_command_callback("SOS", self.car_controller)

#         self.assertEqual(self.car.speed, 0)
#         self.assertEqual(self.car.left_door_lock, "UNLOCKED")
#         self.assertEqual(self.car.right_door_lock, "UNLOCKED")
#         self.assertEqual(self.car.left_door_status, "OPEN")
#         self.assertEqual(self.car.right_door_status, "OPEN")
#         self.assertFalse(self.car.trunk_status)

#     def test_sos_already_stopped(self):
#         """
#         정지상황에서
#         SOS 기능: 이미 정지 상태일 때도 모든 문/트렁크 열림
#         """

#         execute_command_callback("SOS", self.car_controller)

#         self.assertEqual(self.car.speed, 0)
#         self.assertEqual(self.car.left_door_lock, "UNLOCKED")
#         self.assertEqual(self.car.right_door_lock, "UNLOCKED")
#         self.assertEqual(self.car.left_door_status, "OPEN")
#         self.assertEqual(self.car.right_door_status, "OPEN")
#         self.assertFalse(self.car.trunk_status)

# class TestLock(unittest.TestCase):
#     '''
#     엔진 꺼져있고, 모든 문 닫혀 있고, 트렁크 닫혀 있으면 → 접근 제한 잠금 수행
#     '''

#     def setUp(self):
#         self.car = Car()
#         self.car_controller = CarController(self.car)

#     def test_lock_normal(self):
#         """정상적인 LOCK 조건: 엔진 꺼짐, 모든 문/트렁크 닫힘 -> 잠김"""
#         execute_command_callback("UNLOCK", self.car_controller)
#         execute_command_callback("ENGINE_BTN", self.car_controller)
#         execute_command_callback("LEFT_DOOR_CLOSE", self.car_controller)
#         execute_command_callback("RIGHT_DOOR_CLOSE", self.car_controller)
#         execute_command_callback("RIGHT_DOOR_CLOSE", self.car_controller)
#         execute_command_callback("TRUNK_CLOSE", self.car_controller)
#         self.assertFalse(self.car_controller.get_lock_status())

#     def test_lock_engine_on(self):
#         """LOCK 실패 조건: 엔진 켜짐 -> 잠기지 않음"""
#         execute_command_callback("UNLOCK", self.car_controller)
#         execute_command_callback("ENGINE_BTN", self.car_controller)
#         execute_command_callback("LOCK", self.car_controller)
#         self.assertFalse(self.car_controller.get_lock_status())

#     def test_lock_left_door_open(self):
#         """LOCK 실패 조건: 왼쪽 문 열림 -> 잠기지 않음"""
#         execute_command_callback("UNLOCK", self.car_controller)
#         execute_command_callback("ENGINE_BTN", self.car_controller)
#         execute_command_callback("LEFT_DOOR_OPEN", self.car_controller)
#         execute_command_callback("LOCK", self.car_controller)
#         self.assertFalse(self.car_controller.get_lock_status())

#     def test_lock_right_door_open(self):
#         """LOCK 실패 조건: 오른쪽 문 열림 -> 잠기지 않음"""
#         execute_command_callback("UNLOCK", self.car_controller)
#         execute_command_callback("ENGINE_BTN", self.car_controller)
#         execute_command_callback("RIGHT_DOOR_OPEN", self.car_controller)
#         execute_command_callback("LOCK", self.car_controller)
#         self.assertFalse(self.car_controller.get_lock_status())

#     def test_lock_trunk_open(self):
#         """LOCK 실패 조건: 트렁크 열림 -> 잠기지 않음"""
#         execute_command_callback("UNLOCK", self.car_controller)
#         execute_command_callback("ENGINE_BTN", self.car_controller)
#         execute_command_callback("TRUNK_OPEN", self.car_controller)
#         execute_command_callback("LOCK", self.car_controller)
#         self.assertFalse(self.car_controller.get_lock_status())

# class TestUnlock(unittest.TestCase):

#     def setUp(self):
#         self.car = Car()
#         self.car_controller = CarController(self.car)

#     def test_unlock_normal(self):
#         """UNLOCK 정상 조건: 잠김 상태 -> 잠금 해제"""
#         execute_command_callback("LOCK", self.car_controller)
#         execute_command_callback("UNLOCK", self.car_controller)
#         self.assertFalse(self.car_controller.get_lock_status())

#     def test_unlock_already_unlocked(self):
#         """UNLOCK: 이미 잠금 해제 상태 -> 상태 변화 없음"""
#         execute_command_callback("UNLOCK", self.car_controller)
#         self.assertFalse(self.car_controller.get_lock_status())

# class TestAccelerate(unittest.TestCase): #가속 테스트 케이스
#     def setUp(self):
#         self.car = Car()
#         self.car_controller = CarController(self.car)

#     #test case1 : 시스템의 상태 여부 확인하고 가속하는지 / 10km/h 초과 속도 올라가면 문 닫기
#     def test_Accelerate_when_unlocked(self):

#         # 전체 잠금이 되어 있는 경우
#         execute_command_callback("LOCK", self.car_controller)
#         self.assertTrue(self.car_controller.get_lock_status())
#         execute_command_callback("ACCELERATE", self.car_controller)
#         #속도 변화가 없어야 한다
#         self.assertEqual(self.car_controller.get_speed(), 0)

#         # 전체 잠금이 해제 되어 있는 경우
#         execute_command_callback("UNLOCK", self.car_controller)
#         self.assertFalse(self.car_controller.get_lock_status())
#         execute_command_callback("ENGINE_BTN", self.car_controller)

#         #속도가 높아져야 한다 1 (현재 속도가 0인 경우)
#         execute_command_callback("ACCELERATE", self.car_controller)
#         self.assertEqual(self.car_controller.get_speed(), 10)

#         #속도가 높아져야 한다 2 (현재 속도가 10인 경우)
#         execute_command_callback("ACCELERATE", self.car_controller)
#         self.assertEqual(self.car_controller.get_speed(), 20)

#         #시속이 10km 초과한 경우이므로 문이 닫혀있어야 한다.
#         self.assertEqual(self.car_controller.get_left_door_status(), "CLOSED")
#         self.assertEqual(self.car_controller.get_right_door_status(), "CLOSED")


#     #test case2 : 엔진의 상태 여부 확인하고 가속하는지 / 10km/h 이상 속도 올라가면 문 닫기
#     def test_Accelerate_when_engine(self):

#         # 엔진이 꺼져있는 경우
#         execute_command_callback("UNLOCK", self.car_controller)
#         self.assertFalse(self.car_controller.get_lock_status())

#         #속도 변화가 없어야 한다
#         execute_command_callback("ACCELERATE", self.car_controller)
#         self.assertEqual(self.car_controller.get_speed(), 0)

#         execute_command_callback("ENGINE_BTN", self.car_controller)
#         #속도가 높아져야 한다 1 (현재 속도가 0인 경우)
#         execute_command_callback("ACCELERATE", self.car_controller)
#         self.assertEqual(self.car_controller.get_speed(), 10)

#         #속도가 높아져야 한다 2 (현재 속도가 10인 경우)
#         execute_command_callback("ACCELERATE", self.car_controller)
#         self.assertEqual(self.car_controller.get_speed(), 20)

#         #시속이 10km 초과한 경우이므로 문이 닫혀있어야 한다.
#         self.assertEqual(self.car_controller.get_left_door_status(), "CLOSED")
#         self.assertEqual(self.car_controller.get_right_door_status(), "CLOSED")

#     #test case3 : 문의 상태 확인 / 트렁크의 상태 확인 / 최대 제한 속도 확인 / 속도에 따른 여부 확인
#     def test_Accelerate_when_trunk_door(self):

#         execute_command_callback("UNLOCK", self.car_controller)
#         execute_command_callback("ENGINE_BTN", self.car_controller)
#         #트렁크 상태에 따른 가속 명령을 확인 하기위해 열고 가속
#         execute_command_callback("TRUNK_OPEN", self.car_controller)

#         #문의 상태 확인 (현재 속도가 20km/h인 경우)
#         for i in range(2):
#             execute_command_callback("ACCELERATE", self.car_controller)
#         self.assertEqual(self.car_controller.get_speed(), 20)

#         #문이 제대로 닫혀있나 확인
#         self.assertEqual(self.car_controller.get_left_door_status(), "CLOSED")
#         self.assertEqual(self.car_controller.get_right_door_status(), "CLOSED")

#         #문 잠금 상태 확인 후 잠그기 / 20km/h 일때 가속한 경우
#         execute_command_callback("ACCELERATE", self.car_controller)
#         self.assertEqual(self.car_controller.get_speed(), 30)

#         #문은 잠김 상태여야 한다.
#         self.assertEqual(self.car_controller.get_left_door_lock(), "LOCKED")
#         self.assertEqual(self.car_controller.get_right_door_lock(), "LOCKED")

#         #현재 속도가 30km/h인 경우 트렁크 확인 후 가속

#         #현재 트렁크 열린 경우 이므로 속도 안 변함
#         execute_command_callback("ACCELERATE", self.car_controller)
#         self.assertEqual(self.car_controller.get_speed(), 30)

#         #트렁크 닫고 다시 가속하면 속도 변함
#         execute_command_callback("TRUNK_CLOSE", self.car_controller)
#         self.assertTrue(self.car_controller.get_trunk_status(), "TRUNK_CLOSE")
#         execute_command_callback("ACCELERATE", self.car_controller)
#         self.assertEqual(self.car_controller.get_speed(), 40)

#         #최대 제한 속도에 도달한 경우 확인
#         for i in range(16):
#             execute_command_callback("ACCELERATE", self.car_controller)
#         self.assertEqual(self.car_controller.get_speed(), 200)

#         #속도가 높아지지 않는다 (최대 속도에 도달한 경우)
#         execute_command_callback("ACCELERATE", self.car_controller)
#         self.assertEqual(self.car_controller.get_speed(), 200)

###############################################################

class TestBrake(unittest.TestCase): #감속 테스트 케이스
    def setUp(self):
        self.car = Car()
        self.car_controller = CarController(self.car)

    # test case 1 : 전체 잠금 LOCKED 일 때
    def test_brake_when_locked(self):
        # Given
        self.car_controller.lock_vehicle()
        # When
        execute_command_callback("BRAKE", self.car_controller)
        # Then : 속도 변화가 없어야 한다
        self.assertEqual(self.car_controller.get_speed(), 0)

    # test case 2 : 엔진 OFF 일 때
    def test_brake_when_engine_off(self):
        # Given
        self.car_controller.unlock_vehicle()
        # When
        execute_command_callback("BRAKE", self.car_controller)
        # Then : 속도 변화가 없어야 한다
        self.assertEqual(self.car_controller.get_speed(), 0)

    # test case 3 : speed 0 일 때
    def test_brake_when_speed_0(self):
        # Given
        self.car_controller.unlock_vehicle()
        self.car_controller.toggle_engine()
        # When
        execute_command_callback("BRAKE", self.car_controller)
        # Then : 속도 변화가 없어야 한다
        self.assertEqual(self.car_controller.get_speed(), 0)

    # test case 4 : speed >= 10 일 때
    def test_brake_when_speed_is_fater_than_0(self):
        # Given
        self.car_controller.unlock_vehicle()
        self.car_controller.toggle_engine()
        self.car_controller.accelerate()
        self.car_controller.accelerate()
        # When
        execute_command_callback("BRAKE", self.car_controller)
        # Then : 속도 20 -> 10
        self.assertEqual(self.car_controller.get_speed(), 10)


class TestCarDoorLockSystem(unittest.TestCase):
    def setUp(self):
        self.car = Car()  # Car 클래스 인스턴스 생성
        self.car_controller = CarController(self.car)  # CarController 인스턴스 생성

    #LEFT_DOOR_LOCK

    # test case 1 : 전체 잠금 LOCKED 일 때 LEFT_DOOR_LOCK 
    def test_left_door_lock_when_locked(self):
        # Given
        self.car_controller.lock_vehicle()
        # When
        execute_command_callback("LEFT_DOOR_LOCK", self.car_controller)
        # Then
        self.assertEqual(self.car_controller.get_left_door_lock(), "LOCKED")

    # test case 2 : 전체 잠금 UNLOCKED 일 때 LEFT_DOOR_LOCK
    def test_left_door_lock_when_unlocked(self):
        # Given
        self.car_controller.unlock_vehicle()
        # When
        execute_command_callback("LEFT_DOOR_LOCK", self.car_controller)
        # Then
        self.assertEqual(self.car_controller.get_left_door_lock(), "LOCKED")

    # test case 3 : 문이 LOCKED일때 LEFT_DOOR_LOCK
    def test_right_door_unlock_when_door_locked(self):
        # Given
        self.car_controller.unlock_vehicle()
        self.car_controller.lock_left_door()
        # When
        execute_command_callback("LEFT_DOOR_LOCK", self.car_controller)
        # Then
        self.assertEqual(self.car_controller.get_left_door_lock(), "LOCKED")

    # test case 4 : 차량 잠금이 UNLOCKED이고 문이 OPEN일 때 LEFT_DOOR_LOCK
    def test_left_door_lock_when_door_open(self):
        # Given
        self.car_controller.unlock_vehicle()
        self.car_controller.unlock_left_door()
        self.car_controller.open_left_door()

        # When
        execute_command_callback("LEFT_DOOR_LOCK", self.car_controller)
        # Then
        self.assertEqual(get_left_temp(), "LOCKED")
        self.assertEqual(self.car_controller.get_left_door_lock(), "UNLOCKED")

    # LEFT_DOOR_UNLOCK

    # test case 5 : 전체 잠금 LOCKED 일 때 LEFT_DOOR_UNLOCK
    def test_left_door_unlock_when_locked(self):
        # Given
        self.car_controller.lock_vehicle()
        # When
        execute_command_callback("LEFT_DOOR_UNLOCK", self.car_controller)
        # Then
        self.assertEqual(self.car_controller.get_left_door_lock(), "LOCKED")

    # test case 6 : 전체 잠금 UNLOCKED 일 때 LEFT_DOOR_UNLOCK
    def test_left_door_unlock_when_unlocked(self):
        # Given
        self.car_controller.unlock_vehicle()
        # When
        execute_command_callback("LEFT_DOOR_UNLOCK", self.car_controller)
        # Then
        self.assertEqual(self.car_controller.get_left_door_lock(), "UNLOCKED")

    # test case 7 : 문이 OPEN일 때 LEFT_DOOR_UNLOCK
    def test_left_door_unlock_when_door_open(self):
        # Given
        self.car_controller.unlock_vehicle()
        self.car_controller.unlock_left_door()
        self.car_controller.open_left_door()
        # When
        execute_command_callback("LEFT_DOOR_UNLOCK", self.car_controller)
        # Then
        self.assertEqual(get_left_temp(), "UNLOCKED")
        self.assertEqual(self.car_controller.get_left_door_lock(), "UNLOCKED")

    # test case 8 : 문이 이미 UNLOCKED 일 때 LEFT_DOOR_UNLOCK
    def test_left_door_unlock_when_door_is_already_unlocked(self):
        # Given
        self.car_controller.unlock_vehicle()
        self.car_controller.unlock_left_door()

        # When
        execute_command_callback("LEFT_DOOR_UNLOCK", self.car_controller)

        # Then
        self.assertEqual(self.car_controller.get_left_door_lock(), "UNLOCKED")

    # test case 9 : 속도가 20보다 빠를 때 LEFT_DOOR_UNLOCK
    def test_left_door_unlock_when_speed_is_faster_than_20(self):
        # Given
        self.car_controller.unlock_vehicle()
        self.car_controller.toggle_engine()
        self.car_controller.accelerate()
        self.car_controller.accelerate()
        self.car_controller.accelerate()
        # When
        execute_command_callback("LEFT_DOOR_UNLOCK", self.car_controller)
        # Then
        self.assertEqual(self.car_controller.get_left_door_lock(), "LOCKED")

    # RIGHT_DOOR_LOCK

    # test case 10 : 전체 잠금 LOCKED 일 때 RIGHT_DOOR_LOCK
    def test_right_door_lock_when_locked(self):
        # Given
        self.car_controller.lock_vehicle()
        # When
        execute_command_callback("RIGHT_DOOR_LOCK", self.car_controller)
        # Then
        self.assertEqual(self.car_controller.get_right_door_lock(), "LOCKED")
    
    # test case 11 : 전체 잠금 UNLOCKED 일 때 RIGHT_DOOR_LOCK
    def test_right_door_lock_when_unlocked(self):
        # Given
        self.car_controller.unlock_vehicle()
        # When
        execute_command_callback("RIGHT_DOOR_LOCK", self.car_controller)
        # Then
        self.assertEqual(self.car_controller.get_right_door_lock(), "LOCKED")
    
    # test case 12 : 문이 LOCKED일때 RIGHT_DOOR_LOCK
    def test_right_door_unlock_when_door_locked(self):
        # Given
        self.car_controller.unlock_vehicle()
        self.car_controller.lock_right_door()
        # When
        execute_command_callback("RIGHT_DOOR_LOCK", self.car_controller)
        # Then
        self.assertEqual(self.car_controller.get_right_door_lock(), "LOCKED")
    
    # test case 13 : 차량 잠금이 UNLOCKED이고 문이 OPEN일 때 RIGHT_DOOR_LOCK
    def test_right_door_lock_when_door_open(self):
        # Given
        self.car_controller.unlock_vehicle()
        self.car_controller.unlock_right_door()
        self.car_controller.open_right_door()
        # When
        execute_command_callback("RIGHT_DOOR_LOCK", self.car_controller)
        # Then
        self.assertEqual(get_right_temp(), "LOCKED")
        self.assertEqual(self.car_controller.get_right_door_lock(), "UNLOCKED")

    # RIGHT_DOOR_UNLOCK

    # test case 14 : 전체 잠금 LOCKED 일 때 RIGHT_DOOR_UNLOCK
    def test_right_door_unlock_when_locked(self):
        # Given
        self.car_controller.lock_vehicle()
        # When
        execute_command_callback("RIGHT_DOOR_UNLOCK", self.car_controller)
        # Then
        self.assertEqual(self.car_controller.get_right_door_lock(), "LOCKED")

    # test case 15 : 전체 잠금 UNLOCKED 일 때 RIGHT_DOOR_UNLOCK
    def test_right_door_unlock_when_unlocked(self):
        # Given
        self.car_controller.unlock_vehicle()
        # When
        execute_command_callback("RIGHT_DOOR_UNLOCK", self.car_controller)
        # Then
        self.assertEqual(self.car_controller.get_right_door_lock(), "UNLOCKED")

    # test case 16 : 차량 잠금이 UNLOCKED이고, 문이 OPEN일 때 RIGHT_DOOR_UNLOCK
    def test_right_door_unlock_when_door_open(self):
        # Given
        self.car_controller.unlock_vehicle()
        self.car_controller.unlock_right_door()
        self.car_controller.open_right_door()
        # When
        execute_command_callback("RIGHT_DOOR_UNLOCK", self.car_controller)
        # Then
        self.assertEqual(get_right_temp(), "UNLOCKED")
        self.assertEqual(self.car_controller.get_right_door_lock(), "UNLOCKED")
    
    # test case 18 : 문이 이미 UNLOCKED 일 때 RIGHT_DOOR_UNLOCK
    def test_right_door_unlock_when_door_is_already_unlocked(self):
        # Given
        self.car_controller.unlock_vehicle()
        self.car_controller.unlock_right_door()

        # When
        execute_command_callback("RIGHT_DOOR_UNLOCK", self.car_controller)

        # Then
        self.assertEqual(self.car_controller.get_right_door_lock(), "UNLOCKED")

    # test case 19 : 속도가 20보다 빠를 때 RIGHT_DOOR_UNLOCK
    def test_right_door_unlock_when_speed_is_faster_than_20(self):
        # Given
        self.car_controller.unlock_vehicle()
        self.car_controller.toggle_engine()
        self.car_controller.accelerate()
        self.car_controller.accelerate()
        self.car_controller.accelerate()
        # When
        execute_command_callback("RIGHT_DOOR_UNLOCK", self.car_controller)
        # Then
        self.assertEqual(self.car_controller.get_right_door_lock(), "LOCKED")

class TestCarDoorOpenSystem(unittest.TestCase):
    def setUp(self):
        self.car = Car()  # Car 클래스 인스턴스 생성
        self.car_controller = CarController(self.car)  # CarController 인스턴스 생성
    
    # LEFT_DOOR_OPEN

    # test case 1 : 전체 잠금 LOCKED 일 때 LEFT_DOOR_OPEN
    def test_left_door_open_when_locked(self):
        # Given
        self.car_controller.lock_vehicle()
        # When
        execute_command_callback("LEFT_DOOR_OPEN",self.car_controller)
        # Then
        self.assertEqual(self.car_controller.get_left_door_status(), "CLOSED")

    # test case 2 : 문이 LOCKED 일 때 LEFT_DOOR_OPEN
    def test_left_door_open_when_door_locked_with_closed_door(self):
        # Given
        self.car_controller.unlock_vehicle()
        self.car_controller.lock_left_door()
        # When
        execute_command_callback("LEFT_DOOR_OPEN",self.car_controller)
        # Then
        self.assertEqual(self.car_controller.get_left_door_status(), "CLOSED")

    # test case 3 : 문이 UNLOCKED 일 때 LEFT_DOOR_OPEN
    def test_left_door_open_when_door_locked_with_closed_door(self):
        # Given
        self.car_controller.unlock_vehicle()
        self.car_controller.unlock_left_door()
        # When
        execute_command_callback("LEFT_DOOR_OPEN",self.car_controller)
        # Then
        self.assertEqual(self.car_controller.get_left_door_status(), "OPEN")

    # RIGHT_DOOR_OPEN

    # test case 4 : 전체 잠금 LOCKED 일 때 RIGHT_DOOR_OPEN
    def test_right_door_open_when_locked(self):
        # Given
        self.car_controller.lock_vehicle()
        # When
        execute_command_callback("RIGHT_DOOR_OPEN",self.car_controller)
        # Then
        self.assertEqual(self.car_controller.get_right_door_status(), "CLOSED")

    # test case 5 : 문이 LOCKED 일 때 RIGHT_DOOR_OPEN
    def test_right_door_open_when_door_locked_with_closed_door(self):
        # Given
        self.car_controller.unlock_vehicle()
        self.car_controller.lock_right_door()
        # When
        execute_command_callback("RIGHT_DOOR_OPEN",self.car_controller)
        # Then
        self.assertEqual(self.car_controller.get_right_door_status(), "CLOSED")

    # test case 6 : 문이 UNLOCKED 일 때 RIGHT_DOOR_OPEN
    def test_right_door_open_when_door_locked_with_closed_door(self):
        # Given
        self.car_controller.unlock_vehicle()
        self.car_controller.unlock_right_door()
        # When
        execute_command_callback("RIGHT_DOOR_OPEN",self.car_controller)
        # Then
        self.assertEqual(self.car_controller.get_right_door_status(), "OPEN")

    # LEFT_DOOR_CLOSE

    # test case 7 : 문이 OPEN일 때 LEFT_DOOR_CLOSE
    def test_left_door_close(self):
        # Given
        self.car_controller.unlock_vehicle()
        self.car_controller.open_left_door()
        # When
        execute_command_callback("LEFT_DOOR_CLOSE",self.car_controller)
        # Then
        self.assertEqual(self.car_controller.get_left_door_status(), "CLOSED")

    # test case 8 : left_temp가 LOCKED 일 때 LEFT_DOOR_CLOSE
    def test_left_door_close_when_left_temp_is_locked(self):
        # Given
        self.car_controller.unlock_vehicle()
        self.car_controller.open_left_door()
        self.car_controller.lock_left_door()
        # When
        execute_command_callback("LEFT_DOOR_CLOSE",self.car_controller)
        # Then
        self.assertEqual(self.car_controller.get_left_door_status(), "CLOSED")
        self.assertEqual(self.car_controller.get_left_door_lock(), "LOCKED")

    # RIGHT_DOOR_CLOSE

    # test case 7 : 문이 OPEN일 때 RIGHT_DOOR_CLOSE
    def test_right_door_close(self):
        # Given
        self.car_controller.unlock_vehicle()
        self.car_controller.open_right_door()
        # When
        execute_command_callback("RIGHT_DOOR_CLOSE",self.car_controller)
        # Then
        self.assertEqual(self.car_controller.get_right_door_status(), "CLOSED")

    # test case 8 : right_temp가 LOCKED 일 때 RIGHT_DOOR_CLOSE
    def test_right_door_close_when_right_temp_is_locked(self):
        # Given
        self.car_controller.unlock_vehicle()
        self.car_controller.open_right_door()
        self.car_controller.lock_right_door()
        # When
        execute_command_callback("RIGHT_DOOR_CLOSE",self.car_controller)
        # Then
        self.assertEqual(self.car_controller.get_right_door_status(), "CLOSED")
        self.assertEqual(self.car_controller.get_right_door_lock(), "LOCKED")

class TestCarTrunk(unittest.TestCase):
    def setUp(self):
        self.car = Car()
        self.car_controller = CarController(self.car)

    # false = opened, true = closed

    # test case 1 : 전체 잠금이 LOCKED일 때 트렁크 OPEN
    def test_trunk_open_when_locked(self):
        # Given
        self.car_controller.lock_vehicle()
        # When
        execute_command_callback("TRUNK_OPEN", self.car_controller)  # 트렁크 열기
        # Then
        self.assertTrue(self.car_controller.get_trunk_status())  # 트렁크 닫힌 상태 확인

    # test case 2 : 전체 잠금이 UNLOCKED이고 트렁크 CLOSED일 때, 트렁크 OPEN
    def test_trunk_open_when_unlocked(self):
        # Given
        self.car_controller.unlock_vehicle()
        # When
        execute_command_callback("TRUNK_OPEN", self.car_controller)  # 트렁크 열기
        # Then
        self.assertFalse(self.car_controller.get_trunk_status())  # 트렁크 열린 상태 확인

    # test case 3 : 속도가 10 이상일 때, 트렁크 OPEN
    def test_trunk_open_when_speed_is_faster_than_10(self):
        # Given
        self.car_controller.unlock_vehicle()
        self.car_controller.toggle_engine()
        self.car_controller.accelerate()
        self.car_controller.accelerate()
        # When
        execute_command_callback("TRUNK_OPEN", self.car_controller)  # 트렁크 열기
        # Then
        self.assertTrue(self.car_controller.get_trunk_status())  # 트렁크 닫힌 상태 확인

    # test case 4 : 전체 잠금이 UNLOCKED이고 트렁크 OPENED일 때, 트렁크 CLOSE
    def test_trunk_close_when_unlocked(self):
        # Given
        self.car_controller.unlock_vehicle()
        self.car_controller.open_trunk()
        # When
        execute_command_callback("TRUNK_CLOSE", self.car_controller)  # 트렁크 닫기
        # Then
        self.assertTrue(self.car_controller.get_trunk_status())  # 트렁크 닫힌 상태 확인

    # test case 5 : 전체 잠금이 LOCKED이고 트렁크 OPENED일 때, 트렁크 CLOSE
    def test_trunk_close_when_locked(self):
        # Given
        self.car_controller.unlock_vehicle()
        self.car_controller.open_trunk()
        self.car_controller.lock_vehicle()
        # When
        execute_command_callback("TRUNK_CLOSE", self.car_controller)  # 트렁크 닫기
        # Then
        self.assertTrue(self.car_controller.get_trunk_status())  # 트렁크 닫힌 상태 확인
