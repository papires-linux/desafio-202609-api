# 🚀 Desafio — API Flask + Kubernetes + AWS EKS + Prometheus

Aplicação desenvolvida como parte de um desafio técnico com foco em **Cloud, Kubernetes, observabilidade e CI/CD**.

O projeto consiste em uma API REST simples desenvolvida em **Python/Flask**, containerizada com **Docker** e preparada para execução em um cluster **AWS EKS**.

A aplicação possui endpoints de saúde, readiness, processamento simulado e exposição de métricas no formato do **Prometheus**.

O processo de entrega é automatizado por meio do **GitHub Actions**, que realiza o build da imagem Docker, publica a imagem no Docker Hub e executa o deploy dos manifests Kubernetes no EKS.

---

## 📋 Objetivos do projeto

O projeto foi desenvolvido para atender aos seguintes requisitos:

- Desenvolver uma aplicação simples para demonstrar observabilidade;
- Containerizar a aplicação utilizando Docker;
- Executar a aplicação em Kubernetes;
- Disponibilizar a aplicação publicamente;
- Implementar health check e readiness check;
- Expor métricas para Prometheus;
- Implementar escalabilidade horizontal utilizando HPA;
- Publicar o projeto no GitHub;
- Implementar pipeline de CI/CD;
- Automatizar o deploy da aplicação no AWS EKS;
- Utilizar uma imagem Docker versionada por commit;
- Permitir demonstração de um novo deploy durante a apresentação.

---

# 🏗️ Arquitetura

A solução utiliza a seguinte arquitetura:

```text
                    ┌──────────────────────┐
                    │      Developer       │
                    │                      │
                    │ git push / Pull Req. │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    GitHub Actions    │
                    │                      │
                    │ Build Docker Image   │
                    │ Push Docker Hub      │
                    │ Configure AWS        │
                    │ Configure kubectl    │
                    │ Deploy Kubernetes    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Docker Hub      │
                    │                      │
                    │ api-ppteste:<SHA>    │
                    │ api-ppteste:latest   │
                    └──────────┬───────────┘
                               │
                               ▼
             ┌───────────────────────────────────┐
             │             AWS EKS                │
             │                                   │
             │  ┌─────────────────────────────┐  │
             │  │        LoadBalancer         │  │
             │  └──────────────┬──────────────┘  │
             │                 │                 │
             │                 ▼                 │
             │  ┌─────────────────────────────┐  │
             │  │         Service             │  │
             │  │      svc-api-ppteste        │  │
             │  └──────────────┬──────────────┘  │
             │                 │                 │
             │                 ▼                 │
             │  ┌─────────────────────────────┐  │
             │  │        Deployment           │  │
             │  │        api-ppteste           │  │
             │  └──────────────┬──────────────┘  │
             │                 │                 │
             │          ┌──────┴──────┐          │
             │          ▼             ▼          │
             │       Pod #1         Pod #2       │
             │                                   │
             │          HPA: 1 → 3               │
             └───────────────────────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Prometheus      │
                    │                      │
                    │ /metrics             │
                    │ requests             │
                    │ latency              │
                    └──────────────────────┘
```

---

# 🧰 Tecnologias utilizadas

| Tecnologia | Utilização |
|---|---|
| Python 3.11 | Linguagem da aplicação |
| Flask 3.1 | Framework HTTP |
| Prometheus Client | Exposição de métricas |
| Docker | Containerização |
| Kubernetes | Orquestração |
| AWS EKS | Kubernetes gerenciado |
| AWS Load Balancer | Exposição pública |
| HPA | Escalabilidade horizontal |
| Docker Hub | Registry da imagem |
| GitHub | Versionamento |
| GitHub Actions | CI/CD |
| kubectl | Administração do Kubernetes |

---

# 📁 Estrutura do projeto

