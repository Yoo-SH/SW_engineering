## 시나리오 
UNLOCK(차량 잠금) ⇒ 모든 문을 열거나 닫을 수 있는 상태로 만듦.

ENGINE_BTN(엔진 켜기) ⇒ 차량이 주행할 준비를 함.

ACCELERATE(가속) ⇒ 차량이 출발하여 10 km/h의 속도로 주행을 시작함.

SOS(긴급 상황) → 차량 속도가 즉시 0으로 감소하고, 모든 문이 잠금 해제되며 문과 트렁크가 열림.

SOS(긴급 상황) → 두 번째 SOS 버튼 입력. 차량이 이미 정지 상태이므로, 추가 동작 없음.

ENGINE_BTN(엔진 끄기) ⇒ 긴급 상황 이후 엔진을 끔.

LOCK(차량 잠금) ⇒ 문 열림, 트렁크 열림 등의 조건으로 문이 닫히지 않음.

## 실행 결과
engin: off
speed: 0
vehicle: unLocked
leftDoor: open
rightDoor: open
leftDoorLock: unUocked
righDoorLock: unLocked
Trunk: opened