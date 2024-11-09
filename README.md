입력 예시파일 - example_fail, example_success

실행방법 - 입력파일을 프로젝트 path에 포함 후, 콘솔창에 파일 이름을 입력


## `GIT` 

* **main**(테스트 코드 검증이 끝난 브랜치)
* **develop**(기능 개발이 완료된 브랜치)
* **feature**(기능 단위의 브랜치)
    - 브랜치 이름: feature/새로운기능
    - 예시: feature/LEFT_DOOR_LOCK

```
** 레파지토리 가져오기**

<git clone>
1. 해당 코드를 저장할 폴더 생성
2. git init(해당 폴더 경로내에서)
3. git clone https://github.com/Yoo-SH/SW_engineering.git (해당 폴더 경로내에서)
    3.1 연결되지 않으면, 확인사항 - 깃 설치, git config user.name

** 커밋 메시지 올리기 **

<git add -> git commit -m "" >
1. git status (변경사항 확인)
2. git add 파일or경로 (변경사항 커밋단위에 넣음)
    2.1 예시) git add .(해당 경로 모두 커밋에 넣음), git add example.py(해당 파일만 커밋에 넣음)
3. git commit -m "커밋규칙: 커밋내용"
    3.1 예시) git commit -m "feat: 브레이크 작동하는 함수추가"


** 브랜치 로직 **

< 기능 단위의 브랜치 개발시 커맨드 >
1. git checkout develop (로컬 develop 브랜치 가져옴)
2. git pull origin develop(외부 develop 브랜치 가져와 최신화)
3. git checkout -b feature/기능(본인 기능 단위의 브랜치로 이동) 
4. git commit (규칙에 따라 개발)
    ex) git commit -m "feat: LEFT_DOOR_LOCK 자동 닫힘 기능 추가"

< 기능 단위의 브랜치 개발 완료시>
1. git checkout develop (로컬 develop 브랜치 가져옴)
2. git pull origin develop (외부 develop 브랜치 가져와 최신화)
3. git merge --no-ff feature/기능 (본인이 개발한 기능 단위의 브랜치를 병합)
    3.1 --no-f 옵션을 넣어줘야 기능단위로 커밋 히스토리가 볼 수 있으니 유의..
4. git branch -d featrue/기능 (본인이 개발했던 브랜치 삭제)
    4.1 나중에 다시 수정해야하면 브랜치 다시 생성
5. git push origin develop
```

## `git branch logic 예시`
*   빨간 네모칸이 기능 단위의 브랜치
*   기능 단위의 브랜치마다 히스토리를 볼 수 있음


![스크린샷 2024-11-06 124006](https://github.com/user-attachments/assets/114e82ba-116c-4e2f-8501-9451c28fa282)


## `git commit 규칙`

|type|활용상황|예제|
|:---|:---|:---|
|feat|새로운 기능 추가|사용자 로그인 기능 추가|
|fix|버그 수정|잘못된 계산 로직 수정|
|docs|문서 수정|README 파일에 설치 방법 추가|
|style|코드 스타일 변경 (코드 포매팅, 세미콜론 누락 등)|코드에서 불필요한 세미콜론 제거|
|design|사용자 UI 디자인 변경 (CSS 등) 기능 추가|메인 페이지 버튼 스타일 변경|
|test|테스트 코드, 리팩토링 (Test Code)|로그인 기능에 대한 단위 테스트 추가|
|refactor|refactor|중복된 코드 함수로 리팩토링|
|build|빌드 파일 수정|Webpack 설정 파일 수정|
|ci|CI 설정 파일 수정|GitHub Actions 워크플로우 파일 수정|
|perf|성능 개선|API 응답 속도를 높이기 위한 쿼리 최적화|
|chore|자잘한 수정이나 빌드 업데이트|패키지 버전 업데이트|
|rename|파일 혹은 폴더명을 수정만 한 경우|login.js 파일명을 auth.js로 변경|
|remove|파일을 삭제만 한 경우|사용되지 않는 old_styles.css 파일 삭제|