```text
desafio-202609-api-main/
│
├── .github/
│   └── workflows/
│       └── docker-image.yml
│
├── k8s/
│   ├── deploy.yaml
│   ├── hpa.yaml
│   └── svc.yaml
│
├── .gitignore
├── Dockerfile
├── main.py
├── requirements.txt
└── README.md
```

---

# 🔌 API

A aplicação utiliza Flask e disponibiliza os seguintes endpoints.

## `GET /`

Endpoint principal da aplicação.

### Exemplo

```bash
curl http://<LOAD_BALANCER>/ 
```

### Resposta

```json
{
  "message": "Olá teste Observability!",
  "version": "1.0.0",
  "environment": "development"
}
```

A versão e o ambiente podem ser configurados através das variáveis:

```text
APP_VERSION
ENVIRONMENT
```

---

## `GET /health`

Endpoint utilizado para verificar se a aplicação está saudável.

```bash
curl http://<LOAD_BALANCER>/health
```

Resposta:

```json
{
  "status": "healthy"
}
```

Esse endpoint é utilizado pelo Kubernetes através da:

**Liveness Probe**

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
```

---

## `GET /ready`

Endpoint utilizado para verificar se a aplicação está pronta para receber tráfego.

```bash
curl http://<LOAD_BALANCER>/ready
```

Resposta:

```json
{
  "status": "ready"
}
```

Esse endpoint é utilizado pelo Kubernetes através da:

**Readiness Probe**

```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
```

---

## `GET /metrics`

Endpoint utilizado para exposição das métricas no formato esperado pelo Prometheus.

```bash
curl http://<LOAD_BALANCER>/metrics
```

Entre as métricas customizadas disponibilizadas pela aplicação estão:

```text
app_http_requests_total
app_http_request_duration_seconds
```

### Contador de requisições

A aplicação registra requisições através da métrica:

```text
app_http_requests_total
```

Com os labels:

```text
method
endpoint
status
```

Exemplo:

```text
app_http_requests_total{
  method="GET",
  endpoint="/",
  status="200"
}
```

### Latência

A aplicação também registra o tempo de resposta através da métrica:

```text
app_http_request_duration_seconds
```

Com o label:

```text
endpoint
```

---

# ⚙️ Endpoint `/work`

O endpoint `/work` foi criado para simular processamento da aplicação e gerar comportamento observável.

```bash
curl http://<LOAD_BALANCER>/work
```

Resposta:

```json
{
  "message": "Work completed"
}
```

Durante a execução, a aplicação adiciona um atraso aleatório entre aproximadamente:

```text
50ms
300ms
```

Esse comportamento permite gerar diferentes tempos de resposta e facilitar a demonstração de métricas de latência.

---

# 🐳 Docker

A aplicação utiliza como base:

```dockerfile
FROM python:3.11-slim
```

A porta utilizada pela aplicação é:

```text
8080
```

## Build

Para criar a imagem localmente:

```bash
docker build -t api-ppteste:latest .
```

## Executar

```bash
docker run --rm -p 8080:8080 api-ppteste:latest
```

A aplicação estará disponível em:

```text
http://localhost:8080
```

Teste:

```bash
curl http://localhost:8080/
```

Health check:

```bash
curl http://localhost:8080/health
```

Métricas:

```bash
curl http://localhost:8080/metrics
```

---

# ☸️ Kubernetes

A aplicação possui três manifests principais:

```text
k8s/
├── deploy.yaml
├── hpa.yaml
└── svc.yaml
```

---

# 🚀 Deployment

O arquivo:

```text
k8s/deploy.yaml
```

define o Deployment:

```text
api-ppteste
```

Inicialmente é configurada uma réplica:

```yaml
replicas: 1
```

O container utiliza a imagem:

```yaml
image: ${DOCKER_IMAGE}:${GITHUB_SHA}
```

Isso permite utilizar o SHA do commit do GitHub como versão da imagem.

Exemplo:

```text
usuario/api-ppteste:7c8a9e1...
```

Essa estratégia evita depender exclusivamente da tag `latest` e permite identificar exatamente qual commit está executando no cluster.

---

# 📊 Resource Requests e Limits

O container possui os seguintes recursos:

```yaml
requests:
  cpu: 100m
  memory: 128Mi

