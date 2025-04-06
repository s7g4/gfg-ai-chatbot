# Deployment Guide

## Local Development
```bash
# Set up environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload
```

## Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

## Kubernetes Setup
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-support
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-support
  template:
    metadata:
      labels:
        app: ai-support
    spec:
      containers:
      - name: main
        image: ai-support:1.0
        ports:
        - containerPort: 8000
        env:
        - name: REDIS_URL
          value: "redis://redis:6379"
---
apiVersion: v1
kind: Service
metadata:
  name: ai-support
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8000
  selector:
    app: ai-support
```

## CI/CD Pipeline
```yaml
stages:
  - test
  - build
  - deploy

test:
  stage: test
  script:
    - pytest

build:
  stage: build
  script:
    - docker build -t ai-support .
    - docker tag ai-support registry/ai-support:$CI_COMMIT_SHA

deploy:
  stage: deploy
  script:
    - kubectl apply -f k8s/
