
# Spring 초급 개념 정리

## 1. IoC / DI (제어의 역전 / 의존성 주입)

### 개념
- IoC: 객체 생명 주기를 스프링이 관리하는 구조
- DI: 필요한 의존 객체를 외부에서 주입 받는 구조

### 예제
```java
@Service
public class BookService {
    private final BookRepository repo;

    public BookService(BookRepository repo) {
        this.repo = repo;
    }
}
```

---

## 2. Bean 등록

### 주요 어노테이션
| 어노테이션 | 설명 |
|------------|------|
| @Component | 일반적인 컴포넌트 |
| @Service | 서비스 계층 |
| @Repository | DAO 계층 |
| @Controller / @RestController | 웹 요청 처리 |
| @Bean | 수동 등록 |

### 예제
```java
@Component
public class HelloPrinter {
    public void print() {
        System.out.println("Hello");
    }
}
```

---

## 3. Spring Boot 시작

```java
@SpringBootApplication
public class DemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }
}
```

- @SpringBootApplication = @Configuration + @ComponentScan + @EnableAutoConfiguration

---

## 4. MVC 구조

### 흐름
```
클라이언트 → Controller → Service → Repository → DB
```

### 예제
```java
@RestController
public class BookController {
    private final BookService service;

    public BookController(BookService service) {
        this.service = service;
    }

    @GetMapping("/books")
    public List<Book> listBooks() {
        return service.getBooks();
    }
}
```

---

## 5. REST API

| 어노테이션 | 설명 |
|------------|------|
| @RestController | JSON 반환용 컨트롤러 |
| @GetMapping | GET 요청 처리 |
| @PostMapping | POST 요청 처리 |
| @RequestBody | 요청 본문 JSON → 객체 변환 |

### 예제
```java
@RestController
public class UserController {
    @GetMapping("/users")
    public List<User> getUsers() {
        return List.of(new User("홍길동"), new User("김영희"));
    }
}
```

---

## 6. JPA 기초

| 구성 요소 | 설명 |
|-----------|------|
| @Entity | DB 테이블과 매핑되는 클래스 |
| @Id | 기본 키 식별자 |
| JpaRepository<T, ID> | 기본 CRUD 지원 |
| @Transactional | 트랜잭션 처리 |

### 예제
```java
@Entity
public class Book {
    @Id
    @GeneratedValue
    private Long id;
    private String title;
}
```

```java
public interface BookRepository extends JpaRepository<Book, Long> {
    List<Book> findByTitleContaining(String keyword);
}
```

---

## 요약

| 주제 | 핵심 설명 |
|------|-----------|
| IoC / DI | 객체를 직접 만들지 않고 스프링이 관리/주입 |
| Bean 등록 | 어노테이션으로 스프링이 자동 인식 |
| 부트 시작 | @SpringBootApplication + main() |
| MVC 구조 | 요청 → Controller → Service → Repository |
| REST API | @RestController + @GetMapping |
| JPA 기초 | Entity와 Repository로 객체-DB 매핑 |
