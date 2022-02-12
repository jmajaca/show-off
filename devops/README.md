Minikube was installed following [official tutorial](https://minikube.sigs.k8s.io/docs/start/).

nginx reverse proxy was created to route traffic from default server http port `80` to `show-off-ui` service inside
kubernetes cluster. Script for initializing nginx configuration can be found in `devops/scripts/init_reverse_proxy.bash`
while configuration itself is located in `devops/configs/reverse_proxy.conf`. Setup was created with help of
[this tutorial](https://www.scaleway.com/en/docs/tutorials/nginx-reverse-proxy/).

CI-CD pipeline was created via GitHub actions. 
Resources for creating build part of pipeline can be found at 
[GitHub](https://github.com/marketplace/actions/build-and-push-docker-images#path-context),
[docs.docker](https://docs.docker.com/ci-cd/github-actions/) and
[blog.docker](https://www.docker.com/blog/docker-v2-github-action-is-now-ga/).
For deploy part of pipeline [this](https://github.com/appleboy/ssh-action) GitHub action was used.

## Volumes

Volume for pre-trained weights was created with command `minikube mount /var/kubernetes/show-off:/var/kubernetes &`.
Directory `/var/kubernetes/show-off` contains files: `CTPN.pth`.