## 시나리오 
UNLOCK(차량 자금) ⇒ 모든 문을 열거나 닫을 수 있는 상태로 만듦

ENGINE_BTN(엔진켜기) ⇒ 차량이 주행할 준비

ACCELERATE(가속) ⇒ 차량이 출발하여 10 km/h의 속도로 주행을 시작

ACCELERATE(가속) ⇒ 차량이 더 가속하여 현재 속도는 20 km/h로 증가

BRAKE(브레이크) ⇒ 브레이크를 밟아 속도를 줄임. 현재 속도는 10 km/h로 감소

BRAKE(브레이크) ⇒ 차량이 완전히 멈춤. 현재 속도는 0 km/h로 감소

BRAKE(브레이크) ⇒ 차량은 이미 정지 상태이므로, 추가 감속 시도에도 속도에 변화가 없음

ENGINE_BTN(엔진끄기) ⇒ 엔진을 끔 이제 차량은 대기 상태가 됨

LOCK(차량 잠금) ⇒  차량을 잠금 상태로 전환. 

## 실행 결과: 

- engin: off
- speed: 0
- vehicle: locked
- leftDoor: closed
- rightDoor: closed
- leftDoorLock: locked
- righDoorLock: locked
- Trunk: locked