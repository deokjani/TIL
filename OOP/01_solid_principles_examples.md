
# SOLID 원칙 예시 (Spring 기반)

---

## 1. 단일 책임 원칙 (SRP - Single Responsibility Principle)
- 클래스는 하나의 책임만 가져야 한다.
- 즉, 변경의 이유가 하나뿐이어야 한다.

### 예시 (Spring Service 분리)
```java
// 책임 분리 전
public class UserService {
    public void register(User user) { ... }
    public void sendWelcomeEmail(User user) { ... }  // 이메일 책임도 포함
}

// 책임 분리 후
public class UserService {
    public void register(User user) { ... }
}

public class EmailService {
    public void sendWelcomeEmail(User user) { ... }
}
```

---

## 2. 개방-폐쇄 원칙 (OCP - Open Closed Principle)
- 확장에는 열려 있어야 하고, 변경에는 닫혀 있어야 한다.

### 예시 (Strategy 패턴으로 인증 방식 확장)
```java
public interface AuthStrategy {
    void authenticate(User user);
}

public class PasswordAuthStrategy implements AuthStrategy {
    public void authenticate(User user) { ... }
}

public class OAuthStrategy implements AuthStrategy {
    public void authenticate(User user) { ... }
}

// 새로운 전략 추가 시 기존 코드는 수정 필요 없음
```

---

## 3. 리스코프 치환 원칙 (LSP - Liskov Substitution Principle)
- 서브 타입은 기반 타입으로 교체 가능해야 한다.

### 예시 (Spring에서 User → AdminUser로 대체 가능)
```java
public class User {
    public String getRole() { return "USER"; }
}

public class AdminUser extends User {
    @Override
    public String getRole() { return "ADMIN"; }
}

// User를 사용하는 메서드에 AdminUser도 전달 가능
```

---

## 4. 인터페이스 분리 원칙 (ISP - Interface Segregation Principle)
- 클라이언트는 사용하지 않는 메서드에 의존하지 않아야 한다.

### 예시 (역할별 인터페이스 분리)
```java
public interface Writer {
    void write();
}

public interface Reader {
    void read();
}

public class FileManager implements Reader, Writer {
    public void read() { ... }
    public void write() { ... }
}
```

---

## 5. 의존 역전 원칙 (DIP - Dependency Inversion Principle)
- 고수준 모듈은 저수준 모듈에 의존하면 안 된다.
- 둘 다 추상화에 의존해야 한다.

### 예시 (Spring의 @Autowired 인터페이스 기반 DI)
```java
public interface NotificationService {
    void notify(String message);
}

@Service
public class EmailNotificationService implements NotificationService {
    public void notify(String message) { ... }
}

@Service
public class AlertService {
    private final NotificationService notificationService;

    @Autowired
    public AlertService(NotificationService notificationService) {
        this.notificationService = notificationService;
    }
}
```
