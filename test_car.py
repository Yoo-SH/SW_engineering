import unittest
from car import Car
from car_controller import CarController
from main import execute_command_callback
from main import get_left_temp, get_right_temp

class TestEngineBtn(unittest.TestCase):
    def setUp(self):
        self.car = Car()
        self.car_controller = CarController(self.car)

    def test_engine_start_without_brake(self):
        """브레이크를 밟지 않은 상태에서 엔진 시동 실패(1통과)"""

        # Given: 잠금 해제
        self.car_controller.unlock_vehicle()

        # When: 엔진 버튼 누름
        execute_command_callback("ENGINE_BTN", self.car_controller)

        # Then: 엔진 OFF
        self.assertFalse(self.car_controller.get_engine_status())


    def test_engine_start_with_brake(self):
        """브레이크를 밟고 엔진 시동 성공(2통과)"""
        # Given: 잠금 해제
        self.car_controller.unlock_vehicle()

        # When: 엔진 버튼 누름
        execute_command_callback("BRAKE ENGINE_BTN", self.car_controller)

        # Then: 엔진 ON
        self.assertTrue(self.car_controller.get_engine_status())



    def test_engine_toggle_unlocked(self):
        """잠금 해제 상태에서 엔진 토글 테스트(3통과)"""
        # Given: 차량 잠금 해제, 엔진 OFF
        self.car_controller.unlock_vehicle()

        # When: 엔진 버튼 누름 (토글)
        execute_command_callback("BRAKE ENGINE_BTN", self.car_controller)

        # Then: 엔진 ON
        self.assertTrue(self.car_controller.get_engine_status())

        # When: 엔진 버튼 다시 누름 (토글)
        execute_command_callback("ENGINE_BTN", self.car_controller)

        # Then: 엔진 OFF
        self.assertFalse(self.car_controller.get_engine_status())


    def test_engine_toggle_locked(self):
        """잠금 상태에서 엔진 토글 테스트 (변화 없어야 함)(4통과)"""
        # Given: 차량 잠금, 엔진 OFF
        self.car_controller.lock_vehicle()

        # When: 엔진 버튼 누름
        execute_command_callback("BRAKE ENGINE_BTN", self.car_controller)

        # Then: 엔진 OFF (변화 없음)
        self.assertFalse(self.car_controller.get_engine_status())


    def test_engine_start_not_stopped(self):
        """주행 중 엔진 시동 실패(5통과)"""
        # Given: 잠금 해제, 주행 상태
        self.car_controller.unlock_vehicle()
        self.car_controller.toggle_engine()
        self.car_controller.accelerate()

        # When: 엔진 버튼 누름
        execute_command_callback("BRAKE ENGINE_BTN", self.car_controller)

        # Then: 엔진 ON (변경 없음)
        self.assertTrue(self.car_controller.get_engine_status()) # 시동은 켜져있어야 함

    def test_engine_when_stop(self):
        """차량이 가속 후 정지 했을 때, 엔진 토글이 작동하는지 확인(6이상해....)"""
        # Given:
        self.car_controller.unlock_vehicle()
        self.car_controller.toggle_engine()
        self.car_controller.accelerate()
        self.car_controller.brake()

        # When:
        execute_command_callback("ENGINE_BTN", self.car_controller)

        # Then:
        self.assertFalse(self.car_controller.get_engine_status())


