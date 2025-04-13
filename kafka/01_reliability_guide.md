# Kafka 신뢰성 및 메시지 유실 방지 전략 정리

Kafka에서 메시지를 안전하게 처리하고 유실 없이 전송하기 위해 필요한 설정, 구조, 그리고 예시 코드를 정리한 문서입니다. 실무에서 유용하게 사용할 수 있는 내용을 포함합니다.

---

## 1. Kafka 메시지 전송 흐름

Kafka의 기본 구성요소:

- **Producer**: 메시지를 전송
- **Broker**: 메시지를 저장
- **Topic**: 메시지를 분류하는 논리적 단위
- **Partition**: 토픽을 구성하는 물리적 저장 단위
- **Leader**: Partition의 주 브로커
- **Follower**: Leader의 복제본
- **ISR (In-Sync Replicas)**: Leader와 데이터 동기화가 완료된 브로커들

### 전체 전송 흐름

```
[Producer]
  └─ (send message with acks=all)
         ↓
[Leader Broker]
  └─ 복제 → ISR Followers
         ↓
[Leader sends ack to Producer when all ISR stored]
```

---

## 2. acks 옵션 설명

| 설정 | 의미 | 데이터 신뢰성 | 성능 |
|------|------|----------------|------|
| `acks=0` | 확인 응답 없음 | 유실 위험 높음 | 매우 빠름 |
| `acks=1` | Leader만 저장 후 ack | 중간 | 중간 |
| `acks=all` | ISR 전체 저장 후 ack | 가장 안전 | 가장 느림 |

```yaml
spring:
  kafka:
    producer:
      acks: all
      retries: 5
      enable-idempotence: true
```

---

## 3. Kafka Consumer 커밋 처리

Kafka는 메시지를 읽은 뒤에도 보관하며, Consumer가 "처리 완료"를 Kafka에 알려야 다음 메시지를 줍니다. 이를 offset commit이라 합니다.

```java
@KafkaListener(topics = "order", groupId = "order-group")
public void consume(String message, Acknowledgment ack) {
    try {
        process(message);
        ack.acknowledge(); // 커밋, 다음 offset부터 메시지 제공
    } catch (Exception e) {
        // 실패 시 커밋하지 않으면 재처리 가능
    }
}
```

- `enable-auto-commit=false` 설정 필요
- 수동 커밋 방식 사용 (`Acknowledgment`)

---

## 4. ISR 복제 실패 시 메시지 유실 가능성

문제 상황:

- Leader만 메시지를 받은 상태에서 장애 발생
- Follower가 복제를 받기 전이라면, 복제본이 없음
- Kafka는 해당 메시지를 복구 불가 → 유실

---

## 5. 유실 방지 전략

### 필수 설정

```properties
# producer 설정
acks=all
enable.idempotence=true

# broker 설정
min.insync.replicas=2
unclean.leader.election.enable=false
```

- `acks=all`: 모든 ISR에 저장돼야 ack
- `min.insync.replicas`: 최소 동기화 브로커 수
- `enable.idempotence`: 정확히 한 번 전송 보장
- `unclean.leader.election=false`: 동기화 안 된 브로커는 Leader 승격 불가

---

## 6. Kafka 동작 흐름 요약

```
[Producer]
   ↓ send()
[Leader Broker]
   ↓ replicate to ISR
[ISR Brokers]
   ↓
[Leader sends ack (if acks=all)]
   ↓
[Consumer reads]
   ↓
[Consumer processes]
   ↓
[Consumer commit offset to Kafka]
```

---

## 7. 정리 요약

| 구분 | 설정/전략 | 설명 |
|------|-------------|------|
| Producer → Broker | `acks=all`, `retries`, `idempotence` | 모든 ISR에 저장 후 ack |
| Broker 내 설정 | `min.insync.replicas`, `unclean.leader.election` | 복제 실패 시 쓰기 차단 |
| Consumer 처리 | `enable-auto-commit=false`, `ack.acknowledge()` | 처리 후 수동 커밋 |
| 장애 발생 대응 | DLQ 사용, retry 전략 | 메시지 손실 방지 및 보완

---