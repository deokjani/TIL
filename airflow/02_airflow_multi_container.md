
# Airflow 멀티 컨테이너 구성 확장 가이드

Airflow를 실무 환경에서 확장할 때 자주 사용하는 외부 서비스들을 멀티 컨테이너 환경으로 구성할 수 있습니다. 다음은 각 구성요소에 대한 설명과 함께 멀티 컨테이너 아키텍처 설계를 위한 가이드입니다.

## 확장 대상 구성요소

| 구성요소 | 설명 |
|----------|------|
| PostgreSQL | Airflow 메타데이터를 저장하는 외부 데이터베이스 |
| Redis | CeleryExecutor 또는 Worker 간 메시지 브로커로 사용 |
| Flower | Celery 작업 모니터링 및 대시보드 |
| Prometheus | 메트릭 수집 도구 (Airflow, Worker 상태 모니터링 등) |
| Grafana | Prometheus로 수집된 메트릭 시각화 도구 |
| Slack Webhook | Airflow DAG 실패나 경고를 알림으로 전송할 수 있음 |

---

## PostgreSQL 구성

Airflow의 metadata DB로 사용. SQLite 대신 운영 환경에서는 PostgreSQL을 권장.

```yaml
services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    ports:
      - "5432:5432"
```

---

## Redis 구성

CeleryExecutor 사용 시 필수. Task queue를 관리.

```yaml
services:
  redis:
    image: redis:latest
    ports:
      - "6379:6379"
```

---

## Flower 구성

Celery 작업 상태를 시각적으로 확인 가능한 UI 제공.

```yaml
services:
  flower:
    image: mher/flower
    environment:
      - FLOWER_PORT=5555
    ports:
      - "5555:5555"
    command: >
      flower --broker=redis://redis:6379/0
```

---

## Prometheus 구성

Airflow 메트릭 수집용. statsd-exporter와 연동하여 DAG 수행 지표 수집.

```yaml
services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
```

---

## Grafana 구성

Prometheus에서 수집한 메트릭을 시각화.

```yaml
services:
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana-storage:/var/lib/grafana
```

---

## Slack 연동 (옵션)

Slack Webhook을 통해 DAG 실패, 경고 등을 알림으로 수신할 수 있음.

- Airflow에서 PythonOperator로 Slack 알림 전송 가능
- 또는 Alert 기능으로 실패 시 Slack 전송 설정

```python
from airflow.operators.python import PythonOperator
import requests

def slack_alert(context):
    requests.post(
        url="https://hooks.slack.com/services/your/webhook/url",
        json={"text": f"DAG Failed: {context['dag'].dag_id}"}
    )
```

---

## 실행 순서 요약

1. PostgreSQL → Redis → Prometheus → Grafana → Flower 등 순서대로 컨테이너 실행
2. Airflow 구성에서 `executor = CeleryExecutor`, DB 연결 문자열 변경
3. Prometheus, Grafana, Slack 등은 필요에 따라 추가적으로 연동 설정

---

## 실무 적용 팁

- 모든 컨테이너를 `docker-compose.yml`에 통합
- `.env` 파일로 공통 환경변수 관리
- `depends_on`으로 컨테이너 실행 순서 제어
- Airflow 로그 및 데이터 볼륨 외부 마운트