limits:
  cpu: 500m
  memory: 256Mi
```

### Requests

Representam a quantidade mínima de recursos solicitada pelo Pod para seu agendamento.

```text
CPU:    100m
Memory: 128Mi
```

### Limits

Definem o limite máximo permitido para o container.

```text
CPU:    500m
Memory: 256Mi
```

Esses valores também são importantes para o funcionamento do HPA baseado em utilização de CPU.

---

# ❤️ Health Checks

Foram implementadas duas probes diferentes.

## Liveness Probe

```text
/health
```

Utilizada para determinar se o container continua saudável.

Caso o processo deixe de responder corretamente, o Kubernetes pode reiniciar o container.

## Readiness Probe

```text
/ready
```

Utilizada para determinar se o Pod está pronto para receber tráfego.

Isso evita enviar tráfego para um Pod que ainda não esteja pronto.

---

# ⚖️ Horizontal Pod Autoscaler

O arquivo:

```text
k8s/hpa.yaml
```

configura o:

```text
HorizontalPodAutoscaler
```

Configuração:

```text
Minimum replicas: 1
Maximum replicas: 3
CPU target:       60%
```

Ou seja:

```text
          CPU < 60%
              │
              ▼
        ┌───────────┐
        │  1 Pod    │
        └───────────┘

          CPU > 60%
              │
              ▼
       ┌──────────────┐
       │ Scale Out    │
       │ 2 / 3 Pods   │
       └──────────────┘
```

A configuração é:

```yaml
minReplicas: 1
maxReplicas: 3
```

com utilização média de CPU:

```yaml
averageUtilization: 60
```

---

# 🌐 Service

O arquivo:

```text
k8s/svc.yaml
```

cria um Kubernetes Service do tipo:

```text
LoadBalancer
```

Nome:

```text
svc-api-ppteste
```

A porta externa utilizada é:

```text
80
```

que encaminha para:

```text
8080
```

Fluxo:

```text
Internet
   │
   ▼
AWS Load Balancer
   │
   ▼
Service :80
   │
   ▼
Pod :8080
   │
   ▼
Flask
```

Após o deploy, o endereço externo pode ser obtido com:

```bash
kubectl get svc svc-api-ppteste -n homo
```

Exemplo:

```text
NAME              TYPE           EXTERNAL-IP
svc-api-ppteste   LoadBalancer   xxx.amazonaws.com
```

A API poderá então ser acessada através do endereço disponibilizado pelo Load Balancer.

---

# 🔭 Observabilidade

A aplicação foi preparada para trabalhar com **Prometheus**.

O endpoint:

```text
/metrics
```

expõe métricas utilizando a biblioteca:

```text
prometheus_client
```

Foram implementadas métricas relacionadas a:

- quantidade de requisições;
- endpoint acessado;
- método HTTP;
- status HTTP;
- tempo de resposta.

Isso permite utilizar a aplicação como fonte de métricas para uma stack de observabilidade baseada em:

```text
Application
     │
     ▼
 /metrics
     │
     ▼
 Prometheus
     │
     ▼
 Grafana
```

---

# 🔄 CI/CD

O pipeline está localizado em:

```text
.github/workflows/docker-image.yml
```

O workflow é acionado em:

```yaml
push:
  branches:
    - main

pull_request:
  branches:
    - main
```

Entretanto, o job de deploy possui uma condição que permite sua execução somente em um `push` para a branch `main`:

```yaml
if: github.event_name == 'push' && github.ref == 'refs/heads/main'
```

Portanto, o fluxo efetivo de deploy é:

```text
git push
   │
   ▼
main
   │
   ▼
