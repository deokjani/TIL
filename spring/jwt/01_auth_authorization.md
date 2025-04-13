
# JWT 기반 인증(Authentication) vs 인가(Authorization) 정리

## 1. 개념 구분

| 구분 | 인증 (Authentication) | 인가 (Authorization) |
|------|------------------------|------------------------|
| 의미 | 사용자가 누구인지 확인 | 사용자가 요청한 리소스를 사용할 권한이 있는지 확인 |
| 핵심 질문 | "너 누구야?" | "이거 할 수 있어?" |
| 기반 정보 | ID, 비밀번호 → JWT 발급 | JWT 내부의 Role, 권한 정보 |
| 검증 방식 | 로그인 후 JWT 생성 | JWT Payload에서 Role 확인 |
| 결과 | 사용자 확인 완료 → 토큰 발급 | 권한 확인 → 접근 허용 or 거부 |

---

## 2. JWT 인증 흐름 정리

### 1단계. 로그인 요청

```http
POST /login
Content-Type: application/json

{
  "username": "user",
  "password": "pass"
}
```

### 2단계. 비밀번호 확인 및 인증 처리

```java
Authentication auth = authenticationManager.authenticate(
    new UsernamePasswordAuthenticationToken(username, password)
);
```

### 3단계. 인증 성공 → JWT 발급

```java
String token = jwtUtil.generateToken(auth);
return ResponseEntity.ok(new JwtResponse(token));
```

### 4단계. 클라이언트가 토큰 저장
- 로컬 스토리지 또는 쿠키 등 클라이언트 측에 저장

### 5단계. 요청 시 토큰 포함

```http
GET /api/profile
Authorization: Bearer <JWT-Token>
```

### 6단계. 서버는 필터에서 토큰 검증 및 인증 처리

```java
if (token != null && jwtUtil.validateToken(token)) {
    String username = jwtUtil.getUsernameFromToken(token);
    UserDetails userDetails = userDetailsService.loadUserByUsername(username);
    Authentication auth = new UsernamePasswordAuthenticationToken(userDetails, null, userDetails.getAuthorities());
    SecurityContextHolder.getContext().setAuthentication(auth);
}
```

---

## 3. JWT 구조

```
xxxxx.yyyyy.zzzzz
```

| 구성 요소 | 설명 |
|-----------|------|
| Header | 토큰 타입과 해싱 알고리즘 (예: HS256) |
| Payload | 사용자 정보 및 claims (username, roles 등) |
| Signature | 비밀 키로 서명된 값 (변조 방지용) |

---

## 4. JWT + Refresh Token 구조

| 항목 | 설명 |
|------|------|
| Access Token | 유효기간 짧음 (15분 내외), 요청 인증에 사용 |
| Refresh Token | 유효기간 길음 (일주일 이상), 새 Access Token 발급에 사용 |

### 리프레시 토큰 사용 흐름

1. 로그인 시 Access + Refresh Token 모두 발급
2. Access Token이 만료되면 클라이언트가 Refresh Token으로 재요청
3. 서버는 Refresh Token을 DB에서 확인 후 Access Token 재발급

---

## 5. JWT와 관리자 권한 (Authorization)

- JWT는 로그인 인증 수단 (누구인가 확인)
- 관리자 권한 확인은 별도의 인가 과정이 필요
- JWT Payload에 Role을 포함해야 함

### 예시 JWT Payload

```json
{
  "sub": "adminUser",
  "role": "ROLE_ADMIN",
  "exp": 1712767890
}
```

### 서버 측 권한 확인 예시 (Spring)

```java
@PreAuthorize("hasRole('ADMIN')")
@GetMapping("/admin")
public ResponseEntity<?> adminOnly() {
    ...
}
```

---

## 6. 요약

- 인증(Authentication): 사용자가 로그인했는지 확인 (JWT 발급)
- 인가(Authorization): 해당 사용자가 특정 리소스에 접근 가능한지 확인 (role 포함)
- JWT는 인증 수단, 권한은 별도로 관리해야 안전
