

# Flask App on Kubernetes with Monitoring & GitOps

## 🎯 Objective
This project was created as part of a DevOps assignment to practice:
- Deploying a Python Flask application on Kubernetes.
- Building and pushing Docker images to Docker Hub.
- Setting up Prometheus & Grafana for monitoring.
- Creating alert rules for application failures/restarts.
- Implementing GitOps using ArgoCD.

---

## 🏗️ Project Structure
```

flask-k8s-helm/
├── app.py
├── requirements.txt
├── Dockerfile
├── kubernetes/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── servicemonitor.yaml
│   └── prometheusrule.yaml
└── helm/
└── mychart/   (created via `helm create mychart`)

````

---

## 🚀 Step 1: Build & Push Docker Image
```bash
docker login -u david0mizrahi
docker build -t david0mizrahi/flask-app:1.0.0 .
docker push david0mizrahi/flask-app:1.0.0
````

---

## ☸️ Step 2: Start Minikube & Deploy the Application

```bash
minikube start --cpus=4 --memory=8192 --driver=docker
kubectl create namespace demo
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
```

Check resources:

```bash
kubectl get pods -n demo
kubectl get svc -n demo
```

Port-forward to access the app locally:

```bash
kubectl port-forward svc/flask-app-service -n demo 8080:80
```

Endpoints:

* [http://localhost:8080/health](http://localhost:8080/health)
* [http://localhost:8080/metrics](http://localhost:8080/metrics)

---

## 📊 Step 3: Install Prometheus & Grafana

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus-stack prometheus-community/kube-prometheus-stack -n monitoring --create-namespace
```

Check pods:

```bash
kubectl get pods -n monitoring
```

---

## 🔎 Step 4: Monitoring & Alerts

Apply ServiceMonitor and PrometheusRule:

```bash
kubectl apply -f kubernetes/servicemonitor.yaml
kubectl apply -f kubernetes/prometheusrule.yaml
```

Port-forward UIs:

```bash
kubectl port-forward svc/prometheus-stack-kube-prometheus-prometheus -n monitoring 9090:9090
kubectl port-forward svc/prometheus-stack-grafana -n monitoring 3000:80
```

Access:

* Prometheus: [http://localhost:9090](http://localhost:9090)
* Grafana: [http://localhost:3000](http://localhost:3000)

Retrieve Grafana admin password:

```bash
kubectl get secret prometheus-stack-grafana -n monitoring -o jsonpath="{.data.admin-password}" | base64 -d
```

Example Grafana query:

```
rate(flask_requests_total[5m])
```

---

## ⚠️ Step 5: Test Alerts

Trigger pod restarts:

```bash
kubectl get pods -n demo
kubectl exec -n demo <pod-name> -- pkill -f python
```

(repeat twice within 5 minutes)

Prometheus query to check:

```
increase(kube_pod_container_status_restarts_total{namespace="demo", pod=~"flask-app-.*"}[5m])
```

---

## 🔄 Step 6: ArgoCD for GitOps

Install ArgoCD:

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Port-forward ArgoCD server:

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Access UI: [https://localhost:8080](https://localhost:8080)

Retrieve initial password:

```bash
kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d
```

In ArgoCD UI, create an Application:

* **Repository URL:** `https://github.com/Davidvoodo/flask-k8s-helm`
* **Path:** `kubernetes`
* **Destination Namespace:** `demo`
* **Sync Policy:** Automated (optional)

---

## 🐙 Step 7: Push Project to GitHub

Initialize and push to GitHub repo:

```bash
git init
git add .
git commit -m "Initial commit: Flask app + k8s manifests + monitoring + ArgoCD"
git branch -M main
git remote add origin https://github.com/Davidvoodo/flask-k8s-helm.git
git push -u origin main
```

---

## 📷 Deliverables

* Screenshot of Prometheus alert when the app restarts.
* Screenshot of Grafana dashboard showing Flask app metrics.
* Screenshot of ArgoCD UI with synced deployment.

---

## 📝 Report

* **Steps Followed:** All steps from Minikube → Deployment → Monitoring → Alerts → GitOps.
* **Challenges:** e.g., Helm installation errors, Docker push issues, or ArgoCD repo access.
* **Lessons Learned:** Monitoring with Prometheus, alerting strategies, GitOps workflows with ArgoCD.

```
---

```




