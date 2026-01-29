FROM python:3.11-slim
WORKDIR /app

# install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy source
COPY . .

ENV PYTHONUNBUFFERED=1

# At runtime, pass environment variables to change behavior (APP_ENV, GREETING_*, PORT)
CMD ["python", "-m", "app.main"]
