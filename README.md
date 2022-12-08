# "외부 시스템을 사용하는 쇼핑몰의 반품배송 상황 추적"

## 구현사항
1. 반품조회 API를 호출하여 반품 주문을 수집한다.
2. 배송조회 API를 호출하여 수신된 송장번호를 기준으로 배송 상황을 Tracking 한다. 
3. 최종적으로 수거완료된 주문의 결과 데이터를 송신한다.

## 아키텍쳐 구현
![image](https://user-images.githubusercontent.com/97004730/206373120-57f51dd6-76c7-4e00-bc16-103340dc533c.png)
- 컨테이너 서비스로 구현하였으므로 별도의 인스턴스 추가 없이 현재 존재하고 있는 Batch 인스턴스에 로직만 추가하는 방법을 고려했습니다.

### 🏁 프로젝트 실행 방법
1. 도커 컴포즈가 설치되어 있는지 확인합니다.
```
docker-compose -v
```
2. .env.sample 파일을 바탕으로 각 변수 명에 해당하는 값을 넣은 .env 파일을 생성합니다.
```
TOKEN="private token"
BASE_URL="https://moms.dev.musinsalogistics.co.kr/api/external/data"
```
3. 도커 컴포즈 파일을 실행합니다.
```
docker-compose up
```
