
# 머신러닝 학습 방식 정리

머신러닝의 학습 방식은 크게 5가지로 구분할 수 있으며, 각각의 방식은 데이터의 형태와 문제의 성격에 따라 활용된다.

---

## 1. 지도 학습 (Supervised Learning)

**정의**: 입력 데이터(X)와 정답(Y)이 함께 주어지는 학습 방식.  
모델이 입력에 대응하는 출력을 예측하도록 학습한다.

**대표 알고리즘 및 간단 설명**:
- **선형 회귀**: 연속적인 수치를 예측. 예) 아파트 가격 예측
- **로지스틱 회귀**: 확률 기반 이진 분류. 예) 이메일 스팸 여부
- **KNN**: 가장 가까운 이웃의 클래스를 따라가는 분류법
- **결정 트리**: 조건을 따라 데이터를 나누는 방식
- **랜덤 포레스트**: 여러 트리를 평균내는 앙상블 방법
- **SVM**: 클래스 간의 최적 분류 경계를 찾는 방법
- **Gradient Boosting**: 오차를 줄여가며 트리를 순차적으로 학습

**사용 예시**:
- 이메일 스팸 분류
- 아파트 가격 예측
- 고객 이탈 예측
- 수요 예측

---

## 2. 비지도 학습 (Unsupervised Learning)

**정의**: 정답이 없는 데이터에서 데이터의 패턴, 구조, 분포 등을 학습하는 방식.

**대표 알고리즘 및 간단 설명**:
- **K-Means**: 데이터를 K개의 그룹으로 나눔
- **DBSCAN**: 밀도 기반의 클러스터링
- **PCA**: 고차원 데이터를 주요 구성 요소로 차원 축소
- **t-SNE**: 데이터 시각화를 위한 비선형 차원 축소

**사용 예시**:
- 고객 세분화
- 문서 주제 분류
- 이상 거래 탐지
- 데이터 시각화

---

## 3. 강화 학습 (Reinforcement Learning)

**정의**: 환경과 상호작용하며, 보상(reward)을 최대화하는 방향으로 학습.

**대표 알고리즘 및 간단 설명**:
- **Q-learning**: 상태-행동 값을 학습하여 최적 정책을 결정
- **DQN**: Q-learning을 딥러닝으로 확장
- **PPO, A3C**: 복잡한 환경에서 안정적으로 학습하는 정책 최적화 방법

**사용 예시**:
- 자율 주행
- 게임 AI (알파고 등)
- 로봇 제어
- 투자 전략 수립

---

## 4. 준지도 학습 (Semi-Supervised Learning)

**정의**: 대부분 비라벨 데이터에 소수의 라벨 데이터를 활용하여 학습.

**대표 알고리즘 및 간단 설명**:
- **Pseudo-Labeling**: 모델이 생성한 가짜 라벨로 학습
- **Label Propagation**: 라벨이 있는 데이터로부터 이웃에 라벨 전파
- **Graph-based 모델**: 그래프 구조에서 이웃 관계를 활용한 분류

**사용 예시**:
- 의료 영상 진단
- 음성 인식
- 라벨 비용이 높은 상황

---

## 5. 자기 지도 학습 (Self-Supervised Learning)

**정의**: 데이터의 일부분을 예측하게 하여 스스로 학습하는 방식.

**대표 알고리즘 및 간단 설명**:
- **BERT**: 마스킹된 단어 예측
- **GPT**: 다음 단어 예측
- **SimCLR, MoCo**: 이미지 표현 학습
- **CLIP**: 이미지-텍스트 동시 학습

**사용 예시**:
- 자연어처리 사전학습
- 이미지 특징 추출
- 멀티모달 AI 학습

---

## 전체 요약 표

| 학습 방식             | 라벨 필요 여부 | 대표 알고리즘                           | 주 사용 분야                   |
|----------------------|----------------|----------------------------------------|-------------------------------|
| 지도 학습             | 필요           | 선형 회귀, 로지스틱, 트리, SVM, GBM    | 분류, 회귀, 예측              |
| 비지도 학습           | 불필요         | K-Means, PCA, DBSCAN                   | 군집화, 차원 축소, 이상 탐지  |
| 강화 학습             | 보상 기반      | Q-Learning, DQN, PPO                   | 게임, 로봇, 자율주행          |
| 준지도 학습           | 일부 라벨 필요 | Pseudo-Labeling, Label Propagation     | 의료, 음성, 대규모 라벨 부족 |
| 자기 지도 학습        | 자동 생성      | BERT, GPT, SimCLR, MoCo, CLIP          | NLP, 비전 모델 사전학습       |
