# Taban image olarak python:3.9-slim kullanılıyor
FROM python:3.9-slim

# Gerekli bağımlılıkları yükleyin
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Çalışma dizinini ayarlayın
WORKDIR /app

# Gereken Python paketlerini yükleyin
RUN pip install --no-cache-dir Flask google-cloud-storage opencv-python-headless insightface onnxruntime google-cloud-firestore firebase_admin google-cloud-logging

# Uygulama dosyalarını kopyalayın
COPY . .

# 8080 portunu expose edin
EXPOSE 8080

# Uygulamayı başlatın
CMD ["python", "app.py"]
