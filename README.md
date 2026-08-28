# Proyecto Final DevSecOps

## 1. Descripción
Plataforma local de CI/CD, observabilidad y seguridad implementada sobre Rocky Linux con Docker Compose.

La solución integra:
- Aplicación Python Flask.
- NGINX como balanceador de carga.
- Jenkins para CI/CD.
- Trivy para escaneo de vulnerabilidades.
- HashiCorp Vault para gestión de secretos.
- Prometheus, Node Exporter y cAdvisor para métricas.
- Grafana para dashboards.
- Elasticsearch, Filebeat y Kibana para centralización y visualización de logs.
- Healthchecks, reinicio automático y múltiples instancias de la aplicación.

## 2. Arquitectura

```text
GitHub
  |
  v
Jenkins
  |
  +--> Build
  +--> Tests
  +--> Trivy
          |
          +--> CRITICAL -> BLOQUEA DEPLOY
          |
          +--> OK -> Deploy
                      |
                      v
                    NGINX
                   /     \
                APP1     APP2

APP1/APP2 --> Filebeat --> Elasticsearch --> Kibana
APP1/APP2 --> Prometheus --> Grafana
Rocky Linux --> Node Exporter --> Prometheus
Docker --> cAdvisor --> Prometheus
Vault --> Secretos
```

## 3. Tecnologías

| Componente | Tecnología |
|---|---|
| Sistema operativo | Rocky Linux |
| Aplicación | Python Flask |
| Contenedores | Docker / Docker Compose |
| Balanceador | NGINX |
| CI/CD | Jenkins |
| Repositorio | GitHub |
| Seguridad | Trivy + Vault |
| Métricas | Prometheus |
| Dashboards | Grafana |
| Host | Node Exporter |
| Contenedores | cAdvisor |
| Logs | Filebeat |
| Almacenamiento de logs | Elasticsearch |
| Visualización de logs | Kibana |

## 4. Estructura

```text
devsecops-project/
├── app/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests/
├── nginx/
│   └── nginx.conf
├── monitoring/
│   └── prometheus.yml
├── elk/
│   └── filebeat.yml
├── docs/
│   └── evidencias/
├── docker-compose.yml
├── Jenkinsfile
├── .gitignore
└── README.md
```

## 5. Despliegue

```bash
git clone https://github.com/FarezH/proyecto-final-devsecops.git
cd proyecto-final-devsecops
docker compose build
docker compose up -d
docker compose ps
```

## 6. Aplicación

Endpoints disponibles:

```text
/          Aplicación
/health    Healthcheck
/error     Error de prueba
/metrics   Métricas Prometheus
```

Pruebas:

```bash
curl http://localhost
curl http://localhost/health
curl http://localhost/error
```

## 7. Balanceo de carga

NGINX distribuye tráfico entre APP1 y APP2.

```bash
for i in {1..10}; do curl -s http://localhost; echo; done
```

## 8. Prometheus

Acceso:

```text
http://IP_SERVIDOR:9090
```

Validar targets en:

```text
Status -> Target health
```

Targets esperados:
- prometheus
- app1
- app2
- node-exporter
- cadvisor

## 9. Grafana

Acceso:

```text
http://IP_SERVIDOR:3000
```

Datasource:

```text
http://prometheus:9090
```

Consulta PromQL básica:

```promql
up
```

## 10. ELK

Flujo de logs:

```text
APP1 / APP2 -> Docker logs -> Filebeat -> Elasticsearch -> Kibana
```

Kibana:

```text
http://IP_SERVIDOR:5601
```

Data View:

```text
filebeat-*
```

## 11. Vault

Vault se utiliza para evitar guardar secretos en el repositorio.

Ejemplo:

```bash
vault kv put secret/app db_user=usuario_app db_password='PASSWORD' api_key='API_KEY'
```

Los archivos sensibles se excluyen mediante `.gitignore`.

## 12. Trivy

El pipeline ejecuta:

```bash
trivy image --input app-image.tar --exit-code 1 --severity CRITICAL --scanners vuln
```

Si Trivy detecta vulnerabilidades críticas, Jenkins devuelve error y el despliegue se bloquea.

Durante las pruebas, Trivy detectó vulnerabilidades CRITICAL en la imagen basada en Debian. Como remediación se cambió la imagen base de:

```text
python:3.12-slim
```

a:

```text
python:3.12-alpine
```

## 13. Jenkins CI/CD

Flujo:

```text
Checkout -> Build -> Tests -> Trivy Scan -> Deploy
```

El archivo `Jenkinsfile` contiene el pipeline.

## 14. Pruebas automáticas

```bash
pytest -q
```

Resultado esperado:

```text
2 passed
```

## 15. Healthcheck y recuperación

Los contenedores de aplicación incluyen healthcheck y:

```yaml
restart: unless-stopped
```

Validación:

```bash
docker ps
```

La aplicación debe aparecer como `healthy`.

Prueba de reinicio:

```bash
docker kill devsecops-project-app1-1
docker ps
```

## 16. Simulación de fallo

```bash
docker stop devsecops-project-app1-1
curl http://localhost
```

NGINX debe continuar respondiendo mediante APP2.

## 17. Hardening

Medidas aplicadas:
- SELinux habilitado.
- Firewall activo.
- Aplicación ejecutada con usuario no-root.
- Imagen base Alpine.
- Secretos fuera del repositorio.
- Vault para secretos.
- Healthchecks.
- Reinicio automático.
- Trivy integrado al pipeline.
- Bloqueo automático ante vulnerabilidades CRITICAL.
- `.gitignore` para archivos sensibles.

## 18. Evidencias

Las capturas deben guardarse en:

```text
docs/evidencias/
```

Evidencias recomendadas:
1. Docker Compose operativo.
2. Aplicación funcionando.
3. Balanceo APP1/APP2.
4. Prometheus Targets UP.
5. Dashboard Grafana.
6. Logs en Kibana.
7. Vault funcionando.
8. Trivy detectando CRITICAL.
9. Jenkins bloqueando el pipeline.
10. Jenkins pipeline exitoso.
11. Healthcheck.
12. Reinicio automático.

## 19. Operación básica

```bash
docker compose ps
docker compose logs -f
docker compose down
docker compose up -d
```

## 20. Conclusión

El proyecto implementa una plataforma DevSecOps local que integra CI/CD, observabilidad, seguridad, gestión de secretos, escaneo de vulnerabilidades, balanceo de carga y mecanismos básicos de operación en producción.
