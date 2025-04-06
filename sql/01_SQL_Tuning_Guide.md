
# 실무 중심 SQL 성능 최적화 전략 정리

이 문서는 실무에서 자주 사용되는 SQL 성능 튜닝 기법을 체계적으로 정리한 문서입니다.  
쿼리 작성 및 데이터베이스 설계 시 고려해야 할 다양한 튜닝 요소들을 예제와 함께 설명합니다.

---

## 1. 서브쿼리 vs 조인 최적화

### EXISTS vs IN
```sql
-- EXISTS 사용 예 (추천: 서브쿼리 대상 테이블이 클 경우 성능 우수)
SELECT *
FROM KPI_DATA kd
WHERE EXISTS (
    SELECT 1
    FROM DEPT d
    WHERE d.DEPT_ID = kd.DEPT_ID
      AND d.STATUS = 'ACTIVE'
);

-- IN 사용 예 (대상 테이블이 작을 경우 유리)
SELECT *
FROM KPI_DATA
WHERE DEPT_ID IN (
    SELECT DEPT_ID
    FROM DEPT
    WHERE STATUS = 'ACTIVE'
);
```
> `EXISTS`는 조건을 만족하는 첫 행이 발견되면 바로 True를 반환하므로, **불필요한 반복 스캔 없이 빠르게 종료**됨.  
> 반면 `IN`은 **전체 결과를 메모리에 로딩한 후 비교**하므로 대상이 많을 경우 상대적으로 느림.

---

## 2. 불필요한 함수 제거

```sql
-- 비추 예: 컬럼에 함수 적용 시 인덱스 미사용
SELECT * FROM USERS
WHERE TO_CHAR(REG_DATE, 'YYYY-MM') = '2024-01';

-- 추천 예
SELECT * FROM USERS
WHERE REG_DATE >= TO_DATE('2024-01-01', 'YYYY-MM-DD')
  AND REG_DATE < TO_DATE('2024-02-01', 'YYYY-MM-DD');
```

---

## 3. LIKE 연산자 최적화

```sql
-- 비추: 와일드카드가 앞에 있으면 인덱스 사용 불가
WHERE name LIKE '%철수'

-- 추천
WHERE name LIKE '김%'
```

---

## 4. 인덱스 최적화 전략 (LOCAL / FUNCTION BASED)

- 파티셔닝 테이블에는 LOCAL INDEX 권장
```sql
CREATE INDEX IDX_KPI_DATE ON KPI_DATA (KPI_DATE) LOCAL;
```

- 조건 연산 시 FUNCTION-BASED INDEX로 튜닝
```sql
CREATE INDEX IDX_UPPER_DEPT ON DEPT (UPPER(DEPT_NM));
```

- 복합 인덱스 사용 주의
  - WHERE a = ? AND b = ? → (a, b) 인덱스 유리
  - WHERE b = ?만 자주 쓰면 b 단독 인덱스 고려

---

## 5. RANGE 파티셔닝 전략

```sql
CREATE TABLE KPI_DATA (
    KPI_ID       VARCHAR2(20),
    KPI_DATE     DATE,
    KPI_VALUE    NUMBER,
    DEPT_ID      VARCHAR2(10)
)
PARTITION BY RANGE (KPI_DATE) (
    PARTITION p202401 VALUES LESS THAN (TO_DATE('2024-02-01','YYYY-MM-DD')),
    PARTITION p202402 VALUES LESS THAN (TO_DATE('2024-03-01','YYYY-MM-DD')),
    PARTITION p_max   VALUES LESS THAN (MAXVALUE)
);
```

### 파티션 프루닝 적용 쿼리 예시
```sql
SELECT KPI_ID, KPI_VALUE
FROM KPI_DATA
WHERE KPI_DATE BETWEEN TO_DATE('2024-01-01','YYYY-MM-DD') AND TO_DATE('2024-01-31','YYYY-MM-DD');
```

---

## 6. MyBatis 동적 SQL 최적화

