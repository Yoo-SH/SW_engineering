import unittest
from car import Car
from car_controller import CarController
from main import execute_command_callback

class TestCarControllerTrunk(unittest.TestCase):
    def setUp(self):
        self.car = Car()
        self.car_controller = CarController(self.car)

    def test_trunk_open_callback(self):
        self.assertFalse(self.car.get_trunk_status())  # 초기 상태 확인
        execute_command_callback("TRUNK_OPEN", self.car_controller)  # 트렁크 열기
        self.assertTrue(self.car.get_trunk_status())  # 트렁크 열린 상태 확인

    def test_trunk_close_directly(self):
        self.car_controller.open_trunk()
        self.assertTrue(self.car.get_trunk_status())  # 트렁크 열린 상태 확인
        self.car_controller.close_trunk()
        self.assertFalse(self.car.get_trunk_status())  # 트렁크 닫힘 상태 확인

    def test_trunk_speed_limit_with_callback(self):
        execute_command_callback("TRUNK_OPEN", self.car_controller)
        self.assertTrue(self.car.get_trunk_status())
        self.car.set_speed(40)
        execute_command_callback("ACCELERATE", self.car_controller)  # 트렁크 열린 상태에서 가속 시도
        self.assertEqual(self.car.get_speed(), 40)  # 속도 유지 확인

    def test_trunk_speed_allowance_below_limit_with_callback(self):
        execute_command_callback("TRUNK_OPEN", self.car_controller)
        self.assertTrue(self.car.get_trunk_status())
        self.car.set_speed(20)
        execute_command_callback("ACCELERATE", self.car_controller)  # 트렁크 열린 상태에서 제한 속도 이내 가속 시도
        self.assertEqual(self.car.get_speed(), 30)  # 속도가 10 증가했는지 확인

if __name__ == "__main__":
    unittest.main()
