FROM joshps23/ubuntu-opencvgo:latest
COPY . /app
WORKDIR /app
RUN apt-get update -y
RUN apt install pkg-config
RUN apt install -y python3-pip

RUN apt-get install -y python3-blinker


# RUN apt install libgl1-mesa-glx -y
# RUN apt-get update && apt-get install 'ffmpeg'\
#     'libsm6'\
#     'libxext6'  -y

# RUN pip install opencv-contrib-python
# RUN apt-get install python3-opencv



RUN pip install -r requirements.txt
RUN adduser -u 80 --disabled-password --gecos "" appuser && \
    adduser appuser video && \
    chown -R appuser /app
USER appuser
EXPOSE 5000
# ENV NAME World
CMD ["python","application.py"]