## 시나리오
UNLOCK(차량 잠금 해제) ⇒ 모든 문을 열거나 닫을 수 있는 상태로 만듦

TRUNK_OPEN(트렁크 열기) ⇒ 차량의 트렁크를 열어 짐을 싣거나 내릴 수 있는 상태로 만듦

ENGINE_BTN(엔진 켜기) ⇒ 차량이 주행할 준비

ACCELERATE(가속) ⇒ 차량이 출발하여 10 km/h의 속도로 주행을 시작

ACCELERATE(가속) ⇒ 차량의 속도가 20 km/h로 증가. 트렁크가 열린 상태이므로 속도가 30 km/h를 초과하지 않도록 제한됨

ACCELERATE(가속) ⇒ 차량의 속도가 30 km/h로 증가. 이 상태에서 더 이상의 가속은 제한됨

ACCELERATE(추가 가속 시도) ⇒ 트렁크가 열린 상태에서는 30 km/h 이상의 속도로 주행할 수 없음. 속도는 변동 없이 유지됨

TRUNK_CLOSE(트렁크 닫기) ⇒ 트렁크를 닫아 차량을 정상 주행 상태로 만듦

ACCELERATE(가속) ⇒ 차량의 속도가 40 km/h로 증가. 이제 더 높은 속도로 주행 가능

BRAKE(감속) ⇒ 차량의 속도가 30 km/h로 감소

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