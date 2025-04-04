# Docker 기초 & 실무 흐름 정리

---

## 1. Docker란?

Docker는 컨테이너 기반 가상화 플랫폼으로, 애플리케이션과 실행 환경을 하나의 패키지(이미지)로 묶어  
개발부터 배포, 운영까지 동일한 환경을 유지할 수 있도록 도와준다.

### 실무에서의 Docker 활용 이유

- 환경 차이로 인한 "로컬에선 되는데 서버에선 안 돼요" 문제 해결
- 팀원 간 동일한 개발 환경 공유
- 테스트, 배포 자동화 가능 (CI/CD 파이프라인에 자연스럽게 통합)
- 마이크로서비스 구조 운영에 최적화

---

## 2. Docker 핵심 구성 요소

| 구성 요소             | 설명 |
|----------------------|------|
| 이미지 (Image)        | 애플리케이션과 실행 환경이 포함된 불변 패키지 |
| 컨테이너 (Container)  | 이미지를 실행한 인스턴스 (격리된 환경에서 실행됨) |
| Dockerfile           | 이미지를 만들기 위한 명세 파일 (레시피) |
| docker-compose.yml   | 여러 컨테이너를 한 번에 구성하고 실행하는 설정 파일 |
| 볼륨 (Volume)         | 컨테이너 외부와 데이터를 주고받는 경로 (데이터 영속성 유지) |
| 네트워크 (Network)    | 컨테이너 간 통신을 위한 가상 네트워크 |

---

## 3. Docker 기본 실행 흐름 요약

1. `Dockerfile` 작성 → 이미지 생성 (`docker build`)
2. `docker compose`로 여러 컨테이너 실행
3. 컨테이너 안에서 서비스가 실행됨
4. `docker exec`으로 내부 접속 가능
5. `docker logs`, `docker ps`로 상태 확인
6. 작업이 끝나면 `docker compose down`으로 종료 및 정리

---

## 4. Dockerfile 기본 구조 예시

```Dockerfile
FROM python:3.9                   # 베이스 이미지
WORKDIR /app                      # 컨테이너 내 작업 디렉토리 설정
COPY requirements.txt .           # 의존성 파일 복사
RUN pip install -r requirements.txt
COPY . .                           # 전체 코드 복사
CMD ["python", "app/main.py"]     # 실행 명령
```

### 설치 팁

### ENTRYPOINT vs CMD

| 항목 | CMD | ENTRYPOINT |
|------|-----|------------|
| 기본 목적 | 기본 실행 명령 제공 | 컨테이너 시작 시 반드시 실행할 명령 지정 |
| 덮어쓰기 가능 여부 | `docker run` 명령어에서 쉽게 덮어쓰기 가능 | `--entrypoint`로만 변경 가능 |
| 사용 예 | 단순 테스트/스크립트 실행용 | 실제 서비스 실행 강제 시 사용 |

예시:

```Dockerfile
CMD ["python", "app.py"]
# docker run myimage bash → CMD가 bash로 덮어짐

ENTRYPOINT ["python", "app.py"]
# docker run myimage bash → 무시되지 않고 python app.py 실행됨
```

> 실무에서는 ENTRYPOINT로 서비스 실행을 고정하고, CMD는 인자 기본값 제공 용도로 함께 사용하는 경우가 많습니다.

---

### --no-cache-dir 사용

`pip install` 시 캐시 디렉토리를 만들지 않도록 하여 이미지 크기를 줄입니다.

```Dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

- 캐시 생성을 막아 이미지 빌드 후 불필요한 용량 차지 방지
- 특히 대용량 패키지를 포함하는 경우 효과가 큼

---

### Multi-stage Build (다단계 빌드)

불필요한 빌드 도구, 테스트 파일 등을 최종 이미지에 포함시키지 않기 위한 방식

```Dockerfile
# 1단계: 빌드용 이미지
FROM python:3.9 AS builder
WORKDIR /app
COPY . .
RUN pip install --user -r requirements.txt

# 2단계: 실행용 이미지 (슬림)
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /app /app
CMD ["python", "app/main.py"]
```

- 첫 번째 스테이지에서 의존성과 빌드 수행
- 두 번째 스테이지에서는 실행에 필요한 최소한의 파일만 복사
- 이미지 용량 절감 + 보안 강화

> 실무에서는 특히 보안, 경량화, 배포 속도 향상을 위해 Multi-stage Build를 적극 활용합니다.

---

## 5. docker-compose.yml 기본 구조 예시

```yaml
version: '3.8'

services:
  hello-docker:
    build: .
    container_name: hello-container
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - TZ=Asia/Seoul
    networks:
      - default
```

### 실무에서 자주 사용하는 설정 항목

| 항목 | 설명 |
|------|------|
| `build:` | Dockerfile 경로 지정 |
| `image:` | 특정 태그의 이미지 사용 |
| `volumes:` | 로컬 ↔ 컨테이너 파일 동기화 |
| `environment:` | 환경 변수 설정 (.env 파일과 연동) |
| `depends_on:` | 실행 순서 보장 |
| `restart:` | 정책 설정 (always, unless-stopped 등) |

---

## 6. Docker 주요 명령어 정리

```bash
# 빌드 및 실행
docker compose build --no-cache
docker compose up -d

# 상태 및 로그
docker ps
docker logs [컨테이너명]

# 컨테이너 조작
docker exec -it [컨테이너명] bash
docker compose down

# 전체 클린업
docker system prune -a
```

---

## 7. 환경설정 팁

- **시간대 설정**: 모든 컨테이너에 `TZ=Asia/Seoul` 설정하여 로그 시간 일치
- **볼륨 마운트**: 코드 변경 즉시 반영되도록 `.:/app` 방식으로 설정
- **.env 파일 분리**: Git에 올리지 않도록 `.gitignore`에 추가

```bash
# .env 예시
DB_USER=myuser
DB_PASS=securepass
```

```yaml
environment:
  - DB_USER=${DB_USER}
  - DB_PASS=${DB_PASS}
```

---

## 8. Docker가 활용되는 대표 시나리오

- ETL 파이프라인 실행 (Airflow, Spark)
- 머신러닝 모델 서빙 (FastAPI, Streamlit)
- 로그 수집 및 분석 (Filebeat, Logstash, Elasticsearch)
- 데이터베이스 환경 구축 (PostgreSQL, Redis)
- 개발 테스트 환경 이식 (Jupyter, VS Code in Docker)

---

## 9. 정리

| 개념 | 요약 |
|------|------|
| 이미지 | 실행 가능한 코드 + 환경을 포함한 패키지 |
| 컨테이너 | 이미지를 실행한 상태 (격리된 프로세스) |
| Dockerfile | 이미지를 만드는 방법 정의 |
| docker-compose | 다중 컨테이너 정의 및 실행 |
| 실무 적용 | CI/CD, ETL, 분석환경, MLOps 등 전반 활용 |

---

이 문서를 기반으로 실습을 진행하면서 Dockerfile 수정, 다양한 서비스 구성, 환경변수 분리 등을 직접 적용해보면 실무에 더욱 빠르게 익숙해질 수 있습니다.
