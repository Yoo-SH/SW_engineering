## 시나리오
UNLOCK(차량 잠금 해제) ⇒ 모든 문을 열거나 닫을 수 있는 상태로 만듦

ENGINE_BTN(엔진 켜기) ⇒ 차량이 주행할 준비

ACCELERATE(가속) ⇒ 차량이 출발하여 10 km/h의 속도로 주행을 시작

ACCELERATE(가속) ⇒ 차량의 속도가 20 km/h로 증가. 주행 중 안전을 위해 문이 자동으로 잠김

ACCELERATE(가속) ⇒ 차량의 속도가 30 km/h로 증가

LOCK(차량 잠금) ⇒ 차량이 이미 주행 중이므로 문은 잠금이 동작되지 않음.

ACCELERATE(추가 가속) ⇒ 차량의 속도가 40 km/h로 증가. 주행이 계속됨

BRAKE(감속) ⇒ 차량의 속도가 30 km/h로 감소

ENGINE_BTN(엔진 끄기) ⇒ 차량 주행 중 엔진 버튼을 작동. 동작하지 않음.

BRAKE(감속) ⇒ 차량의 속도가 20 km/h로 감소

BRAKE(감속) ⇒ 차량의 속도가 10 km/h로 감소

BRAKE(감속) ⇒ 차량의 속도가 0 km/h로 감소

ENGINE_BTN(엔진 끄기) ⇒ 차량이 정지한  후 엔진 버튼을 작동. 시도 꺼짐

LOCK(차량 잠금) ⇒ 차량을 잠금 상태로 전환. 이제 차량은 안전하게 잠김.

## 실행 결과: 

- engin: off
- speed: 0
- vehicle: locked
- leftDoor: closed
- rightDoor: closed
- leftDoorLock: locked
- righDoorLock: locked
- Trunk: locked