class TestSOS(unittest.TestCase):
    def setUp(self):
        self.car = Car()
        self.car_controller = CarController(self.car)

    def test_sos_normal(self):
        """주행 중 SOS 버튼 누르면 정지 및 모든 문/트렁크 열림"""
        # Given: 주행 중
        self.car_controller.unlock_vehicle()
        self.car_controller.toggle_engine()
        self.car_controller.accelerate()

        # When: SOS 버튼 누름
        execute_command_callback("SOS", self.car_controller)

        # Then: 정지, 모든 문/트렁크 열림
        self.assertEqual(self.car.speed, 0)
        self.assertEqual(self.car.left_door_lock, "UNLOCKED")
        self.assertEqual(self.car.right_door_lock, "UNLOCKED")
        self.assertEqual(self.car.left_door_status, "OPEN")
        self.assertEqual(self.car.right_door_status, "OPEN")
        self.assertFalse(self.car.trunk_status)

    def test_sos_already_stopped(self):
        """정지 상태에서 SOS 버튼 누르면 모든 문/트렁크 열림"""
        # Given: 정지 상태
        self.car_controller.unlock_vehicle()

        # When: SOS 버튼 누름
        execute_command_callback("SOS", self.car_controller)

        # Then: 모든 문/트렁크 열림 (속도는 변화 없음)
        self.assertEqual(self.car.speed, 0)
        self.assertEqual(self.car.left_door_lock, "UNLOCKED")
        self.assertEqual(self.car.right_door_lock, "UNLOCKED")
        self.assertEqual(self.car.left_door_status, "OPEN")
        self.assertEqual(self.car.right_door_status, "OPEN")
        self.assertFalse(self.car.trunk_status)

##여기까지 괜찮..

class TestLock(unittest.TestCase):
    def setUp(self):
        self.car = Car()
        self.car_controller = CarController(self.car)

    def test_lock_normal(self):
        """엔진 OFF, 모든 문/트렁크 닫힘 상태에서 잠금 성공(1통과)"""
        # Given: 엔진 OFF, 모든 문/트렁크 닫힘, 잠금 해제 상태
        self.car_controller.unlock_vehicle()
        self.car_controller.toggle_engine()  # 엔진 켜짐
        self.car_controller.toggle_engine()  # 엔진 꺼짐
        self.car_controller.close_trunk()
        self.car_controller.close_left_door()
        self.car_controller.close_right_door()

        # When: 잠금 시도
        execute_command_callback("LOCK", self.car_controller)

        # Then: 잠김 상태
        self.assertTrue(self.car_controller.get_lock_status())

    def test_lock_engine_on(self):
        """엔진 ON 상태에서 잠금 실패(2통과)"""
        # Given: 엔진 ON, 잠금 해제 상태
        self.car_controller.unlock_vehicle()
        self.car_controller.toggle_engine()  # 엔진 켜짐

        # When: 잠금 시도
        execute_command_callback("LOCK", self.car_controller)

        # Then: 잠금 해제 상태 유지
        self.assertFalse(self.car_controller.get_lock_status())

    def test_lock_left_door_open(self):
        """왼쪽 문 열린 상태에서 잠금 실패(3통과)"""
        # Given: 왼쪽 문 열림, 잠금 해제 상태
        self.car_controller.unlock_vehicle()
        self.car_controller.unlock_left_door()  # 왼쪽 문 잠금 해제
        self.car_controller.open_left_door()  # 왼쪽 문 열기

        # When: 잠금 시도
        execute_command_callback("LOCK", self.car_controller)

        # Then: 잠금 해제 상태 유지
        self.assertFalse(self.car_controller.get_lock_status())

    def test_lock_right_door_open(self):
        """오른쪽 문 열린 상태에서 잠금 실패(4통과)"""
        # Given: 오른쪽 문 열림, 잠금 해제 상태
        self.car_controller.unlock_vehicle()
        self.car_controller.unlock_right_door()
        self.car_controller.open_right_door()

        # When: 잠금 시도
        execute_command_callback("LOCK", self.car_controller)

        # Then: 잠금 해제 상태 유지
        self.assertFalse(self.car_controller.get_lock_status())

    def test_lock_trunk_open(self):
        """트렁크 열린 상태에서 잠금 실패(5통과)"""
        # Given: 트렁크 열림, 잠금 해제 상태
        self.car_controller.unlock_vehicle()
        self.car_controller.open_trunk()

        # When: 잠금 시도
        execute_command_callback("LOCK", self.car_controller)

        # Then: 잠금 해제 상태 유지
        self.assertFalse(self.car_controller.get_lock_status())


##여기까지 완료

