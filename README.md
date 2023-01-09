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

docker run -d -p 9000:9000 -e ASR_MODEL=base lovemefan/whisper-webserver:amd64

# for mac apple chip

docker run -d -p 9000:9000 -e ASR_MODEL=base lovemefan/whisper-webserver:arm64

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
Response
```json
{
	"message": "Success",
	"code": 200,
	"data": {
		"text": " As for etchings, there are two kinds British and foreign.",
		"segments": [
			{
				"id": 0,
				"seek": 0,
				"start": 0,
				"end": 5,
				"text": " As for etchings, there are two kinds British and foreign.",
				"tokens": [
					50364,
					1018,
					337,
					1030,
					339,
					1109,
					11,
					456,
					366,
					732,
					3685,
					6221,
					293,
					5329,
					13,
					50614
				],
				"temperature": 0,
				"avg_logprob": -0.37133017708273497,
				"compression_ratio": 0.9344262295081968,
				"no_speech_prob": 0.04418903589248657
			}
		],
		"language": "en"
	}
}
```

