
# Spark JDBC 성능 최적화 및 대용량 데이터 비교 전략 정리

## 1. Spark JDBC 성능 최적화 구성

### 1.1 핵심 옵션 설명

| 옵션 | 설명 |
|------|------|
| `--num-executors` / `spark.executor.instances` | Spark Executor 수, 병렬 처리 리소스 |
| `.option("numPartitions")` | JDBC 병렬 쿼리 수, 동시에 생성되는 DB 연결 수 |
| `.option("partitionColumn")` | 데이터를 나눌 기준 컬럼, 숫자형이며 고르게 분포된 컬럼이 적합 |
| `.option("lowerBound")` / `.option("upperBound")` | partitionColumn의 범위, Spark가 병렬 쿼리를 날리기 위해 필요 |
| `.option("pushDownPredicate")` | 필터 조건을 DB로 미리 넘길지 여부 (기본 true) |

### 1.2 병목 및 DB 부하 방지 전략

| 전략 | 설명 |
|-------|------|
| Read-only 계정 사용 | SELECT 전용 계정으로 데이터 보호 |
| numPartitions 제한 | 동시 JDBC 연결 수 제한 (보통 4~8) |
| DB max_connections 확인 | DB가 처리 가능한 최대 커넥션 수 고려 |
| executor 수 조절 | Spark Executor 수 제한하여 과도한 병렬 연결 방지 |
| 타임아웃 설정 | `.option("queryTimeout", 300)` 등으로 timeout 제어 |

## 2. partitionColumn 선택 기준

| 조건 | 이유 |
|-------|------|
| 숫자형 컬럼 | 범위 나누기 쉬움 |
| 고르게 분포 | 파티션 간 작업 균형 유지 |
| NULL 없음 | 비어있는 파티션 방지 |
| 인덱스 존재 | DB가 범위 조건 빠르게 처리 가능 |

기본키(PK)는 보통 고르게 분포되어 있어 자주 선택됨.

## 3. 데이터 비교 전략

### 3.1 Spark DataFrame 비교 방식

```python
df1.subtract(df2)  # df1에만 있는 데이터
df1.intersect(df2)  # 공통된 데이터
df1.union(df2).dropDuplicates()  # 전체 병합 후 중복 제거
```

### 3.2 대용량 비교에서의 최적화 전략

| 전략 | 설명 |
|------|------|
| partitionColumn 기준 병렬 쿼리 | id 또는 timestamp 기준 분할 |
| 쿼리 범위 제한 | lowerBound / upperBound로 범위 지정 |
| 덤프 → S3 → Spark 처리 | JDBC 대신 Parquet 등으로 내보내기 후 처리 |
| 해시 비교 | MD5, SHA256 등으로 row-level hash 비교 |

## 4. 대체 전략: 파일 기반 처리

| 단계 | 설명 |
|------|------|
| DB Export | DB에서 CSV/Parquet로 덤프 |
| S3 업로드 | S3, HDFS 등으로 저장 |
| Spark 처리 | Spark로 Parquet/CSV 읽기 (성능 매우 빠름) |

## 5. JDBC Pushdown

Spark에서 filter, limit, join 등을 DB에 미리 넘겨서 처리하게 만드는 기능  
→ `.option("pushDownPredicate", "true")`

예시:
```python
df = spark.read.jdbc(...).filter("age > 30")  # 조건을 DB에 미리 적용
```

DB 부하가 크지 않다면 Pushdown을 활성화하면 전체 처리 속도 향상 가능.

---

## 참고

- Spark JDBC는 기본적으로 단일 쿼리 실행 → 병렬 분할 설정을 해주어야 성능 향상 가능
- 병렬성 조절은 Spark 리소스(executor)와 DB 커넥션 수(max_connections)를 함께 고려해야 함
