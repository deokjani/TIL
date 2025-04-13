# Spring Transaction 정리

이 문서는 Spring Framework에서 `@Transactional`을 중심으로 한 트랜잭션 처리 개념, AOP 동작 원리, 예외 처리, 비동기 이벤트 분리 및 정합성 보장 전략 등을 정리한 지침서입니다.

---

## 1. `@Transactional` 기본 개념

- Spring의 트랜잭션은 AOP(프록시) 기반으로 작동
- 기본적으로 메서드 실행 전 트랜잭션 시작 → 정상 종료 시 commit, 예외 발생 시 rollback

### 기본 규칙

| 조건 | 롤백 여부 |
|------|----------|
| `RuntimeException`, `Error` 발생 | 롤백됨 |
| `Checked Exception` 발생 | 롤백 안됨 |
| `rollbackFor = Exception.class` 명시 | 롤백됨 |
| 예외가 발생했지만 `try-catch`로 잡고 끝냄 | 롤백 안됨 |

### 예시

```java
@Transactional
public void save() throws IOException {
    throw new IOException("기본적으로 롤백 안 됨");
}
```

```java
@Transactional(rollbackFor = Exception.class)
public void save() throws IOException {
    throw new IOException("이제는 롤백 됨");
}
```

---

## 2. 내부 메서드 호출 시 트랜잭션 미적용

- Spring의 AOP는 프록시 기반 → 외부에서 호출해야 트랜잭션 적용됨
- 자기 자신이 `this.method()` 형태로 내부 메서드 호출하면 프록시를 통하지 않아 트랜잭션이 작동하지 않음

### 해결 방법

- 구조 분리 (다른 클래스에서 호출)
- ApplicationContext로 프록시 객체 직접 주입

```java
@Autowired
private ApplicationContext context;

public void doLogic() {
    context.getBean(UserService.class).subLogic(); // 프록시를 통해 트랜잭션 적용
}
```

---

## 3. 비동기 이벤트 활용

- 핵심 로직과 부가 로직을 분리하고, 부가 로직은 비동기적으로 실행
- 응답 지연 최소화, 트랜잭션 분리, 확장성 확보

### 구조 예시

```java
@Transactional
public void processOrder(Order order) {
    orderRepository.save(order);
    eventPublisher.publishEvent(new OrderEvent(order)); // 이벤트 발행
}
```

```java
@Async
@EventListener
public void handleOrderEvent(OrderEvent event) {
    emailService.sendEmail(...);
}
```

- 핵심 로직은 빠르게 커밋
- 이벤트 리스너는 트랜잭션 외부에서 비동기 실행

---

## 4. 비동기 이벤트 실패 시 정합성 문제

핵심 로직은 성공했지만, 비동기 부가 로직이 실패할 경우 정합성 깨질 수 있음

### 대응 전략

1. **Retry 처리**
   - 실패한 이벤트를 DB나 큐에 저장 후 재처리

2. **보상 트랜잭션**
   - 반대 작업으로 정합성 복구

3. **상태 테이블 관리**
   - 이벤트 상태를 명시적으로 기록

4. **Kafka 등 메시지 브로커 활용**
   - 안정적인 비동기 메시징 처리

---

## 5. 팁 요약

| 상황 | 처리 방법 |
|------|-----------|
| 내부 메서드 트랜잭션 적용 안 됨 | 서비스 분리 또는 ApplicationContext 주입 |
| Checked 예외 rollback | `rollbackFor` 명시 |
| 트랜잭션 종료 후 부가 작업 | 이벤트 + `@Async` |
| 부가 작업 실패 대응 | Retry, 상태 관리, Kafka DLQ 등 |
| 느린 외부 API 호출 분리 | 비동기 이벤트로 처리 |

---