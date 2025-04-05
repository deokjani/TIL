
# 📘 Kubernetes with Minikube - 기초 개념 정리 (WSL2 + Docker)

> Kubernetes 클러스터를 Minikube로 로컬에 구축하고,  
> Docker 기반 컨테이너를 Kubernetes로 올리기 위한 기본 구조, 개념, 명령어 정리

---

## 🔧 1. 환경 구성

- OS: Windows 10/11
- Backend: WSL2 + Docker Desktop
- K8s 실행: Minikube

```bash
# Minikube 클러스터 시작 (Docker 드라이버 사용)
minikube start --driver=docker

# 클러스터 상태 확인
minikube status

# 기본 대시보드 실행
minikube dashboard
```

---

## 📦 2. Nginx 앱 배포 실습

```bash
# 1) Nginx 앱 배포 (Deployment 생성)
kubectl create deployment my-nginx --image=nginx

# 2) NodePort로 서비스 외부 노출
kubectl expose deployment my-nginx --type=NodePort --port=80

# 3) 자동 브라우저 실행 (IP + 포트 출력)
minikube service my-nginx

# 또는 localhost 접속용 수동 포트 포워딩
kubectl port-forward service/my-nginx 8080:80
```

👉 `http://localhost:8080` 으로 브라우저에서 접근 가능

---

## 🔍 3. 핵심 구조 이해

```plaintext
🧠 Cluster (클러스터)
 └── 📦 Namespace (서비스/팀 간 논리적 격리)
      └── 📥 Deployment (Pod을 배포하고 버전 관리)
           └── 🧱 Pod (실행 단위, 여러 컨테이너 포함 가능)
                └── 🧩 Container (실제 앱 실행: ex. nginx, python)
```

| 계층 | 역할 | 예시 |
|------|------|------|
| **Container** | 실제 앱 | `nginx`, `fluentd`, `redis` |
| **Pod** | 연관된 컨테이너 묶음 | nginx + log-agent sidecar |
| **Deployment** | Pod 템플릿 + 버전 + 스케일 관리 | v1.2.0 → v1.3.0 롤링 |
| **Namespace** | 서비스/팀 간 격리 | team-a, dev, prod |
| **Cluster** | 전체 Kubernetes 환경 | dev 클러스터, prod 클러스터 |

---

## 🎯 Kubernetes vs Airflow 개념 비교

| Airflow | Kubernetes | 설명 |
|---------|------------|------|
| DAG | Deployment / Job | 전체 흐름 |
| Task | Pod | 실행 단위 |
| TaskInstance | Pod Instance | 실 실행 단위 |
| Executor | Kubelet | Task 실행자 |
| Scheduler | K8s Scheduler | 할당자 |

---

## 🛠️ 자주 쓰는 명령어 요약

```bash
# 클러스터 상태 확인
kubectl get nodes
kubectl get pods -A

# 로그 보기
kubectl logs <pod-name>

# 리소스 설명
kubectl describe pod <pod-name>

# 포트포워딩
kubectl port-forward service/<svc-name> 8080:80

# 애드온 리스트
minikube addons list
```

---

## ⚠️ 기타 팁

- `minikube stop`: 클러스터 일시 정지  
- `minikube delete`: 클러스터 완전 삭제  
- `kubectl config use-context`: 여러 클러스터 전환 시 사용  
- `docker ps`: Minikube의 K8s 컨테이너들도 Docker 위에 뜸

---

## 📌 요약

> Kubernetes는 앱 실행을 **컨테이너 → Pod → Deployment → Namespace → Cluster**  
> 순으로 묶고 관리하며,  
> Minikube는 로컬에서 이를 실습할 수 있게 해주는 가상 클러스터 도구다.
