# 딥러닝 대표 신경망 구조 상세 정리

---

## 1. ANN (Artificial Neural Network) – 인공 신경망

### 구성
- 입력층 (Input Layer)
- 은닉층 (Hidden Layer) – 1개 또는 0개
- 출력층 (Output Layer)

### 작동 원리
- 입력값 * 가중치 → 합산 후 활성화 함수 통과 → 다음 층으로 전달

### 주로 사용하는 분야
- 정형 데이터 분류
- 예: 금융 데이터로 신용도 평가, 마케팅 데이터로 고객 이탈 예측

### 예시 코드
```python
from sklearn.neural_network import MLPClassifier
model = MLPClassifier(hidden_layer_sizes=(10,), activation='relu')
```

### 한계
- 층이 얕아 복잡한 패턴 인식에 한계
- 비정형 데이터(이미지, 음성 등)에 적합하지 않음

---

## 2. DNN (Deep Neural Network) – 심층 신경망

### 구성
- ANN 구조에 은닉층을 여러 개 추가
- 비선형 활성화 함수 반복으로 복잡한 함수 근사 가능

### 사용 분야
- 텍스트 분류, 이미지 분류, 예측 분석 등 일반적 비정형 데이터 처리
- 예: 영화 리뷰 감성 분석, 보험사기 탐지, 추천 시스템

### 예시 코드
```python
import tensorflow as tf
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
```

### 한계
- 많은 층 → 과적합, 연산량 증가
- 특화된 구조(CNN, RNN 등)에 비해 효율이 떨어질 수 있음

---

## 3. CNN (Convolutional Neural Network) – 합성곱 신경망

### 구성
- 합성곱 계층 (Convolution Layer)
- 풀링 계층 (Pooling Layer)
- 완전 연결 계층 (Fully Connected Layer)

### 사용 분야
- 이미지 분류, 얼굴 인식, 자율 주행 비전 처리
- 예: 고양이 vs 강아지 분류, CCTV 사람 탐지

### 예시 코드
```python
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(64, 64, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])
```

### 장점
- 이미지의 위치 불변 특징 학습에 뛰어남
- 적은 파라미터로 복잡한 이미지도 처리

---

## 4. RNN (Recurrent Neural Network) – 순환 신경망

### 구성
- 순환 구조: 자기 자신에게 연결되는 노드
- 이전 시간의 출력값을 현재 계산에 반영

### 사용 분야
- 자연어 처리 (NLP), 시계열 예측, 음성 인식
- 예: 날씨 예측, 문장 생성, 주식 가격 예측

### 예시 코드
```python
model = tf.keras.Sequential([
    tf.keras.layers.SimpleRNN(50, activation='tanh', input_shape=(10, 1)),
    tf.keras.layers.Dense(1)
])
```

### 한계
- 장기 의존성 문제 → LSTM, GRU로 해결

---

## 5. AE (AutoEncoder) – 오토인코더

### 구성
- 인코더 (Encoder): 입력 → 잠재 벡터
- 디코더 (Decoder): 잠재 벡터 → 복원된 출력

### 사용 분야
- 차원 축소, 이상 탐지, 보이스 변조, 노이즈 제거
- 예: CCTV 비정상 행동 탐지, 음성에서 배경 노이즈 제거, 목소리 변조

---

## 6. GAN (Generative Adversarial Network) – 생성적 적대 신경망

### 구성
- Generator: 가짜 데이터 생성
- Discriminator: 진짜/가짜 판별
- 서로 경쟁하면서 학습

### 사용 분야
- 딥페이크, 이미지 생성, 스타일 변환, 데이터 보강
- 예: 실제 사람 같은 얼굴 생성, 낮을 밤 이미지로 전환

---

## 7. U-NET

### 구성
- CNN 기반의 인코더-디코더 구조 + Skip Connection
- U자형 구조로 고해상도 특징 보존

### 사용 분야
- 이미지 분할, 특히 의료 영상에서 높은 정확도
- 예: CT/MRI 이미지에서 장기 분할, 위성사진에서 도로 검출

### 구조 설명
- 왼쪽: 다운샘플링 (Convolution + MaxPooling)
- 오른쪽: 업샘플링 (Transpose Conv) + 이전 층 연결


## 요약 표

| 구조         | 주요 데이터     | 대표 알고리즘/모델            | 주요 사용 예시                     |
|--------------|----------------|-------------------------------|------------------------------------|
| MLP (ANN)    | 정형 데이터     | Dense Layer 기반 ANN          | 수요 예측, 고객 분류               |
| DNN          | 정형/비정형    | Relu, Dropout, BatchNorm       | 사기 탐지, 사용자 예측             |
| CNN          | 이미지          | Conv2D, ResNet, EfficientNet   | 이미지 분류, 의료 영상, 얼굴 인식 |
| RNN / LSTM   | 시계열/텍스트  | LSTM, GRU                      | 감정 분석, 기상 예측, 번역         |
| AE           | 이미지/음성    | AutoEncoder, VQ-VAE            | 이상 탐지, 보이스 변조             |
| GAN          | 이미지          | StyleGAN, CycleGAN             | 이미지 생성, 딥페이크              |
| U-NET        | 이미지 (픽셀 단위) | U-Net, Attention U-Net         | 의료/위성 영상 분할                |
