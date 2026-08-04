# Labsheet 06 — Kubernetes Fundamentals with Minikube

**Student Name:** M.H.L.Dilshan
**Student ID:** CIT-24-01-0488
**Module:** CCS3308 — Virtualization and Containers

## Summary
This lab deploys a multi-tier application (frontend, API, cache, database) on a local
Kubernetes cluster using Minikube, demonstrating Pods, Deployments, Services, scaling,
rolling updates/rollbacks, StatefulSets with PersistentVolumeClaims, and basic
observability/troubleshooting.

## Prerequisites
- Docker
- kubectl
- Minikube

## How to Run
```bash
minikube start --driver=docker
kubectl apply -f k8s/
kubectl get all
```

## Manifest Overview
| File | Purpose |
|---|---|
| pod-frontend.yaml | Single standalone frontend Pod (nginx:alpine) |
| deployment-frontend.yaml | Frontend Deployment, 3 replicas |
| service-frontend.yaml | NodePort Service exposing frontend |
| api-deployment.yaml | API Deployment (httpbin), 2 replicas |
| api-service.yaml | ClusterIP Service for API |
| cache-deployment.yaml | Redis cache Deployment, 1 replica |
| cache-service.yaml | ClusterIP Service for cache |
| postgres-statefulset.yaml | PostgreSQL StatefulSet with PVC (1Gi) |
| postgres-service.yaml | Headless Service for postgres |
| broken-pod.yaml | Deliberately broken pod for Part 9 troubleshooting demo |

## Verification
- `kubectl get all` — view all resources
- `minikube service frontend --url` — access frontend via Service
- `kubectl exec -it postgres-0 -- psql -U postgres -c "SELECT * FROM demo;"` — verify DB persistence
