
# OCI에서 VM.Standard.A1.Flex 구성에 대한 용량이 부족 문제를 해결하기

오라클 클라우드 Always Free Resources 에는 Ampere A1 Compute instances (4OCPU와 24GB 메모리)를 제공하지만 일부 리전에서는 용량 부족 문제 (Out of Capacity)로   인스턴스를 생성할 수 없습니다. 이 프로젝트는 일정 기간마다 인스턴스 생성 요청을 보내 문제를 해결합니다.

원본 프로젝트: [hitrov/oci-arm-host-capacity](https://github.com/hitrov/oci-arm-host-capacity)

## 프로그램을 실행하기 위한 요소

 - API 키 생성 [OCI 콘솔 > 사용자 설정 > API 키 관리]
 - SSH 접속에 사용할 키파일 생성 [OCI 인스턴스 생성 과정에서 키 페어 생성]
 - 로그 기능 사용 > 디스코드 웹훅 연동하기 [디스코드 채널 Integrations > Webhooks > New Webhook]

## 도커로 실행하기
```bash
docker-compose up -d
```

## 직접 실행하기

### 1. Python 3.13 버전 설치
[여기를 클릭해](https://www.python.org/downloads/) Python version이 3.13인지 확인한 후 운영체제에 맞게 설치합니다.

### 2. 필요한 라이브러리 설치
```bash
pip install -r requirements.txt
```

### 3.프로그램 실행하기
```bash
python cronjob.py
```



