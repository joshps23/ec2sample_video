FROM python:3.11.5
COPY . /app
WORKDIR /app
RUN apt-get update -y
RUN apt install libgl1-mesa-glx -y
RUN apt-get update && apt-get install 'ffmpeg'\
    'libsm6'\
    'libxext6'  -y
RUN pip install opencv-python==4.10.0.84
RUN pip install -r requirements.txt
RUN adduser -u 5000 --disabled-password --gecos "" appuser && \
    adduser appuser video && \
    chown -R appuser /app
USER appuser
EXPOSE 5000
ENV NAME World
CMD ["python","application.py"]