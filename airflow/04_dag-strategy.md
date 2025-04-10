# Airflow 주요 개념 정리

Airflow는 워크플로우를 자동화하고 스케줄링하는 플랫폼입니다. DAG, Task, Operator 등 핵심 구성 요소를 통해 데이터 파이프라인을 구성하고 관리할 수 있습니다.

---

## 1. DAG 간 의존성 설정

Airflow에서 Task 간 실행 순서는 연산자(`>>`, `<<`) 또는 `set_upstream()`, `set_downstream()` 메서드를 통해 정의합니다.

### 예시
```python
fetch_data >> clean_data >> train_model >> register_model
```

각 Task는 명확한 역할을 가지며, 의존 관계를 설정하지 않으면 누락, 중복 실행 등의 문제가 발생할 수 있습니다.

---

## 2. TriggerRule

TriggerRule은 Task가 실행되기 위한 조건을 설정하는 옵션입니다. 기본값은 `ALL_SUCCESS`로, 모든 이전 Task가 성공해야 실행됩니다.

### 주요 옵션
- `ALL_SUCCESS`: 기본값. 모든 이전 Task 성공 시 실행
- `ONE_FAILED`: 하나라도 실패하면 실행
- `ALL_FAILED`: 모두 실패한 경우 실행
- `ALL_DONE`: 성공/실패 상관없이 실행

### 사용 예시
Slack 알림과 같은 Task는 실패하더라도 반드시 실행되어야 하므로 `TriggerRule.ONE_FAILED`나 `ALL_DONE`을 사용합니다.

---

## 3. SLA (Service Level Agreement)

SLA는 특정 Task가 지정된 시간 내에 완료되지 않을 경우 경고를 발생시킵니다.  
지연되는 작업을 빠르게 감지하고 대응할 수 있도록 도와줍니다.

### 예시
```python
sla=timedelta(minutes=30)
```

SLA 미스는 Slack 또는 이메일로 알림을 설정해 감시할 수 있습니다.

---

## 4. Retry 설정

일시적인 오류에 대비해 Task 재시도 횟수와 재시도 간격을 설정할 수 있습니다.

### 예시
```python
retries=3,
retry_delay=timedelta(minutes=10)
```

외부 API 호출, DB 연결 등 실패 가능성이 높은 Task에서 주로 사용합니다.

---

## 5. Slack 알림 연동

Airflow는 PythonOperator를 통해 Slack Webhook URL로 메시지를 전송할 수 있습니다.  
주로 실패 감지, SLA 미스, 워크플로우 종료 알림 등에 활용됩니다.

### 예시
```python
def send_slack_alert(context):
    error_message = context.get("exception")
    requests.post(SLACK_WEBHOOK_URL, json={"text": f"Task 실패: {error_message}"})
```

---

## 6. 기타 개념 요약

| 개념 | 설명 |
|------|------|
| DAG | Directed Acyclic Graph. Task들의 실행 순서를 정의한 구조 |
| Operator | 실제 작업을 수행하는 단위. PythonOperator, BashOperator 등 |
| Task | DAG 내에서 실행되는 개별 작업 단위 |
| `>>`, `<<` | Task 간 실행 순서를 나타내는 연산자 (operator overloading) |
| SLA Miss Callback | SLA를 초과했을 때 실행되는 함수 또는 알림 트리거 |
| Retry 전략 | 실패한 Task를 일정 횟수/시간 간격으로 재실행하는 설정 |

---

## 핵심 요약

- DAG는 Task 간의 흐름을 정의하며 `>>` 연산자를 통해 순서를 설정
- TriggerRule로 Task 실행 조건을 세밀하게 조절 가능
- SLA는 지연 감지용, Slack 알림과 함께 사용 시 빠른 대응 가능
- Retry는 실패 복구용. 네트워크/외부 시스템 Task에 효과적

Airflow의 이 개념들을 조합하면 신뢰성과 확장성이 높은 데이터 파이프라인을 구축할 수 있습니다.
