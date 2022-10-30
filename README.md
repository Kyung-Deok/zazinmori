# Zazinmori
> 취업준비생 대상 자기소개서 분석 및 구직 관련 정보 제공 서비스

취업준비생을 타겟으로 하여 합격 자기소개서 키워드 빈도 및 기업의 최신 토픽을 분석하고,
사용자에게 자기자소서 작성 관련 가이드 라인 및 구인 중인 기업 정보를 종합적으로 제공하여 
취업을 종합적으로 지원하는 서비스입니다.


- 김세진 [nijes](https://github.com/nijes) : 데이터 엔지니어, 데이터 파이프라인 구축 & 웹 서비스 구현
- 송원혁 [won21yuk](https://github.com/won1hyuk) : 데이터 엔지니어, 데이터 파이프라인 구축 & 웹 서비스 배포
- 이경덕 [Kyung-Deok](https://github.com/Kyung-Deok) : 데이터 엔지니어, 데이터 파이프라인 구축 & 검색엔진 구현
- 장혁준 [ouyaaa](https://github.com/ouyaaa) : 데이터 사이언스, 데이터 분석 & 모델링
- 이준영 [zeous22](https://github.com/zeous22) : 데이터 사이언스, 데이터 분석 & 모델링
- 김우준 [cjdma90](https://github.com/cjdma90) : 데이터 사이언스, 데이터 분석 & 모델링

프로젝트 기간 : 2022.08.18 ~ 2022.09.30
<br><br>

## 서비스 주요 기능
<img src="./zazinmori_server/static/img/favicon.png" alt="-" width="25">&nbsp;기업별 세부 정보 검색 기능<br>
<img src="./zazinmori_server/static/img/favicon.png" alt="-" width="25">&nbsp;채용공고 스크랩 및 자소서 작성 기능<br>
<img src="./zazinmori_server/static/img/favicon.png" alt="-" width="25">&nbsp;기업별, 자소서 항목별 추천 키워드 제공 기능<br>
<img src="./zazinmori_server/static/img/favicon.png" alt="-" width="25">&nbsp;사용자 활동 기반의 유저 맞춤형 기업 추천 기능<br>
<img src="./zazinmori_server/static/img/favicon.png" alt="-" width="25">&nbsp;커뮤니티 및 기타 유저 편의 기능
<br><br>

## 활용 데이터
|  no  |       내용        |          출처           |    형식/방식     |
|:----:|:---------------:|:---------------------:|:------------:|
|  1   |  금융위원회 기업기본정보   |  [공공데이터포털][공공데이터포털]   |   JSON/API   |
|  2   |  금융위원회 기업재무정보   |  [공공데이터포털][공공데이터포털]   |   JSON/API   |
|  3   |  금융위원회 지배구조정보   |  [공공데이터포털][공공데이터포털]   |   JSON/API   |
|  4   | 금융감독원 단일회사 주요계정 | [OPEN DART][opendart] |   XML/API    |
|  5   |   금융감독원 기업개황    | [OPEN DART][opendart] |   XML/API    |
|  6   |  금융감독원 기업고유번호   | [OPEN DART][opendart] |   XML/API    |
|  7   |   잡코리아 합격자소서    |     [잡코리아][잡코리아]      | CSV/CRAWLING |
|  8   |   인크루트 합격자소서    |     [인크루트][인크루트]      | CSV/CRAWLING |
|  9   |   링커리어 합격자소서    |     [링커리어][링커리어]      | CSV/CRAWLING |
|  10  |    독취사 합격자소서    |  [독취사(네이버 카페)][독취사]   | CSV/CRAWLING |
|  11  | 자소설 채용공고/자소서 항목 |      [자소설][자소설]       | CSV/CRAWLING |
|  12  | 빅카인즈 기업별 주요 뉴스  |     [빅카인즈][빅카인즈]      | CSV/CRAWLING |
<br><br>

## 아키텍처 및 기술 스택
#### 아키텍처 정의서
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2F5PWjI%2FbtrODPjpnPt%2Fc7fzBmj5fjICOxVCwytwi0%2Fimg.png">

#### 클러스터
<img src="https://s3-us-west-2.amazonaws.com/secure.notion-static.com/12b4f721-6d2f-4c98-823f-22ace3fcf0ed/%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0.png">

* AWS EC2
* Ubuntu [18.04]
* MySQL [5.7]
* Hadoop [3.2.4]
* Spark [3.2.2]
* Airflow [2.3.3]
* Elasticsearch [8.4.1]
* Logstash [8.4.1]
* Kibana [8.4.1]
* Kafka [2.12]
* Zookeeper [3.8.0]
* Airflow [2.3.3]
* Docker
* NGINX
* FastAPI
* django
* mongoDB
* jenkins
* gitlab
* github
<br><br>

## 데이터 파이프라인 세부 기술
### 확장성
서비스 성장에 따른 서버 규모 확장 용이
* H-S Clustering : 클러스터에 노드 추가하는 형태로 scale out 가능
* Nginx Upstream : Upstream으로 추가 WAS 지정하여 서버 확장 가능
* 로그 모니터링 : elasticsearch, kibana 등을 통해 로그 데이터 분석 환경 구축
* 용도에 따른 서버 구분 : 추후 서버 확장 시, 용도에 맞는 서버에서 기능 확장 시도 가능
### 성능
구축한 데이터 파이프 라인에 대한 가동 속도 향상
* 멀티프로세싱 : 30만 건 이상의 데이터 크롤링 단시간 내 가능토록 멀티프로세싱을 통한 성능 향상
* Spark Cluster : yarn을 클러스터 매니저로 지정하여 리소스 관리, 각 executor에 2core씩 할당
* FastAPI : 메인 서비스 및 모델 서빙 역할에 따라 WAS 구분, FastAPI 이용하여 모델 서빙
* Logstash : Django에서 실시간으로 로그 확보
### 안정성
서비스 규모, 트래픽 증가되는 경우에도 감당 가능토록 인프라 구축
* Hadoop Cluster : 3개 서버를 MasterNode, SecondaryNamenode, DataNode로 활용
* Airflow : 지속적인 업데이트가 필요한 ETL [데이터 수집 -> 하둡 적재 -> 스파크 처리 -> MySQL 적재] 스케줄링하여 자동화
* NGINX : 정적인 파인에 대한 요청 담당하여 서비스 서버 중 하나의 WAS로만 트래픽 집중 방지
* 로그 수집 : 데이터 유실 방지 위해 2개의 logstash를 각각 로그 수집기와 메세지 처리기로 구분, 중간 저장소로 kafka 사용
### 기타
* Jenkins-GitLab : 배포과정을 자동화하여 개발 속도 향상
* coolData MongoDB 적재 : 추후 분석을 위해 과거 로그 데이터 적재
* HTTPS : 서비스 보안 향상
<br><br>
* 

## 서비스 화면
<img src="./zazinmori_server/static/img/favicon.png" alt="-" width="25">&nbsp;인덱스 페이지<br>
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FKTeoY%2FbtrO6NQWlNN%2FxL30meDiHdNx07Tq8XGpJK%2Fimg.png">
<br><img src="./zazinmori_server/static/img/favicon.png" alt="-" width="25">&nbsp;검색 페이지<br>
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbGsfti%2FbtrOFkC16WQ%2FcBUmE0yCIrRHbLSXquBOik%2Fimg.png">
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FO2EaZ%2FbtrOQuLPmRS%2FTIO9eRKKUiDyvdDHvudRp1%2Fimg.png">
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FXUFEn%2FbtrO3UYyJgP%2FHI3h2TIiKP72CfanCj5U20%2Fimg.png">
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FdiBvKW%2FbtrOQCwmJ8C%2F330lvkRqAkWcK6wsyxymEk%2Fimg.png">
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fd99Vw2%2FbtrO2Wbvljd%2FnNlUUH2NN0JuXZmBLV4qf0%2Fimg.png">
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbhcVJU%2FbtrO5sNiFis%2FQZL1L5bBvFGqrSTpkt0S90%2Fimg.png">
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2F30xpz%2FbtrO4ty9iT0%2FkoMLKFnypfcJVcoRwXJRBk%2Fimg.png">
<br><img src="./zazinmori_server/static/img/favicon.png" alt="-" width="25">&nbsp;자기소개서 작성 페이지<br>
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fd23AyB%2FbtrO6glkrsK%2FxHLPZtdtukyDbMQOp2x5n0%2Fimg.png">
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbVH9tm%2FbtrO45dIabS%2FZ0afEs6VUbeRC7ZUK192Nk%2Fimg.png">
<br><img src="./zazinmori_server/static/img/favicon.png" alt="-" width="25">&nbsp;커뮤니티 페이지<br>
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FlHvj9%2FbtrO4pbYVYN%2FxnE2jXrzk15hItkbl6WYl0%2Fimg.png">
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbacpmA%2FbtrO6N4t633%2FJCSVF6g6QuM2k9qDgWHXX0%2Fimg.png">
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbNz349%2FbtrO45EKZCR%2FSVx53DKwHrKjN9QRrO5xn0%2Fimg.png">
<br><img src="./zazinmori_server/static/img/favicon.png" alt="-" width="25">&nbsp;마이페이지<br>
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fc8U05a%2FbtrOQvYi29c%2Fmx7P4pJvc8acGkCXkJn271%2Fimg.png">



<!-- Markdown link & img dfn's -->
[공공데이터포털]: https://www.data.go.kr/
[opendart]: https://opendart.fss.or.kr/
[잡코리아]: https://www.jobkorea.co.kr/
[인크루트]: https://www.incruit.com/
[링커리어]: https://linkareer.com/
[독취사]: https://cafe.naver.com/dokchi/
[자소설]: https://jasoseol.com/
[빅카인즈]: https://www.bigkinds.or.kr/
