# company_graph_web_service

## Usage
```
gunicorn -b 0.0.0.0:8000 -w 4 -k uvicorn.workers.UvicornWorker --timeout 120 app.factory:create_app
```