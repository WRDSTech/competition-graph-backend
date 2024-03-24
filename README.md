# company_graph_web_service

## How to run the code
1. Connect to a remote Neo4j database by writing provided credentials into secrets file, or set up your own Neo4j according to doc: https://github.com/chuyanc/WRDS-Documentations/blob/main/Neo4j-Deployment-Data-Loading.md

2. Install Neo4j Python Driver:
```
pip install neo4j
```

3. Use gunicorn command to run the application: 
```
gunicorn -b 0.0.0.0:8000 -w 4 -k uvicorn.workers.UvicornWorker --timeout 120 app.factory:create_app
```