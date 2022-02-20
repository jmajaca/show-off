#!/bin/bash

cd "../$(dirname "$0")" || exit 1
ROOT_DIR="$(pwd)"

echo 'Creating show-off namespace'
cd "$ROOT_DIR/administration/show-off" || exit 1
kubectl apply -f namespace.yaml

echo 'Switching to show-off namespace'
kubectl config set-context --current --namespace=show-off

echo 'Creating applications'
cd "$ROOT_DIR/applications/show-off" || exit 1

for dir in */ ; do
    application=${dir::-1}
    echo "Creating application: $application"
    kubectl apply -f "$application/deployment.yaml"
    kubectl apply -f "$application/service.yaml"
done

echo 'All done'