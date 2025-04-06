# Spring Framework vs Spring Boot 전체 구조 및 설정 비교

## 1. 개요

Spring Boot는 기존 Spring Framework의 복잡한 설정(XML, web.xml 등)을 간소화하고, 빠르게 웹 애플리케이션을 개발할 수 있도록 지원하는 프레임워크입니다.

---

## 2. 구조 비교

### Spring Framework 디렉토리 예시

```
src/
 ├── main/
 │   ├── java/
 │   │   └── com/example/
 │   │       ├── controller/
 │   │       ├── service/
 │   │       └── repository/
 │   ├── resources/
 │   │   ├── context-root.xml
 │   │   ├── dispatcher-servlet.xml
 │   │   └── application.properties
 │   └── webapp/
 │       └── WEB-INF/
 │           ├── web.xml
 │           └── views/
```

### Spring Boot 디렉토리 예시

```
src/
 └── main/
     ├── java/
     │   └── com/example/
     │       ├── DemoApplication.java
     │       └── config/
     │           └── WebConfig.java
     ├── resources/
     │   ├── application.yml
     │   └── templates/
     └── static/
```

---

## 3. 주요 차이점

| 항목 | Spring Framework | Spring Boot |
|------|------------------|-------------|
| 설정 방식 | XML (web.xml, context-*.xml) | Java Config, application.yml |
| Servlet 등록 | web.xml에서 수동 설정 | 자동 등록 (DispatcherServlet 포함) |
| 필터/리스너 등록 | web.xml에서 명시 | Java Config 또는 자동 처리 |
| 실행 방식 | WAR + 외부 톰캣 | JAR + 내장 톰캣 실행 (`java -jar`) |
| 정적 리소스 | 서블릿으로 직접 매핑 | /static, /public 등 자동 처리 |
| View 설정 | ViewResolver XML에 설정 | yml 또는 Java Config에서 설정 |
| JPA 설정 | datasource, entity 설정 수동 | 자동 구성 (starter + yml 기반) |
| 테스트 설정 | context 로딩 복잡 | @SpringBootTest로 간편 테스트 |
| 로깅 설정 | log4j/logback XML 설정 | 기본 logback or log4j2 + yml 구성 가능 |

---

## 4. Java Config 예시 (Spring Boot)

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {

  @Override
  public void addViewControllers(ViewControllerRegistry registry) {
    registry.addViewController("/home").setViewName("home");
  }

  @Bean
  public FilterRegistrationBean<CharacterEncodingFilter> encodingFilter() {
    CharacterEncodingFilter filter = new CharacterEncodingFilter();
    filter.setEncoding("UTF-8");
    filter.setForceEncoding(true);
    FilterRegistrationBean<CharacterEncodingFilter> bean = new FilterRegistrationBean<>(filter);
    bean.addUrlPatterns("/*");
    return bean;
  }
}
```

---

## 5. 마이그레이션 체크리스트

- web.xml 제거 → @SpringBootApplication 도입
- context-*.xml 제거 → Java Config로 대체
- DispatcherServlet 등록 제거
- application.yml 또는 application.properties로 설정 통합
- JAR 기반 실행 구조로 전환 (내장 톰캣 사용)
- view, filter, static 설정을 Config class로 이동

## Spring Framework vs Spring Boot 주요 차이점 총정리

| 항목 | Spring Framework | Spring Boot |
|------|------------------|-------------|
| 설정 방식 | XML 또는 Java Config 수동 설정 | 대부분 자동 설정 + application.yml |
| 서블릿 등록 | web.xml에서 DispatcherServlet 명시 | 자동 등록 |
| Tomcat 실행 | WAR 배포 → 외부 Tomcat 필요 | 내장 Tomcat 실행 → java -jar |
| build 방식 | 일반 Maven/Gradle 구성 | starter 의존성으로 간단히 구성 |
| 실행 진입점 | 따로 main() 없음 → WAR로 배포 | @SpringBootApplication + main() |
| JPA 설정 | 수동 설정 필요 | 자동 설정 + EntityScan, DataSource 설정 자동화 |
| 로깅 설정 | log4j.xml, logback.xml 수동 설정 | application.yml로 제어, SLF4J 통합 |
| 환경변수 설정 | 복잡한 profile 구성 | application-{profile}.yml 지원 |
| Actuator 모니터링 | 직접 구현해야 함 | actuator 자동 내장 (/actuator/health 등) |
| 테스트 환경 설정 | 복잡한 context 구성 필요 | @SpringBootTest 하나로 통합 |
| 배포 편의성 | WAS 연동 필요 | java -jar로 즉시 실행 가능 |
| REST 지원 | 설정 필요 | @RestController 기본 내장 |
| 라이프사이클 | 복잡한 설정 필요 | AutoConfiguration 기반 단순화 |

## 실무 개발자 관점에서 차이

| 관점 | 전통 스프링 | 스프링 부트 |
|------|-------------|-------------|
| 생산성 | 초반 설정 시간 많이 듦 | 빠르게 개발 시작 가능 |
| 러닝 커브 | 명시적이라 배우기 좋음 | 자동화되어 있어서 내부가 감춰짐 |
| 유연성 | 복잡한 시스템에 유리 | 표준적인 구조에서 강점 |
| 확장성 | 세세하게 제어 가능 | 복잡한 설정은 오히려 어려울 수 있음 |

## 디렉토리 구조 차이

| Spring Framework | Spring Boot |
|------------------|-------------|
| src/main/webapp/WEB-INF/web.xml | 없음 (Servlet 자동 등록) |
| context-*.xml, *-servlet.xml | 없음 or Java Config |
| 별도 설정 class | @SpringBootApplication으로 통합 |
| 정적 파일: /resources/ | /static/, /public/, /resources/ 자동 제공 |

## Spring Boot이 제공하는 대표 자동화

| 기능 | 자동 설정 예 |
|------|-------------------------------|
| JPA | spring.datasource.*, spring.jpa.* 설정만 하면 EntityManager 자동 구성 |
| Security | 의존성만 넣으면 로그인 화면까지 자동 제공 |
| Thymeleaf | spring.thymeleaf.*만으로 동작 |
| Embedded Tomcat | 별도 설정 없이 실행 (@SpringBootApplication) |

## 결론 요약

| 구분 | Spring Framework | Spring Boot |
|------|------------------|-------------|
| 진입장벽 | 낮음 (직접 컨트롤 가능) | 높을 수 있음 (자동화된 구조 이해 필요) |
| 생산성 | 낮음 | 매우 높음 |
| 설정 | 수동 위주 (web.xml, context.xml) | 자동 위주 (yml, starter, auto-config) |
| 실무 사용 | 유지보수성 좋음 (대기업 레거시에서 종종 사용) | 스타트업, 신규 프로젝트 대부분 사용 |