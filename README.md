## Simple HTTP checker in Kubernetes

* Check HTTP status code
* Check response time
* Check SSL cert valid

### Notification transports support

* Slack

### Install

#### Clone repo

    git clone https://github.com/kuberstack/kuberstack-monitoring-http.git

#### Create Slack bot

[Create Slack bot](https://my.slack.com/services/new/bot) and getting *token* for next step

#### Edit config file

    vim kuberstack-monitoring-http/manifestos/configmap.yaml
  
#### Deploy http monitoring

    kubectl create -f kuberstack-monitoring-http/manifestos/