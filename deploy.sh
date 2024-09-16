#!/bin/bash

set -e

# Build and push Docker images
docker build -t dst-server-with-monitor:latest .
docker build -t dst-server-tests:latest -f Dockerfile.test .

# TODO: Replace with your actual container registry
REGISTRY="your-container-registry"
docker tag dst-server-with-monitor:latest $REGISTRY/dst-server-with-monitor:latest
docker tag dst-server-tests:latest $REGISTRY/dst-server-tests:latest
docker push $REGISTRY/dst-server-with-monitor:latest
docker push $REGISTRY/dst-server-tests:latest

# Apply Kubernetes manifests
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/persistent-volume-claim.yaml
kubectl apply -f k8s/karpenter-provisioner.yaml
kubectl apply -f k8s/test-job.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Wait for the test job to complete
kubectl wait --for=condition=complete job/dst-server-tests --timeout=300s

# Check if the test job was successful
if [ $? -eq 0 ]; then
    echo "Tests passed successfully. Continuing with deployment."
else
    echo "Tests failed. Aborting deployment."
    exit 1
fi

# Wait for the deployment to be ready
kubectl rollout status deployment/dst-server

echo "Deployment completed successfully!"