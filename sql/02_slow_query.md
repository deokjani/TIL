# 슬로우 쿼리 원인과 해결 방법 정리 (개선 예시 포함)

---

## 1. 슬로우 쿼리란?

**슬로우 쿼리(Slow Query)**는 실행 시간이 비정상적으로 오래 걸리는 SQL 문으로, 대용량 데이터 처리나 비효율적인 쿼리 설계로 인해 발생한다.

---

## 2. 슬로우 쿼리 주요 원인 및 개선 예시

| 원인 | 설명 | 문제 예시 | 개선 방법 |
|------|------|-----------|------------|
| 인덱스 미사용 | 테이블 전체 스캔 발생 | `SELECT * FROM orders WHERE customer_email = 'abc@naver.com';` | `CREATE INDEX idx_customer_email ON orders(customer_email);` |
| 잘못된 JOIN 순서 | 큰 테이블 먼저 JOIN → 연산량 폭증 | 고객 필터 없이 주문 먼저 JOIN | 서브쿼리 또는 WITH절로 필터링 먼저 수행 |
| 불필요한 정렬, 그룹화 | 정렬/그룹화는 리소스를 많이 씀 | `SELECT * FROM orders ORDER BY created_at;` | 필요한 컬럼만 정렬, 정렬 제거 또는 인덱스 활용 |
| 함수 사용 | 인덱스가 무효화됨 | `WHERE DATE(order_date) = '2024-01-01'` | `order_date BETWEEN '2024-01-01 00:00:00' AND '2024-01-01 23:59:59'` |
| LIKE '%값%' | 앞에 % 있으면 인덱스 사용 불가 | `WHERE name LIKE '%kim%'` | `LIKE 'kim%'` 또는 Full Text Index 사용 |
| SELECT * | 불필요한 데이터까지 다 조회 | `SELECT * FROM orders` | `SELECT order_id, payment_amount FROM orders` |
| 서브쿼리 중첩 | 반복 실행으로 성능 저하 | `WHERE id IN (SELECT id FROM ...)` | JOIN으로 변경하거나 EXISTS 사용 |
| 필터링 누락 | 조인 전에 조건 필터 안 하면 느림 | 조인 후 WHERE 조건 사용 | 조인 전에 WHERE 조건으로 필터링 |
| 통계정보 부족 | 실행계획 비효율 | `ANALYZE` 안 된 상태 | `ANALYZE TABLE orders;` 실행으로 통계 갱신 |
| 파티션 무시 | WHERE절에 파티션 키가 없음 | `SELECT * FROM logs` (파티션 조건 없음) | `WHERE log_date = '2024-04-01'` 처럼 파티션 키 포함 |

---

## 3. 예시 개선 코드

### 1. 함수 무효화 개선
```sql
-- Before
SELECT * FROM orders WHERE DATE(order_date) = '2024-01-01';

-- After
SELECT * FROM orders
WHERE order_date BETWEEN '2024-01-01 00:00:00' AND '2024-01-01 23:59:59';
```

### 2. 인덱스 없는 WHERE절
```sql
-- Before
SELECT * FROM orders WHERE customer_email = 'abc@naver.com';

-- After
CREATE INDEX idx_email ON orders(customer_email);
SELECT * FROM orders WHERE customer_email = 'abc@naver.com';
```

### 3. 서브쿼리 중첩
```sql
-- Before
SELECT * FROM products
WHERE id IN (SELECT product_id FROM order_items);

-- After
SELECT DISTINCT p.*
FROM products p
JOIN order_items oi ON p.id = oi.product_id;
```

### 4. LIKE 패턴 개선
```sql
-- Before
SELECT * FROM customers WHERE name LIKE '%kim%';

-- After
SELECT * FROM customers WHERE name LIKE 'kim%';
-- 또는
-- Full Text Index 사용
```

### 5. 잘못된 조인 순서
```sql
-- Before
SELECT * FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE c.email = 'a@b.com';

-- After
SELECT * FROM (
  SELECT * FROM customers WHERE email = 'a@b.com'
) c
JOIN orders o ON o.customer_id = c.customer_id;
```

---

## 4. 슬로우 쿼리 분석 도구

| 도구 | 설명 |
|------|------|
| EXPLAIN / EXPLAIN ANALYZE | 실행 계획 분석 |
| SHOW INDEX | 인덱스 정보 확인 |
| Slow Query Log | MySQL 슬로우 쿼리 로그 기록 |
| pg_stat_statements | PostgreSQL에서 쿼리 통계 확인 |
| Spark UI / Presto UI | 대용량 분석 쿼리 시 단계별 성능 분석 |

---

## 5. 실무 튜닝 팁

- 쿼리 작성 후 항상 `EXPLAIN` 분석 수행
- SELECT 시 꼭 필요한 컬럼만 지정
- WHERE 절에서 인덱스 활용 여부 검토
- 조인 전에 가능한 조건으로 필터링
- 파티션 테이블은 반드시 파티션 키를 활용한 조건 사용