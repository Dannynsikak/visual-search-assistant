
FROM node:18 as frontend-builder

WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install
COPY frontend .
RUN npm run build

FROM python:3.9

WORKDIR /app

COPY backend /app/backend
COPY --from=frontend-builder /app/frontend/dist /app/backend/static

RUN pip install -r backend/requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
