#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @FileName  :RecognitionRoute.py
# @Time      :2023/1/7 22:18
# @Author    :lovemefan
# @email     :lovemefan@outlook.com

from sanic import Blueprint
from sanic.response import json

from backend.exception.SpeechException import SpeechSampleRateException, MissParameters
from backend.model.ResponseBody import ResponseBody
from backend.service.WhisperAsrService import WhisperAsrService

from whisper import tokenizer
from backend.utils.StatusCode import StatusCode

recognition_route = Blueprint('speech', url_prefix='/api/speech', version=1)
recongnitionService = WhisperAsrService()
LANGUAGE_CODES = sorted(list(tokenizer.LANGUAGES.keys()))


@recognition_route.exception(SpeechSampleRateException)
async def speech_sample_rate_exception(request, exception):
    response = {
        "reasons": [str(exception)],
        "exception": StatusCode.SAMPLE_RATE_ERROR.name
    }
    return json(response, 408)


@recognition_route.post('/recognition')
async def recognition(request):
    audio_file = request.files.get('audio', None)
    language = request.form.get('language', None)
    task = request.form.get('task', 'transcribe')

    if language is not None:
        if language not in LANGUAGE_CODES:
            raise MissParameters(f'language parameter {language} is not supported')

    if task not in ['transcribe', 'translate']:
        raise MissParameters(f'task parameter {language} is not supported')

    if not audio_file:
        raise MissParameters('audio is empty')

    result = recongnitionService.transcribe(audio_file, task, language)
    return json(
        ResponseBody(message=f'Success',
                     data=result).__dict__,
        200)


@recognition_route.post('/detect_language')
async def segment(request):
    audio_file = request.files.get('audio', None)

    if not audio_file:
        raise MissParameters('audio is missing')

    result = recongnitionService.language_detection(audio_file)
    return json(
        ResponseBody(message=f'Success',
                     data=result).__dict__,
        200)
