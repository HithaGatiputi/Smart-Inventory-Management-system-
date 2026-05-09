
# Enterprise Kirana AI Forecasting Platform

Production-style AI forecasting platform for Indian kirana stores.

## Features
- FastAPI backend
- KMeans clustering
- DecisionTree + XGBoost models
- Explainable AI
- Redis caching
- PostgreSQL integration
- JWT authentication
- Docker deployment
- React scenario simulator

## Run Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

## Run Docker
cd deployment
docker-compose up --build
