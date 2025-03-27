# Use official Python image
FROM python:3.10-slim

# Set work directory inside container
WORKDIR /app

# Copy project files into container
COPY . .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*
    
# Install system dependencies
RUN apt-get update && apt-get install -y \
portaudio19-dev \
libportaudio2 \
libportaudiocpp0 \
ffmpeg \
&& rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose Streamlit (8501) and FastAPI (8000) ports
EXPOSE 8000
EXPOSE 8501

# Start both servers using a shell script (we'll define it below)
CMD ["sh", "start.sh"]
