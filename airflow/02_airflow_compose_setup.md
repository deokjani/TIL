# Docker Compose 기반 Airflow 구성 설명

---

## 1. Docker Compose란?

Docker Compose는 여러 컨테이너 서비스를 하나의 설정 파일(`docker-compose.yml`)로 정의하여  
한 번에 실행, 중지, 삭제, 관리할 수 있게 해주는 도구입니다.

실무에서는 DAG 실행을 위한 **Airflow + PostgreSQL + Redis + Monitoring 도구**까지  
모두 함께 배포 가능한 구조로 활용됩니다.

---

## 2. Airflow 주요 컴포넌트 구성

| 컴포넌트     | 설명 |
|--------------|------|
| Webserver    | 웹 UI 제공, DAG 상태 확인 및 트리거 |
| Scheduler    | DAG 실행 시간 확인, Task 실행 담당 |
| PostgreSQL   | 메타데이터 저장소 (Task 상태, 실행 기록 등) |
| Worker (옵션) | CeleryExecutor 사용 시 필요 |
| Redis (옵션) | CeleryExecutor 큐 관리 용도 |
| Flower (옵션) | 워커 상태 모니터링 |
| Volume       | DAG 및 로그 등 외부 데이터 저장소로 연결 |

---

## 3. 실무에서 중요하게 보는 Airflow Docker 설정 포인트

### 컨테이너 분리
- 개발용에서는 `webserver`, `scheduler`를 하나로 합칠 수 있으나  
  **실무에선 일반적으로 각 역할별로 별도 컨테이너 구성**  
  → 배포, 모니터링, 확장성 확보를 위해

### 환경 변수 관리
- `AIRFLOW__` 형태로 모든 설정 커스터마이징 가능
- 실무에선 `.env` 또는 `secrets manager`로 환경변수를 외부화함
- 민감 정보(`DB 비밀번호`, `Slack URL`, `API Key`)는 코드에 직접 쓰지 않음

### 로그 관리
- `logs`를 volume으로 연결하여 **외부에서 실시간 확인 가능**하게 구성
- 실무에서는 로그를 **ELK Stack / S3 / CloudWatch** 등에 연동

### DAG 자동 감지
- `AIRFLOW__CORE__DAG_DISCOVERY_SAFE_MODE=False` 설정을 통해  
  DAG 파일 변경 시 자동으로 반영되도록 구성
- `airflow dags reserialize` 명령으로 수동 강제 인식도 가능

### Slack / Alert 연동
- 실무에서는 DAG 실패 시 Slack 알림을 통해 **모니터링 자동화** 필수
- `SLACK_WEBHOOK_URL` 설정 필요 + 공통 Operator로 래핑

---

## 4. Webserver ↔ Scheduler 실행 흐름 (실무 기준)

```text
사용자 DAG 등록 → PostgreSQL 저장
    ↓
Scheduler가 주기적으로 DB 스캔
    ↓
Task 실행 조건 확인 → 실행
    ↓
Task 실행 로그 저장
    ↓
Webserver에서 상태 확인
```

> 모든 컴포넌트는 DB를 통해 간접적으로 동기화되며, 로그는 파일 또는 외부 스토리지로 저장됨

---

## 5. docker-compose 핵심 체크리스트

| 항목 | 설명 |
|------|------|
| DAG 반영 확인 | scheduler가 변경된 DAG 인식하는지 확인 (재시작 or reserialize 필요) |
| 로그 확인 | 볼륨 연결 상태 or 외부 저장소 연동 여부 확인 |
| 환경 변수 관리 | .env 파일 외부 저장 및 gitignore 처리 |
| Alert 연동 | Slack 연동, AirflowFailureAlert 정의 여부 |
| DAG 실행 실패 대응 | `try_number`, `log`, `email_on_failure`, `retry_delay` 등 설정 |
| 실행 시간 동기화 | 컨테이너 시간대 설정 (`TZ`, `default_timezone`) |

---

## 6. 실습에 활용 가능한 확장 포인트

- Flower 추가: 워커 상태 대시보드 확인
- Redis 연동: CeleryExecutor로 분산 실행 실습
- Prometheus + Grafana 연동: DAG 실행 상태, Task 성공률 모니터링
- S3 또는 MinIO 연동: 로그, 결과 저장 백업
- GitHub Actions 연동: DAG CI/CD 배포 자동화

---

## 7. 마무리 요약

| 항목 | 정리 |
|------|------|
| 분리 실행 | webserver / scheduler는 컨테이너 분리 권장 |
| 로그 관리 | 외부 로그 연동 필수 (ELK/S3 등) |
| Alert 설정 | Slack 연동 + 실패 감지 설정 |
| 환경변수 보안 | 민감정보는 .env / Secrets Manager 사용 |
| DAG 버전 관리 | Git + CI/CD로 버전 추적 & 자동 배포 |

---

> 이 구성은 실무에서 사용하는 Airflow 배포와 가장 유사한 형태로,  
> 향후 ML 파이프라인, ETL, 데이터 마트 구축 시 중요한 기반이 됩니다.
