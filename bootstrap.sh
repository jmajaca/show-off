#!/bin/bash

cd "$(dirname "$0")" || exit 1

# installation of argo and minikube if do not exist
# installation of argocd command - https://argo-cd.readthedocs.io/en/stable/cli_installation/ & https://github.com/argoproj/argo-cd/issues/7035

echo 'Installing minikube'
minikube start --addons=ingress --mount-string="/var/kubernetes/show-off-pv:/var/kubernetes" --mount

echo 'Installing ArgoCD'
mkdir bin
curl -sSL -o bin/argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-arm64
chmod +x bin/argocd
minikube kubectl -- create namespace argocd
minikube kubectl -- apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

echo 'Switching image to arm ones'
minikube kubectl -- config set-context --current --namespace=argocd
mkdir configs
cd configs || exit 1
resources=(argocd-server argocd-repo-server argocd-application-controller argocd-dex-server)
sleep 5
for resource in "${resources[@]}"
do
  echo "Switching image for $resource"
  resource_file="$resource.yaml"
  if [[ $resource != 'argocd-application-controller' ]]; then
    minikube kubectl -- get deployments "$resource" -o yaml > "$resource_file"
  else
    minikube kubectl -- get statefulsets "$resource" -o yaml > "$resource_file"
  fi
  sed -i "s;quay.io/argoproj/argocd:v2.2.5;spaladium/argocd:v2.1.2;g" "$resource_file"
  if [[ $resource != 'argocd-dex-server' ]]; then
    minikube kubectl -- apply -f "$resource_file"
  else
    sed -i "s;ghcr.io/dexidp/dex:v2.30.2;dexidp/dex:v2.30.2;g" "$resource_file"
    minikube kubectl -- apply -f "$resource_file"
  fi
done
cd .. || exit 1

spin='-\|/'
i=0
end_wait=$((SECONDS+50))
while [ $SECONDS -lt $end_wait ]; do
  i=$(( (i+1) %4 ))
  printf "\r Waiting for ArgoCD to startup ${spin:$i:1}"
  sleep .1
done
printf "\n"

minikube kubectl -- delete "$(minikube kubectl -- get events | grep BackOff | sed -r "s;.*(pod/[^ ]+).*;\1;")"

echo 'Setup Jaeger Operator'
minikube kubectl -- create namespace observability
minikube kubectl -- apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.8.0/cert-manager.yaml
minikube kubectl -- create -f https://github.com/jaegertracing/jaeger-operator/releases/download/v1.33.0/jaeger-operator.yaml -n observability

echo 'Setup ArgoCD'

# expose argocd
cat << EOF | minikube kubectl -- apply -f -
apiVersion: v1
kind: Service
metadata:
  name: argocd-server-2
  namespace: argocd
spec:
  ports:
  - name: https
    port: 443
    protocol: TCP
    targetPort: 8080
    nodePort: 31000
  selector:
    app.kubernetes.io/name: argocd-server
  sessionAffinity: None
  type: NodePort
EOF
sleep 3

# login
argo_password="$(minikube kubectl -- get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)"
yes | bin/argocd login "$(minikube ip):31000" --username admin --password "$argo_password"

# sync
yes | bin/argocd cluster add "$(minikube kubectl -- config get-contexts -o name)"
bin/argocd app create platform --repo 'https://github.com/jmajaca/show-off.git' \
                               --path 'devops/namespace-apps' \
                               --revision devops \
                               --dest-server 'https://kubernetes.default.svc' \
                               --directory-recurse \
                               --sync-policy auto \
                               --auto-prune \
                               --self-heal \
                               --sync-option CreateNamespace=true \
                               --sync-option ApplyOutOfSyncOnly=true \
                               --sync-option PruneLast=true

bin/argocd app sync platform > /dev/null
APPLICATIONS=($(bin/argocd app list -o name))
for application in "${APPLICATIONS[@]}"
do
  sleep 2
  echo "Syncing $application"
  bin/argocd app sync "$application" > /dev/null
done

echo 'Cleanup'
rm -rf bin
rm -rf configs
minikube kubectl -- delete svc/argocd-server-2
minikube kubectl -- config set-context --current --namespace=default
