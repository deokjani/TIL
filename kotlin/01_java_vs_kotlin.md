# Java & Kotlin 공통 기본기 정리 (비교 중심)

## 1. `final` 키워드

### Java에서의 사용
```java
final int MAX = 100; // 값 재할당 불가

final class A {}     // 클래스 상속 불가

class B {
    final void doSomething() {
        System.out.println("변경 금지 메서드");
    }
}
```

- 변수: 값 재할당 불가
- 메서드: 오버라이딩 불가
- 클래스: 상속 불가

---

## 1.5 Kotlin의 `final`과 `open` 개념 차이

### 기본값 차이

| 항목 | Java | Kotlin |
|------|------|--------|
| 변수 상수 선언 | `final int x = 1;` | `val x = 1` (자동 불변) |
| 메서드 오버라이드 방지 | `final void method()` | `final`이 기본값 |
| 클래스 상속 방지 | `final class MyClass` | `class MyClass` (기본이 final) |

### Kotlin의 기본 동작 예시
```kotlin
class Animal      // 기본은 final
// class Dog : Animal() // 오류 (open 필요)

open class Animal2
class Dog2 : Animal2()  // OK
```

```kotlin
open class Animal {
    open fun speak() = println("소리")
}

class Dog : Animal() {
    override fun speak() = println("멍멍")
}
```

### 결론

- Kotlin은 기본이 `final` → 안전 기본 설계
- `open`을 붙여야 상속 및 오버라이딩 가능
- `val`은 Java의 `final`과 유사 (재할당 불가)

---

## 2. `equals()`와 `hashCode()`

### 역할
- `equals()`: 두 객체의 내용 비교
- `hashCode()`: Hash 자료구조에서 객체 식별용

### Java 예시
```java
@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof User)) return false;
    User user = (User) o;
    return this.id.equals(user.id);
}

@Override
public int hashCode() {
    return Objects.hash(id);
}
```

- equals가 같으면 hashCode도 같아야 함
- 변경 가능한 필드(id 등)를 기준으로 사용할 경우 주의 필요

### Kotlin의 차별점
- `data class`는 equals/hashCode 자동 생성
- 불변 프로퍼티(val)를 사용하여 해시 기반 컬렉션에서 안전성 높임
- `copy()` 메서드로 변경 시 새 객체 생성 → 기존 해시 불변 유지

```kotlin
data class User(val id: Long)

val set = hashSetOf(User(1))
println(User(1) in set) // true

val user = User(1)
val updated = user.copy(id = 2) // 새로운 객체 → 기존 user 영향 없음
```

---

## 3. Kotlin의 `data class`

### 장점
- `equals()`, `hashCode()`, `toString()`, `copy()`, `componentN()` 자동 생성
- 간결하고 명확한 데이터 모델링 가능

### 예시
```kotlin
data class User(val id: Long, val name: String)

val u1 = User(1, "Tom")
val u2 = u1.copy(name = "Jane")
val (id, name) = u1 // 구조 분해
```

---

## 4. Kotlin의 Null-Safety vs Java의 Null 처리

### Kotlin: 타입 수준에서 null 가능 여부 구분
```kotlin
val a: String = "hello"     // null 불가
val b: String? = null       // null 허용
```

### Java: 모든 참조 타입이 기본적으로 null 가능
```java
String name = null; // 기본적으로 가능
```

### Kotlin 주요 문법

| 문법 | 설명 | 예시 |
|------|------|------|
| `?.` | null-safe 호출 | `user?.name` |
| `!!` | 강제 not-null | `user!!.name` |
| `?:` | 기본값 설정 (Elvis 연산자) | `user?.name ?: "Guest"` |
| `let` | null 아닐 때 블록 실행 | `user?.let { println(it) }` |

---

## 5. Kotlin에서의 예외 처리 vs Java

| 항목 | Java | Kotlin |
|------|------|--------|
| Checked Exception | 있음 (`throws IOException`) | 없음 |
| 강제 try-catch 여부 | 컴파일러가 강제함 | 개발자 선택 |
| 대표 함수 | `try { } catch { }` | 동일 |

### Kotlin 예시
```kotlin
try {
    val content = File("data.txt").readText()
} catch (e: IOException) {
    println("에러: ${e.message}")
}
```

---

## 6. Kotlin 컬렉션: 변경 가능 여부 vs Java

| 항목 | Java | Kotlin |
|------|------|--------|
| 불변 컬렉션 | 명시적으로 구현 필요 | `listOf()` 등 기본 제공 |
| 변경 가능 컬렉션 | `ArrayList`, `LinkedList` | `mutableListOf()`, `arrayListOf()` |
| 안전성 | 실수로 수정 가능 | 타입 수준에서 제한 가능 (`val`, `listOf`) |

### Kotlin 예시
```kotlin
val names = listOf("a", "b")        // 불변
val mNames = mutableListOf("a", "b") // 변경 가능
mNames.add("c")
```

---

## 7. SAM 변환 (Single Abstract Method)

| 항목 | Java | Kotlin |
|------|------|--------|
| SAM 지원 | 기본 지원 (`Runnable`) | `fun interface` 필요 |
| 람다 표현 | `(e) -> {}` | 동일 |
| 제한 | 없음 | Kotlin 인터페이스는 명시 필요 |

### Kotlin 예시
```kotlin
fun interface ClickListener {
    fun onClick(msg: String)
}

val listener = ClickListener { println("Clicked $it") }
```

### Java 인터페이스 사용 예시
```kotlin
val r = Runnable { println("Run") } // Java SAM 변환 가능
```

---

## 8. componentN() 함수 (Kotlin 전용 기능)

| 항목 | Java | Kotlin |
|------|------|--------|
| 구조 분해 | 지원 안 됨 | `componentN()` 자동 생성 |
| 대상 | 없음 | `data class`, `Pair`, `Triple` 등 |
| 커스터마이징 | 불가 | `operator fun componentN()` 구현 가능 |

### 예시
```kotlin
data class User(val id: Long, val name: String)
val (id, name) = User(1, "Tom") // 구조 분해 = component1(), component2()
```