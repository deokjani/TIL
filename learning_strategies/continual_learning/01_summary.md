
# Continual Learning 전략 정리 (실무 중심)

## 1. Continual Learning이란?

Continual Learning은 모델이 순차적으로 학습되는 여러 Task 또는 데이터 흐름에 대해,  
기존에 학습한 지식을 잊지 않고 누적해서 학습하는 전략이다.

### 특징
- Catastrophic Forgetting 방지가 핵심
- 전체 데이터를 다시 학습할 수 없는 환경에서 유용
- 머신러닝과 딥러닝 모두에 적용 가능

---

## 2. 모델별 적용 가능성

| 모델 유형 | 적용 가능 여부 | 비고 |
|-----------|----------------|------|
| 머신러닝 (SVM, XGBoost 등) | Rehearsal 중심 | 일부 과거 데이터를 저장해 같이 학습 |
| 딥러닝 (CNN, BERT 등) | Rehearsal, EWC, Expansion | 다양한 전략 사용 가능 |
| 강화학습 (DQN 등) | Experience Replay | Rehearsal의 변형 개념 사용 |

---

## 3. 주요 전략 비교

| 전략 | 실무 사용도 | 이유 |
|------|--------------|------|
| Rehearsal | 가장 많이 사용 | 간단하고 성능도 우수 |
| EWC | 일부 사용 | 계산 복잡도 높음, 연구 중심 |
| Expansion | 거의 사용되지 않음 | 모델 크기 증가, 실무 부적합 |
| Distillation | 일부 사용 | 기존 모델 지식을 경량화 모델에 전이 |
| Prompt 기반 | 일부 사용 | 최신 LLM 위주 연구, 실무 확산 중 |

---

## 4. Rehearsal 예시

```python
# 이전 Task에서 일부 샘플 저장
memory_X, memory_y = [], []
for x, y in task_A_data:
    model.train(x, y)
    if random.random() < 0.05:
        memory_X.append(x)
        memory_y.append(y)

# 새로운 Task에서 과거 데이터와 함께 재학습
X_combined = task_B_X + memory_X
y_combined = task_B_y + memory_y
model.fit(X_combined, y_combined)
```

---

## 5. 왜 Rehearsal이 가장 많이 쓰이는가?

| 이유 | 설명 |
|------|------|
| 구현 단순 | 과거 데이터를 일부 저장하여 반복 학습 |
| 효과 확실 | forgetting 방지에 직접적 효과 |
| 범용 적용 | 모든 모델 유형에 적용 가능 |

---

## 6. 기타 전략 요약

### EWC (Elastic Weight Consolidation)
- 중요한 파라미터는 바뀌지 않도록 손실 함수에 제약 부여
- Fisher Information 계산 필요 → 계산 복잡도 높음

### Expansion (ProgressiveNet 등)
- Task마다 Layer를 확장 → 모델 크기 증가
- 연구용에서는 활발, 실무에서는 메모리 문제로 거의 사용되지 않음

### Distillation
- 이전 모델 지식을 작은 모델로 압축하여 전달
- 단일 Task 유지에는 효과적

---

## 7. 한 줄 요약

Rehearsal은 가장 실용적이고 효과적인 Continual Learning 전략이며,  
머신러닝과 딥러닝을 가리지 않고 대부분의 환경에서 안정적으로 사용 가능하다.
