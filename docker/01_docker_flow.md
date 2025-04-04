# Docker 기초 & 실무 흐름 정리

## 1. Docker란?

Docker는 컨테이너 기반 가상화 플랫폼으로, 애플리케이션을 개발한 환경 그대로 배포하고 실행할 수 있도록 도와준다.  
운영체제 수준에서 격리된 환경을 만들어, 동일한 이미지가 어디서나 동일하게 동작하게 해준다.

---

## 2. Docker 핵심 구성 요소

| 구성 요소             | 설명 |
|----------------------|------|
| 이미지 (Image)        | 애플리케이션과 실행 환경을 포함한 패키지 |
| 컨테이너 (Container)  | 이미지를 기반으로 생성된 실행 환경 |
| Dockerfile           | 이미지를 만들기 위한 설정 파일 |
| docker-compose.yml   | 여러 컨테이너를 동시에 구성하고 실행하는 설정 파일 |
| 볼륨 (Volume)         | 컨테이너 외부에 데이터를 저장하는 방법 |

---

## 3. 기본 실행 흐름 요약

1. Dockerfile을 작성하여 이미지를 생성
2. docker compose 명령어로 컨테이너를 실행
3. 컨테이너 안에서 애플리케이션이 실행됨
4. 필요시 exec 명령어로 컨테이너 내부에 접속 가능
5. 실행이 끝난 후에는 컨테이너와 이미지를 정리

---

## 4. Dockerfile 기본 구조

```Dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app/main.py"]
```

---

## 5. docker-compose.yml 기본 구조

```yaml
version: '3.8'

services:
  hello-docker:
    build: .
    container_name: hello-container
```

---

## 6. 주요 명령어 정리

```bash
docker compose build --no-cache      # 이미지 빌드
docker compose up -d                # 컨테이너 실행
docker ps                           # 실행 중인 컨테이너 확인
docker logs [컨테이너명]             # 로그 확인
docker exec -it [컨테이너명] bash    # 컨테이너 내부 접속
docker compose down                 # 실행 중인 컨테이너 종료 및 정리
docker system prune -a              # 이미지, 캐시 등 전체 정리
```

---

## 7. 개념 정리

- Docker는 코드, 실행 환경, 설정 등을 이미지로 패키징하여 어디서든 동일하게 실행할 수 있도록 함
- 컨테이너는 이미지의 실행 인스턴스로, 독립된 격리 환경에서 실행됨
- docker-compose는 복잡한 다중 컨테이너 환경을 쉽게 구성할 수 있도록 함
