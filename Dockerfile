FROM ubuntu:20.04

ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get -qq update \
    && apt-get -qq install -y python3 python3-pip ffmpeg libsm6 libxext6

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY main.py .
COPY functions.py .
RUN mkdir features
COPY ./features/ ./features/
RUN mkdir upload_images

EXPOSE 5555
EXPOSE 8055 

# Testing
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8055", "--workers", "2"]

# Production
# ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8055", "--workers", "2", "--log-level", "critical"]