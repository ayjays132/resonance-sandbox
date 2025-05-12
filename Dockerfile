
# Docker setup for Resonance Sandbox
FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
ENTRYPOINT ["resonance-sandbox"]
