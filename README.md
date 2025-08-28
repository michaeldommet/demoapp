# ToDo App Helm Chart

This repository contains a Helm chart for deploying a ToDo application on Kubernetes. The application is built using Flask and MySQL, and includes OpenTelemetry instrumentation for tracing.

## Repository Structure

```
.
├── .helmignore                # Helm ignore file
├── Chart.yaml                 # Helm chart metadata
├── Dockerfile                 # Dockerfile for building the application image
├── values.yaml                # Default values for the Helm chart
├── charts/                    # Subcharts and common templates
│   └── common/                # Common Helm chart utilities
├── src/                       # Application source code
│   ├── app.py                 # Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── static/                # Static files (CSS, JS, etc.)
│   └── templates/             # HTML templates
└── templates/                 # Helm templates for Kubernetes resources
```

## Features

- **Flask Application**: A simple ToDo app with CRUD functionality.
- **MySQL Integration**: Uses MySQL as the backend database.
- **Helm Chart**: Deploys the application on Kubernetes with configurable values.
- **OpenTelemetry**: Tracing support for Flask and SQLAlchemy.
- **Customizable**: Easily configurable via `values.yaml`.

## Prerequisites

- Docker
- Kubernetes cluster
- Helm 3.x
- Python 3.8+ (for local development)

## Getting Started

### 1. Build the Docker Image

```bash
docker build -t todo-app:latest .
```

### 2. Deploy the Helm Chart

```bash
helm install todo ./ --values values.yaml
```

### 3. Access the Application

- The application will be exposed via a Kubernetes `LoadBalancer` service.
- Check the external IP of the service:

```bash
kubectl get svc
```

- Open the external IP in your browser.

## Configuration

You can customize the deployment by modifying the `values.yaml` file. Key parameters include:

- **replicaCount**: Number of application replicas.
- **image.repository**: Docker image repository.
- **service.type**: Kubernetes service type (e.g., `ClusterIP`, `LoadBalancer`).
- **ingress.enabled**: Enable or disable ingress.

## Development

### Run Locally

1. Install dependencies:

   ```bash
   pip install -r src/requirements.txt
   ```

2. Run the application:

   ```bash
   python src/app.py
   ```

3. Open `http://localhost:5000` in your browser.

### Database Initialization

The MySQL database is initialized with a `ConfigMap` that creates the `appdb` database and a `todo` table.

## OpenTelemetry

The application is instrumented with OpenTelemetry for tracing. Traces are exported using the OTLP exporter. You can configure the exporter endpoint in `src/app.py`.

## Helm Chart Details

### Templates

- `templates/deployment.yaml`: Defines the application deployment.
- `templates/service.yaml`: Exposes the application as a service.
- `templates/ingress.yaml`: Configures ingress for the application.
- `templates/statefulset.yaml`: Manages the MySQL database.

### Subcharts

The `charts/common` directory contains reusable Helm templates and utilities.

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.
