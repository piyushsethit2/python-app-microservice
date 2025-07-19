# Python App Microservice

Flask-based microservice for malicious URL detection using app.py configuration.

## Quick Start

### Local Development
```bash
pip install -r requirements.txt
python3 app.py
```

### Docker
```bash
docker build -t python-app-microservice .
docker run -p 5000:5000 python-app-microservice
```

## Port: 5000
## Model: distilbert-base-uncased 