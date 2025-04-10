
# Spring Batch 정리: 주요 개념 + 확장 기능 + 예시 흐름

---

## 1. POJO 클래스는 왜 사용하는가?

**설명:**  
CSV 한 줄을 자바 객체로 매핑하기 위해 POJO(Plain Old Java Object) 클래스를 사용하는 것이다.  
예를 들어, CSV가 다음과 같다면:

```
1,John,john@example.com
```

이 한 줄을 아래처럼 자바 객체로 변환할 수 있다:

```java
public class Customer {
    private Long id;
    private String name;
    private String email;
}
```

`Customer`는 단순한 데이터 컨테이너일 뿐이며, 클래스 이름은 자유롭게 지정할 수 있다.  
중요한 건 **CSV 필드 순서와 클래스 필드가 일치해야** 자동 매핑이 가능하다는 점이다.  
즉, 꼭 `Customer`라는 이름일 필요는 없고, CSV에 맞는 POJO 클래스를 정의하면 된다.

---

## 2. Job과 Step 구조, chunk()의 의미

**Job이란:**  
하나 이상의 Step으로 구성되는 단위 작업이다.

**Step이란:**  
데이터를 처리하는 단위로, 내부적으로 Reader → Processor → Writer 구조로 구성된다.

```java
Job job = jobBuilderFactory.get("myJob")
    .start(step1())
    .next(step2())
    .build();
```

### chunk()

```java
.stepBuilderFactory.get("step1")
    .<Customer, Customer>chunk(100)
```

- chunk 단위로 데이터를 읽고, 처리하고, 한번에 commit 한다.
- chunk(100)은 100개 처리 후 한 번에 commit 하겠다는 의미.
- 일반적으로 `100~1000` 사이 값 사용.

**기준:**
- 데이터가 크면 chunk 작게
- 처리 속도와 안정성 균형 필요

---

## 3. ItemProcessor 제네릭 타입 의미

```java
ItemProcessor<Customer, Customer>
```

- 앞은 입력 타입: Reader가 넘긴 객체
- 뒤는 출력 타입: Processor가 가공 후 Writer에 넘길 객체

**예:**
- `ItemProcessor<Customer, User>`: Customer를 User 객체로 변환
- `ItemProcessor<Customer, Customer>`: Customer 객체 그대로 가공 또는 필터링

---

## 4. 예외 처리 (SkipPolicy)

예외 발생 시 Job을 실패시키지 않고, 특정 예외는 건너뛰도록 처리

```java
.faultTolerant()
.skip(ValidationException.class)
.skipLimit(10)
```

- 최대 10번까지 건너뛰고 계속 실행
- `null` 반환 시 Writer로 전달되지 않음

---

## 5. JobParameters 사용 이유

```java
JobParameters params = new JobParametersBuilder()
    .addLong("time", System.currentTimeMillis())
    .toJobParameters();
```

- Spring Batch는 같은 Job을 중복 실행 못하게 막음
- 매 실행마다 고유한 JobParameters를 전달해야 실행됨
- 보통 현재 시간, 사용자 ID, 파일명 등을 넣음

---

## 6. Listener 정리 (JobExecutionListener vs StepExecutionListener)

| 종류 | 설명 | 사용 시점 |
|------|------|-----------|
| JobExecutionListener | Job 전체 전/후 훅 | 로그, 소요 시간 측정 |
| StepExecutionListener | Step 단위 전/후 훅 | 전처리/후처리, 리소스 초기화 등 |

```java
public class MyJobListener implements JobExecutionListener {
    public void beforeJob(JobExecution jobExecution) {
        System.out.println("Job 시작");
    }
    public void afterJob(JobExecution jobExecution) {
        System.out.println("Job 종료");
    }
}
```

```java
public class MyStepListener implements StepExecutionListener {
    public void beforeStep(StepExecution stepExecution) {
        System.out.println("Step 시작");
    }
    public ExitStatus afterStep(StepExecution stepExecution) {
        System.out.println("Step 종료");
        return ExitStatus.COMPLETED;
    }
}
```

---

## 7. 병렬 처리 (TaskExecutor 사용)

```java
@Bean
public TaskExecutor taskExecutor() {
    SimpleAsyncTaskExecutor executor = new SimpleAsyncTaskExecutor("batch_task");
    executor.setConcurrencyLimit(4);
    return executor;
}

@Bean
public Step parallelStep() {
    return stepBuilderFactory.get("parallelStep")
        .<Customer, Customer>chunk(10)
        .reader(reader())
        .processor(processor())
        .writer(writer())
        .taskExecutor(taskExecutor())
        .throttleLimit(4)
        .build();
}
```

---

## 8. CSV → Excel 변환 (POI 사용)

```java
@Bean
public ItemWriter<Customer> excelWriter() {
    return items -> {
        Workbook workbook = new XSSFWorkbook();
        Sheet sheet = workbook.createSheet("Customers");
        int rowNum = 0;

        for (Customer customer : items) {
            Row row = sheet.createRow(rowNum++);
            row.createCell(0).setCellValue(customer.getId());
            row.createCell(1).setCellValue(customer.getName());
            row.createCell(2).setCellValue(customer.getEmail());
        }

        try (FileOutputStream fileOut = new FileOutputStream("customers.xlsx")) {
            workbook.write(fileOut);
        }
        workbook.close();
    };
}
```

---

## 9. DB → CSV 저장

```java
@Bean
public JdbcCursorItemReader<Customer> dbReader(DataSource dataSource) {
    JdbcCursorItemReader<Customer> reader = new JdbcCursorItemReader<>();
    reader.setDataSource(dataSource);
    reader.setSql("SELECT id, name, email FROM customer");
    reader.setRowMapper(new BeanPropertyRowMapper<>(Customer.class));
    return reader;
}

@Bean
public FlatFileItemWriter<Customer> csvWriter() {
    return new FlatFileItemWriterBuilder<Customer>()
        .name("customerCsvWriter")
        .resource(new FileSystemResource("output/customers.csv"))
        .delimited()
        .names(new String[]{"id", "name", "email"})
        .build();
}
```

---

## 10. 전체 흐름 요약

1. CSV 파일 → Reader → Processor → Writer(DB 저장)
2. DB → Reader → Writer(CSV 저장)
3. 병렬 처리로 속도 개선
4. 예외 발생 시 건너뛰기 (SkipPolicy)
5. Excel 파일로 변환 가능 (POI 기반 커스텀 Writer)
6. Job과 Step 단위로 전/후 처리 Listener 설정
