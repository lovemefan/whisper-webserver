# Whisper webserver 
Whisper is a general-purpose speech recognition model trained by openai.
that can perform multilingual speech recognition as well as speech translation and language identification.
for more detail: https://github.com/openai/whisper

Whisper webserver provides an HTTP interface build with sanic framework of python.


* transcribe
* language detect

## Quick start
Docker hub: https://hub.docker.com/r/lovemefan/whisper-webserver
```bash
# for gpu
docker run -d --gpus all -p 9000:9000 -e ASR_MODEL=base lovemefan/whisper-webserver:cuda-11.2.0

# for cpu

docker run -d --gpus all -p 9000:9000 -e ASR_MODEL=base lovemefan/whisper-webserver:amd64

# for mac apple chip

docker run -d --gpus all -p 9000:9000 -e ASR_MODEL=base lovemefan/whisper-webserver:arm64

```

## RUN

```bash
git clone https://github.com/lovemefan/whisper-webserver.git
cd whisper-webserver
pip install -r requirement.txt
gunicorn --bind 0.0.0.0:9000 --workers 1  app.webservice:app -k uvicorn.workers.UvicornWorker
```


## Docker build
### FOR CPU
```bash
# Build Image
docker build -f Dockerfile-cpu -t whisper-webserver-cpu .

# Run Container
docker run -d -p 9000:9000 whisper-webserver-cpu
# or
docker run -d -p 9000:9000 -e ASR_MODEL=base whisper-webserver-cpu
```

### FOR GPU
```bash
# Build Image
docker build -f Dockerfile-gpu -t whisper-webserver-gpu .

# Run Container
docker run -d --gpus all -p 9000:9000 whisper-webserver-gpu
# or
docker run -d --gpus all -p 9000:9000 -e ASR_MODEL=base whisper-webserver-gpu
```

### FOR ARM (M1 chip Tested)
```bash
# Build Image
docker build -f Dockerfile-arm -t whisper-webserver-arm64 .

# Run Container
docker run -d -p 9000:9000 whisper-webserver-arm64
# or
docker run -d -p 9000:9000 -e ASR_MODEL=base whisper-webserver-arm64
```

## Usage
use 16hz, 16bit, mono format of wav file
```bash
curl --location --request POST --X POST 'http://localhost:9000/v1/api/speech/recognition' \
--form 'audio=@/path/audio.wav'
```

