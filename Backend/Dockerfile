FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for easyocr and lxml
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    python3-dev \
    gcc \
    g++ \
    libffi-dev \
    libjpeg-dev \
    libopencv-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    # Зависимости для PyMuPDF
    pkg-config \
    libfreetype6-dev \
    libharfbuzz-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (без PyMuPDF и EasyOCR)
COPY requirements.txt .

# Устанавливаем PyMuPDF через бинарные пакеты
RUN pip install --no-cache-dir --extra-index-url https://www.piwheels.org/simple PyMuPDF==1.23.3 || \
    pip install --no-cache-dir --only-binary=:all: PyMuPDF==1.23.3 || \
    pip install --no-cache-dir PyMuPDF==1.22.5  # Используем более старую версию как резервный вариант
    
# Теперь устанавливаем остальные зависимости
RUN grep -v "PyMuPDF" requirements.txt > requirements_filtered.txt && \
    pip install --no-cache-dir -r requirements_filtered.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p static/uploads/gallery static/uploads/posts

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"] 