class TestUnlock(unittest.TestCase):
    def setUp(self):
        self.car = Car()
        self.car_controller = CarController(self.car)

    def test_unlock_normal(self):
        """잠김 상태에서 잠금 해제 성공(1통과)"""
        # Given: 잠김 상태
        self.car_controller.lock_vehicle()

        # When: 잠금 해제 시도
        execute_command_callback("UNLOCK", self.car_controller)

        # Then: 잠금 해제 상태
        self.assertFalse(self.car_controller.get_lock_status())

    def test_unlock_already_unlocked(self):
        """이미 잠금 해제 상태에서 잠금 해제 시도 (변화 없음)(2통과)"""
        # Given: 잠금 해제 상태
        self.car_controller.unlock_vehicle()

        # When: 잠금 해제 시도
        execute_command_callback("UNLOCK", self.car_controller)

        # Then: 잠금 해제 상태 유지
        self.assertFalse(self.car_controller.get_lock_status())


class TestAccelerate(unittest.TestCase):
    def setUp(self):
        self.car = Car()
        self.car_controller = CarController(self.car)

    def test_accelerate_unlocked(self):
        """잠금 해제, 엔진 ON 상태에서 가속 20키로면 문 닫힘"""

        # Given: 잠금 해제, 엔진 ON, 속도 0, 모든 문 열림
        self.car_controller.unlock_vehicle()
        self.car_controller.toggle_engine()
        self.car_controller.unlock_left_door()
        self.car_controller.open_left_door()
        self.car_controller.unlock_right_door()
        self.car_controller.open_right_door()

        # When: 가속
        execute_command_callback("ACCELERATE", self.car_controller)
        execute_command_callback("ACCELERATE", self.car_controller)

        # Then: 속도 20, 모든 문 닫힘
        self.assertEqual(self.car_controller.get_speed(), 20)
        self.assertEqual(self.car_controller.get_left_door_status(), "CLOSED")
        self.assertEqual(self.car_controller.get_right_door_status(), "CLOSED")

##############여기까지 완료




    def test_accelerate_engine_off(self):
        """엔진 OFF 상태에서 가속 실패"""
        # Given: 엔진 OFF, 잠금 해제
        self.car_controller.unlock_vehicle()

        # When: 가속 시도
        execute_command_callback("ACCELERATE", self.car_controller)

        # Then: 속도 변화 없음
        self.assertEqual(self.car_controller.get_speed(), 0)

    def test_accelerate_trunk_open(self):
        """트렁크 열린 상태에서 가속, 속도 제한(30) 테스트"""
        # Given: 트렁크 열림, 엔진 ON, 잠금 해제
        self.car_controller.unlock_vehicle()
        self.car_controller.toggle_engine()
        self.car_controller.open_trunk()

        # When: 가속 (3번)
        for _ in range(3):
            execute_command_callback("ACCELERATE", self.car_controller)

        # Then: 속도 30 (제한)
        self.assertEqual(self.car_controller.get_speed(), 30)

        # When: 추가 가속 시도
        execute_command_callback("ACCELERATE", self.car_controller)

        # Then: 속도 30 유지
        self.assertEqual(self.car_controller.get_speed(), 30)


    def test_accelerate_trunk_closed(self):
        """트렁크 닫힘 상태에서 가속, 최대 속도(200) 테스트"""
        # Given: 트렁크 닫힘, 엔진 ON, 잠금 해제
        self.car_controller.unlock_vehicle()
        self.car_controller.toggle_engine()
        self.car_controller.close_trunk()

        # When: 가속 (20번)
        for _ in range(20):
            execute_command_callback("ACCELERATE", self.car_controller)

        # Then: 속도 200 (최대 속도)
        self.assertEqual(self.car.speed, 200)

        # When: 추가 가속 시도
        execute_command_callback("ACCELERATE", self.car_controller)

        # Then: 속도 200 유지
        self.assertEqual(self.car_controller.get_speed(), 200)
        
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
    def test_right_door_open_when_door_unlocked_with_closed_door(self):
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