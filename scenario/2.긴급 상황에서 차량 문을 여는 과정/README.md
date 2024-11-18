## 시나리오
UNLOCK(차량 자금) ⇒ 모든 문을 열거나 닫을 수 있는 상태로 만듦

ENGINE_BTN(엔진켜기) ⇒ 차량이 주행할 준비

ACCELERATE(가속) ⇒ 차량이 출발하여 10 km/h의 속도로 주행을 시작

SOS(긴급상황) ⇒ 차량의 속도가 0으로 즉시 감소하고, 모든 문이 잠금 해제되며 문과 트렁크가 열림

ENGINE_BTN(엔진끄기) ⇒ 긴급 상황 이후 엔진을 끔

LOCK(차량 잠금) ⇒ 문 열림, 트렁크 열림 등의 조건으로 문이 닫히지 않음.

## 실행 결과: 

- engin: off
- speed: 0
- vehicle: unLocked
- leftDoor: open
- rightDoor: open
- leftDoorLock: unLocked
- rightDoorLock: unLocked
- Trunk: opened