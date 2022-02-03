

Minikube was installed following [official tutorial](https://minikube.sigs.k8s.io/docs/start/).

nginx reverse proxy was created to route traffic from default server http port `80` to `show-off-ui` service inside
kubernetes cluster. Script for initializing nginx configuration can be found in `devops/scripts/init_reverse_proxy.bash`
while configuration itself is located in `devops/configs/reverse_proxy.conf`. Setup was created with help of
[this tutorial](https://www.scaleway.com/en/docs/tutorials/nginx-reverse-proxy/).