GitHub Actions
   │
   ├── Checkout
   │
   ├── Docker Buildx
   │
   ├── Login Docker Hub
   │
   ├── Docker Build
   │
   ├── Docker Push
   │
   ├── AWS Authentication
   │
   ├── Configure kubectl
   │
   ├── Apply Kubernetes manifests
   │
   ├── Wait Rollout
   │
   └── Validate Deployment
```

---

# 🐳 Build e Push da imagem

O pipeline gera duas tags para a imagem:

```text
latest
```

e:

```text
<github-sha>
```

Exemplo:

```text
docker-user/api-ppteste:latest
docker-user/api-ppteste:a82d7f91...
```

A tag baseada no SHA permite rastrear qual versão do código está implantada.

---

# ☁️ AWS

O workflow utiliza as credenciais configuradas no GitHub para autenticar na AWS.

Atualmente a autenticação está configurada através das seguintes secrets:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

A região utilizada é:

```text
us-east-1
```

O cluster configurado no workflow é:

```text
eks-01teste
```

A configuração do Kubernetes é obtida através do comando:

```bash
aws eks update-kubeconfig \
  --region $AWS_REGION \
  --name $EKS_CLUSTER_NAME
```

Após isso, o pipeline valida a conexão:

```bash
kubectl cluster-info
kubectl get nodes
```

---

# 🔐 GitHub Secrets

Para executar o pipeline é necessário configurar os secrets no GitHub.

## Docker Hub

```text
DOCKER_USERNAME
DOCKER_PASSWORD
```

## AWS

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

### Importante

As credenciais não devem ser armazenadas diretamente no código-fonte ou nos manifests Kubernetes.

Elas devem permanecer configuradas como **GitHub Actions Secrets**.

---

# 🌎 Namespace

A aplicação é implantada no namespace:

```text
homo
```

O workflow define:

```yaml
K8S_NAMESPACE: homo
```

Antes de executar o deploy, o namespace deve existir no cluster.

Caso ainda não exista:

```bash
kubectl create namespace homo
```

Verificar:

```bash
kubectl get namespace homo
```

---

# 📦 Deploy manual

Apesar de o projeto possuir CI/CD, também é possível realizar o deploy manualmente.

Primeiro configure o contexto do EKS:

```bash
aws eks update-kubeconfig \
  --region us-east-1 \
  --name eks-01teste
