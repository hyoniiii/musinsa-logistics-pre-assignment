# "외부 시스템을 사용하는 쇼핑몰의 반품배송 상황 추적"
## 동작 개요

### 상황 설명
```
💡 위와 같은 아키텍처로 설계된 서비스를 제공하는 A 회사는 현재 단발성 이벤트로 단시간(3~5분 이내) 내 유입되는 트래픽(평균 3만건)으로 인해, 
   타 외부 시스템들과의 통신 장애 등의 서비스 장애로 인해 곤란한 상황을 겪고 있다. 
   이 상황을 개선하기 위해 아키텍처 재설계 혹은 부분적 기능 개선을 고민 중이다. 
   엔지니어로써 내가 내놓을 수 있는 솔루션을 제안해보자
```
## 구현사항
1. 반품조회 API를 호출하여 반품 주문을 수집한다.
2. 배송조회 API를 호출하여 수신된 송장번호를 기준으로 배송 상황을 Tracking 한다. 
3. 최종적으로 수거완료된 주문의 결과 데이터를 송신한다.

## 아키텍쳐 구현
![Untitled Diagram drawio (1)](https://user-images.githubusercontent.com/97004730/201527453-b581204b-56c0-4ddf-ae17-37865d359d6b.png)

### 🏁 프로젝트 실행 방법
1. 서버리스 프레임 워크를 설치합니다.
```
npm install -g serverless
```
2. 의존성 패키지를 설치합니다.
```
npm install
```
3. .env.sample 파일을 바탕으로 각 변수 명에 해당하는 값을 넣은 .env 파일을 생성합니다.
```
TOKEN="private token"
BASE_URL="https://moms.dev.musinsalogistics.co.kr/api/external/data"
SLACK_URL="slack url"
```
4. 서버리스 어플리케이션을 배포합니다.
```
sls deploy
```
### 🏁 Clean Up
```
sls remove
```
## 고려 사항
### Backend Engineer
#### 1. 어플리케이션의 구동에 적절한 아키텍쳐를 구성하여 네트워크 환경 구축
- 문제 : 모놀리틱 서버 아키텍쳐 구조로 인해 간헐적 이벤트 트래픽에도 서비스 장애가 발생함
- 해결 : 필요한 기능만 Serverless로 구축하여 메인 서버의 부담을 감소시킴
- 이유 : 서버리스는 AWS에서 관리하므로, 서버유지에 대한 비용이 들지 않고, 사용한 만큼만 비용을 지불하기 때문에(On-demand) 트래픽으로 인한 간헐적인 이슈 대응에 적합하다고 판단
#### 2. 동작 개요에 맞춰 각 API를 호출하여 올바른 동작 구현
- 문제 : 제공받은 반품조회 API가 정상적으로 동작하지 않음
- 해결 : 현재 테스트 가능한 배송조회 API를 기준으로 동작 확인 함. 추후 API 서버가 정상적으로 동작 할 시 업데이트 예정
<img width="2147" alt="image" src="https://user-images.githubusercontent.com/97004730/201528056-77568ce4-486a-49c1-9a56-026860fd130f.png">

- 이유 : 반품 조회 API /get 요청 시 아래와 같이 데이터 값이 나오지 않음
<img width="2141" alt="스크린샷 2022-11-13 오후 11 45 18" src="https://user-images.githubusercontent.com/97004730/201527938-fa2f6808-42e9-477a-bbb7-43df3a9a942c.png">


### DevOps/Cloud Engineer
#### 1. az 또는 vpc 분리를 통한 가용성 확보
- 서버리스를 이용하여 아키텍쳐를 구현하였으므로, AZ와 VPC 분리를 적용하지 않았지만 해당 서비스를 EC2로 개발한다면 적용 가능
#### 2. 기본적인 보안 요소(private/public 서브넷 분리 등) 설계
- 기존 아키텍쳐에서는 VPC Peering이 존재하였는데, 이는 Dev 환경에서의 에러가 Product 까지 확산 될 우려가 있으므로 삭제함
- AWS Client VPN을 사용하여 각각의 VPC의 하나의 서브넷에 세션을 연결하여 보안성을 추구함
- AWS Client VPN은 세션 유지 당 0.1 달러 per hour, 활성 커넥션 수에 따라 0.05 달러 per hour의 비용이 청구됨
#### 3. 주요 지표(EC2, ECS, RDS, Cache 등)에 대한 모니터링 구축
- 현재 유지하고 있는 Batch Master에 그라파나 설치 후 CloudWatch를 이용하여 모니터링 구축 가능
#### 4. 비용 최적화에 따른 아키텍쳐 구성
- 비용 최적하에 따른 아키텍쳐를 구성하기 위해 서버리스를 고려함
#### 5. (advanced) 데이터베이스의 동기화 고려
- 모놀리틱 서비스에서 이용중인 Aurora RDS의 '읽기 전용 복제본(Create Read Replica)' 옵션을 사용하여 읽기 전용 dB 이용 가능
   
### 가점 기준
#### 1. 인프라에 접근 가능한 유저 및 IP 통제 등 적절한 권한 관리를 통한 보안 관리
- IAM 또는 보안그룹 적용으로 각 인스턴스에 접근 가능한 User별 관리와 IP 기반 접근권환 관리
  <img width="2185" alt="image" src="https://user-images.githubusercontent.com/97004730/201528274-3e1f4aef-185d-4d7d-83d7-c514761cd0b6.png">
  <img width="2396" alt="image" src="https://user-images.githubusercontent.com/97004730/201528516-f5112fdf-f3d6-4fd5-8b22-c57e8700f961.png">


#### 2. 스케쥴러(Batch 등)를 이용한 자동화된 기능을 구현
- Event Bridge를 사용하여 Batch 스케쥴러 구현
#### 3. 테스트 가능한 API 구현
- Lambda로 개발 시 이벤트 JSON 작성
```JSON
{
  "body": {
    "Attribute": {
      "shipment_number": "SHP_00000579",
      "order_number": "1234",
      "order_item_number": "123123"
    }
  }
}
```
<img width="2013" alt="image" src="https://user-images.githubusercontent.com/97004730/201528576-def97c6a-96d6-476b-8047-ac6c96f3a5f1.png">

#### 4. 서버 내 발생된 이벤트의 Alert 송신(Slack)
https://github.com/hyoniiii/musinsa-logistics-pre-assignment/blob/bb2f285029eadda099e631430fb4c0534c2efffb/functions/delivers.py#L21-L52
![image](https://user-images.githubusercontent.com/97004730/201528585-44d07995-2d30-459f-95da-54d11651aa1e.png)
