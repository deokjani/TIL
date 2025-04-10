
# Apache Airflow 학습 로드맵 및 기본 설정 정리

## 학습 로드맵 (구조화)

| 단계 | 주제 | 설명 |
|------|------|------|
| 1 | Airflow 개요 및 설정 파일 | 에어플로우 구조, 주요 개념(DAG, Task 등), airflow.cfg 이해 |
| 2 | DAG 작성 실습 | DAG 구조, PythonOperator, BashOperator, Task 관계 설정 |
| 3 | Scheduler & Webserver 구성 | 에어플로우의 실행 흐름과 UI 이해 |
| 4 | 다양한 Operator 사용 | Sensor, Branch, Trigger Rule, TaskGroup 등 활용 |
| 5 | 에어플로우 확장 | 커스텀 플러그인, XCom, Variable, Connection 사용 |
| 6 | Docker & Prod 구성 | Docker-Compose 기반 개발환경 구성, 운영 환경 설계 |
| 7 | CI/CD & DevOps 연동 | GitHub Actions, Slack 알림, Airflow Monitoring 구성 |

---

## 1단계: Airflow 기본 개념과 설정 파일

### 1. Airflow 핵심 개념 요약

| 용어 | 설명 |
|------|------|
| DAG (Directed Acyclic Graph) | 작업의 흐름(워크플로우)을 정의한 그래프 |
| Task | DAG 내의 하나의 작업 단위 |
| Operator | Task가 실제로 수행할 작업 정의 (예: PythonOperator, BashOperator) |
| Scheduler | DAG 실행을 트리거함 (스케줄 기반 실행) |
| Executor | Task를 실제로 실행함 (Sequential, Local, Celery, Kubernetes 등) |
| Webserver | UI 대시보드를 제공, DAG/Task 실행 상태를 시각화 |

---

### 2. airflow.cfg에서 자주 설정하는 항목

| 섹션 | 키 | 설명 | 예시 |
|------|----|------|------|
| [core] | executor | 실행기 설정 (SequentialExecutor, LocalExecutor, CeleryExecutor) | LocalExecutor |
|        | dags_folder | DAG 파일 저장 위치 | /opt/airflow/dags |
|        | sql_alchemy_conn | 메타데이터 DB 연결 문자열 | sqlite:///airflow.db, postgresql+psycopg2://user:pass@host/db |
|        | load_examples | 예제 DAG 로딩 여부 | False |
| [webserver] | web_server_port | 웹서버 포트 번호 | 8080 |
|             | authenticate | 로그인 인증 여부 | False |
| [scheduler] | dag_dir_list_interval | DAG 폴더 스캔 주기 (초) | 30 |
|             | max_active_runs_per_dag | DAG당 최대 동시 실행 수 | 1 |
| [logging] | base_log_folder | 로그 저장 폴더 위치 | /opt/airflow/logs |
|           | remote_logging | 원격 로그 전송 여부 | False |

---

### 3. Airflow 설정 변경 팁

- airflow.cfg 파일을 수동으로 수정하거나,
- 환경변수 (예: AIRFLOW__CORE__EXECUTOR)를 통해 재정의 가능
- 설정 반영을 위해선 일부 서비스 재시작 필요 (예: scheduler, webserver)

---

## 다음 학습 단계 제안

- DAG 파일 직접 작성 및 테스트
- 다양한 Operator 사용 실습 (PythonOperator, BashOperator 등)
- Docker 기반 Airflow 환경 구성
- Airflow UI에서 DAG 등록 및 실행 실습
