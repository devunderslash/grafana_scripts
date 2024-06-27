# Grafana Data Exporters
This repository contains a collection of exporters for Grafana. The exporters are written in Python and are designed to be run as a cripts. The exporters are designed to simplify the process of exporting data from Grafana via it's api.

## Exporters
- [Grafana Dashboard Exporter](#Grafana-Dashboard-Exporter)
- [Grafana Alert Exporter](#Grafana-Alert-Exporter)
- [Grafana Datasource Exporter](#Grafana-Datasource-Exporter)
- [Grafana Notification Template Exporter](#Grafana-Notification-Template-Exporter)

## Setup
It is best to run these scripts in a virtual environment. To create a virtual environment, run the following command:
```bash
python3 -m venv venv
```

To activate the virtual environment, run the following command:
```bash
source venv/bin/activate
```

To install the required packages, run the following command:
```bash
pip install -r requirements.txt
```

To deactivate the virtual environment, run the following command:
```bash
deactivate
```

## Configure
To configure the exporters, you will need to create a `.env` file in the root of the repository. The `.env` file should contain the following variables:
```bash
GRAFANA_URL=https://grafana.example.com
GRAFANA_API_KEY=<api key created in grafana>
```

## Grafana Dashboard Exporter
The Grafana Dashboard Exporter is a script that exports all dashboards from a Grafana instance. The script will export the dashboards as json files to a specified directory.

### Usage
```bash
python3 grafana_dashboard_exporter.py
```

## Grafana Alert Exporter
The Grafana Alert Exporter is a script that exports all alerts from a Grafana instance. The script will export the alerts as json and hcl files to a specified directory.

### Usage
```bash
python3 grafana_alert_exporter.py
```

## Grafana Datasource Exporter
The Grafana Datasource Exporter is a script that exports all datasources from a Grafana instance. The script will export the datasources as json files to a specified directory.

### Usage
```bash
python3 grafana_datasource_exporter.py
```

## Grafana Notification Template Exporter
The Grafana Notification Template Exporter is a script that exports all notification templates from a Grafana instance. The script will export the notification templates as json files to a specified directory.

### Usage
```bash
python3 grafana_notification_template_exporter.py
```
