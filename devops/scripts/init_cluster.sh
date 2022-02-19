#!/bin/bash

cd "../$(dirname "$0")" || exit 1
CURRENT_DIR="$(pwd)"

# installation of argo and minikube if do not exist
# installation of argocd command - https://argo-cd.readthedocs.io/en/stable/cli_installation/ & https://github.com/argoproj/argo-cd/issues/7035

echo 'Installing minikube'
minikube start --mount-string="/var/kubernetes/show-off-pv:/var/kubernetes" --mount

echo 'Installing ArgoCD'
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

echo 'Switching image to arm ones'
kubectl config set-context --current --namespace=argocd
mkdir configs
cd configs || exit 1
resources=(argocd-server argocd-repo-server argocd-application-controller argocd-dex-server)
for resource in "${resources[@]}"
do
  echo "Switching image for $resource"
  resource_file="$resource.yaml"
  if [[ $resource != 'argocd-application-controller' ]]; then
    kubectl get deployments "$resource" -o yaml > "$resource_file"
  else
    kubectl get statefulsets "$resource" -o yaml > "$resource_file"
  fi
  sed -i "s;quay.io/argoproj/argocd:v2.2.5;spaladium/argocd:v2.1.2;g" "$resource_file"
  if [[ $resource != 'argocd-dex-server' ]]; then
    kubectl apply -f "$resource_file"
  else
    sed -i "s;ghcr.io/dexidp/dex:v2.30.2;dexidp/dex:v2.30.2;g" "$resource_file"
    kubectl apply -f "$resource_file"
  fi
done
kubectl delete pod "$(kubectl get pods | grep argocd-application* | cut -d" " -f1)"

# todo auto create Argo CRD after arm64 command in version 2.3
echo 'Admin password is':
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