MyBatis에서는 `<if>`, `<choose>`, `<when>`, `<otherwise>` 등의 태그를 활용하여 **동적으로 SQL 조건을 제어**할 수 있습니다.  
조건에 따라 쿼리 내 WHERE 절을 유연하게 조합하므로, **불필요한 조건문 실행을 방지하고 실행 계획을 간결하게 유지**할 수 있어 성능 향상에 도움을 줍니다.

### CDATA + choose/when 방식 예시
```xml
<![CDATA[
SELECT *
FROM KPI_DATA
WHERE 1 = 1
<choose>
    <when test="status != null">
        AND STATUS = #{status}
    </when>
    <when test="deptId != null">
        AND DEPT_ID = #{deptId}
    </when>
    <otherwise>
        AND STATUS = 'ACTIVE'
    </otherwise>
</choose>
]]>
```

---

## 7. 기타 튜닝 전략 요약

- `SELECT *` → 필요한 컬럼만 명시  
  → 불필요한 데이터 전송 및 I/O 감소, 실행 계획 단순화

- `DISTINCT`, `GROUP BY` 최소화  
  → 정렬(SORT) 비용이 크고, 인덱스 활용이 어려워 성능 저하 유발

- `COUNT` 연산 줄이고 `EXISTS` 대체 고려  
  → 단순 존재 여부 확인 시 `COUNT(*)`는 전체 스캔이 발생하지만, `EXISTS`는 조건 만족 시 즉시 종료

- `OR` 조건 → `UNION ALL` 또는 별도 쿼리 분리  
  → `OR` 조건은 옵티마이저가 인덱스 사용을 포기하고 Full Scan을 선택할 수 있음.  
    `UNION ALL`로 쿼리를 분리하면 각각의 조건에 맞는 인덱스를 활용 가능

---

## 8. 실행 계획 및 분석 도구 정리

| 도구          | 주요 목적                     | 특징 |
|---------------|-------------------------------|------|
| EXPLAIN PLAN  | 실행 계획 미리보기            | 인덱스 사용 여부, COST 확인 |
| AUTOTRACE     | 실행 결과 + 통계 자동 출력    | 블록 I/O, Consistent Gets 등 확인 |
| TKPROF        | 트레이스 파일 분석 도구       | 상세 실행 순서 및 병목 구간 분석 |
| GUI 툴        | 시각적 쿼리 분석              | SQL Developer, TOAD, DataGrip 등 활용 가능 |

### Autotrace 등에서 보는 I/O 지표 해석
```text
3  recursive calls
2  db block gets
10 consistent gets
1  rows processed
```

| 항목 | 설명 |
|------|------|
| `recursive calls` | Oracle 내부적으로 수행하는 쿼리 수 (예: 통계 수집, 뷰 해석 등) |
| `db block gets` | 데이터 블록을 **버퍼 캐시에서 직접 읽은 횟수** |
| `consistent gets` | Undo 영역 포함, **일관성 있는 읽기**를 위한 블록 접근 수 |
| `rows processed` | 실제로 처리된 결과 행 수 |

### EXPLAIN PLAN 실행 예
```text
ID  Operation                         Object Name       Rows  Cost
0   SELECT STATEMENT
1   TABLE ACCESS BY INDEX ROWID      KPI_DATA          1     10
2   INDEX RANGE SCAN                 IDX_KPI_ID        5
```
> 하단부터 위로 실행되며, 인덱스를 통해 조회되었는지 확인 가능

---

## 9. 성능 개선 사례 요약 (Before → After)

| 항목             | 튜닝 전                          | 튜닝 후                          |
|------------------|----------------------------------|----------------------------------|
| 조회 쿼리 복잡도 | 다중 JOIN, 조건문 혼합           | EXISTS 활용 및 조건 분리로 간결화 |
| 데이터 범위 분리 | 단일 테이블 full scan            | RANGE 파티셔닝 + 프루닝 적용     |
| 인덱스 활용률    | 불완전 인덱스 사용               | LOCAL + FUNCTION-BASED 인덱스    |