```

Valide:

```bash
kubectl get nodes
```

Crie o namespace:

```bash
kubectl create namespace homo
```

Caso já exista, o Kubernetes informará que o namespace já está presente.

---

## Aplicar os manifests

Como os manifests utilizam variáveis:

```text
DOCKER_IMAGE
GITHUB_SHA
```

é necessário defini-las antes do deploy.

Exemplo:

```bash
export DOCKER_IMAGE=seu-usuario/api-ppteste
export GITHUB_SHA=latest
```

Depois:

```bash
for file in k8s/*.yaml; do
  envsubst < "$file" | kubectl apply -f - --namespace homo
done
```

---

# 🔎 Validando o deployment

Verificar o Deployment:

```bash
kubectl get deployment -n homo
```

Verificar os Pods:

```bash
kubectl get pods -n homo
```

Verificar o Service:

```bash
kubectl get svc -n homo
```

Verificar o HPA:

```bash
kubectl get hpa -n homo
```

Para obter informações detalhadas:

```bash
kubectl describe deployment api-ppteste -n homo
```

---

# 🔄 Rollout

Após uma atualização:

```bash
kubectl rollout status \
  deployment/api-ppteste \
  -n homo \
  --timeout=300s
```

Ver histórico:

```bash
kubectl rollout history \
  deployment/api-ppteste \
  -n homo
```

---

# ↩️ Rollback

Caso uma versão apresente problema:

```bash
kubectl rollout undo \
  deployment/api-ppteste \
  -n homo
```

Validar:

```bash
kubectl rollout status \
  deployment/api-ppteste \
  -n homo
```

---

# 🧪 Testando a aplicação

Depois que o Load Balancer estiver provisionado:

```bash
kubectl get svc svc-api-ppteste -n homo
```

Obtenha o endereço externo e teste:

```bash
curl http://<EXTERNAL-IP>/
```

Health:

```bash
curl http://<EXTERNAL-IP>/health
```

Readiness:

```bash
curl http://<EXTERNAL-IP>/ready
```

Work:

```bash
curl http://<EXTERNAL-IP>/work
```

Metrics:

```bash
curl http://<EXTERNAL-IP>/metrics
```

---

# 📈 Testando o HPA

Verifique o estado:

```bash
kubectl get hpa -n homo
```

Exemplo:

```text
NAME             REFERENCE               TARGETS
api-ppteste-hpa  Deployment/api-ppteste  10%/60%
```

Para acompanhar continuamente:

```bash
kubectl get hpa -n homo -w
```

Também é possível observar os Pods:

```bash
kubectl get pods -n homo -w
```

A ideia é demonstrar que o Kubernetes pode aumentar a quantidade de réplicas quando o consumo de CPU atingir o threshold configurado.

---

# 📊 Consultando métricas

Para acessar as métricas diretamente:

```bash
curl http://<EXTERNAL-IP>/metrics
```

É possível encontrar métricas como:

```text
app_http_requests_total
```

e:

```text
app_http_request_duration_seconds
```

Essas métricas podem ser coletadas por um Prometheus instalado no cluster.

---

# 🧩 Configuração da aplicação

A aplicação suporta algumas variáveis de ambiente.

## `APP_VERSION`

Define a versão apresentada pelo endpoint `/`.

Exemplo:

```bash
APP_VERSION=2.0.0
```

## `ENVIRONMENT`

Define o ambiente da aplicação.

Exemplo:

```bash
ENVIRONMENT=homo
```

## `PORT`

Define a porta utilizada pela aplicação quando executada diretamente pelo Python.

Valor padrão:

```text
8080
```

---

# 🛡️ Boas práticas implementadas

O projeto possui algumas práticas importantes para uma aplicação Kubernetes:

### Containerização

A aplicação é executada dentro de um container Docker baseado em uma imagem `python:3.11-slim`.

### Health Check

A aplicação possui endpoint específico para:

```text
Liveness
```

### Readiness

A aplicação possui endpoint específico para:

```text
Readiness
```

### Resource Management

O Deployment possui:

```text
Requests
Limits
```

### Autoscaling

Foi implementado:

```text
Horizontal Pod Autoscaler
```

com:

```text
1 → 3 replicas
```

### Observabilidade

A aplicação expõe métricas no padrão Prometheus.

### Versionamento

As imagens são publicadas utilizando o SHA do commit.

### Automação

O deploy é executado automaticamente através do GitHub Actions.

---

# 🔐 Segurança

As credenciais utilizadas pelo pipeline não ficam armazenadas no código.

O projeto utiliza GitHub Secrets para armazenar:

```text
DOCKER_USERNAME
DOCKER_PASSWORD
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

Além disso, arquivos potencialmente sensíveis como:

```text
*.tfvars
*.tfstate
.env
```

estão configurados no `.gitignore`.

> Para ambientes produtivos, recomenda-se evoluir a autenticação AWS do GitHub Actions para **OIDC + IAM Role**, eliminando a necessidade de armazenar access keys de longa duração.

---

# 🧱 Separação de responsabilidades

O projeto da aplicação mantém responsabilidades separadas:

```text
Application
    │
    ├── main.py
    ├── requirements.txt
    └── Dockerfile

Kubernetes
    │
    └── k8s/
        ├── deploy.yaml
        ├── hpa.yaml
        └── svc.yaml

CI/CD
    │
    └── .github/workflows/
        └── docker-image.yml
```

A infraestrutura do EKS pode ser mantida em um repositório separado de IaC, utilizando Terraform.

Isso permite separar:

```text
Infrastructure as Code
          +
Application
          +
CI/CD
```

---

# 🔁 Fluxo completo de entrega

O fluxo completo da solução é:

```text
1. Desenvolvedor altera o código
              │
              ▼
2. git push origin main
              │
              ▼
3. GitHub Actions inicia
              │
              ▼
4. Checkout do código
              │
              ▼
5. Build da imagem Docker
              │
              ▼
6. Push para Docker Hub
              │
              ├── :latest
              └── :<commit-sha>
              │
              ▼
7. Autenticação AWS
              │
              ▼
8. Configuração do kubectl
              │
              ▼
9. Conexão com EKS
              │
              ▼
10. Renderização dos manifests
              │
              ▼
11. kubectl apply
              │
              ▼
12. Kubernetes atualiza Deployment
              │
              ▼
13. Readiness Probe
              │
              ▼
14. Rollout concluído
              │
              ▼
15. Aplicação disponível
```

---

# 🎯 Demonstração durante apresentação

Uma demonstração possível do projeto pode seguir o seguinte roteiro:

### 1. Mostrar a aplicação

```bash
curl http://<LOAD_BALANCER>/
```

### 2. Mostrar health check

```bash
curl http://<LOAD_BALANCER>/health
```

### 3. Mostrar métricas

```bash
curl http://<LOAD_BALANCER>/metrics
```

### 4. Mostrar Kubernetes

```bash
kubectl get pods -n homo
```

```bash
kubectl get svc -n homo
```

```bash
kubectl get hpa -n homo
```

### 5. Alterar a aplicação

Modificar, por exemplo, a mensagem:

```python
"message": "Olá teste Observability!"
```

para:

```python
"message": "Olá! Nova versão da aplicação!"
```

### 6. Commit e push

```bash
git add .
git commit -m "feat: update application message"
git push origin main
```

### 7. Demonstrar GitHub Actions

O pipeline executará:

```text
Build
   ↓
Docker Push
   ↓
AWS Authentication
   ↓
kubectl
   ↓
Deployment
   ↓
Rollout
```

### 8. Validar nova versão

```bash
curl http://<LOAD_BALANCER>/
```

Dessa forma é possível demonstrar o ciclo completo:

```text
Código
  ↓
GitHub
  ↓
CI/CD
  ↓
Docker
  ↓
EKS
  ↓
Kubernetes
  ↓
Aplicação
```

---

# 🧹 Limpeza

Para remover os recursos Kubernetes:

```bash
kubectl delete -f k8s/ --namespace homo
```

Ou individualmente:

```bash
kubectl delete deployment api-ppteste -n homo
kubectl delete service svc-api-ppteste -n homo
kubectl delete hpa api-ppteste-hpa -n homo
```

> A infraestrutura do AWS EKS não é criada por este repositório. Caso o cluster seja gerenciado por Terraform em outro projeto, a destruição da infraestrutura deve ser realizada pelo repositório de IaC correspondente.

---

# 📌 Considerações técnicas

A solução foi construída buscando manter uma arquitetura simples, reproduzível e adequada para demonstrar os principais conceitos envolvidos em uma plataforma Kubernetes.

A aplicação possui instrumentação mínima de observabilidade, enquanto o Kubernetes é responsável por:

- execução dos containers;
- gerenciamento dos Pods;
- health checks;
- readiness;
- exposição através de Load Balancer;
- controle de recursos;
- escalabilidade horizontal.

O GitHub Actions funciona como camada de automação entre o código-fonte, o registry de imagens e o cluster EKS.

A utilização do SHA do commit na tag da imagem também permite estabelecer uma relação direta entre:

```text
Git Commit
     │
     ▼
Docker Image
     │
     ▼
Kubernetes Deployment
     │
     ▼
Running Pod
```

Isso facilita rastreabilidade e troubleshooting durante o processo de entrega.
