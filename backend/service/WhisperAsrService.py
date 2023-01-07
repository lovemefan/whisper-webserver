#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @FileName  :WhisperAsrService.py
# @Time      :2023/1/7 17:01
# @Author    :lovemefan
# @email     :lovemefan@outlook.com
from typing import Union

from backend.decorator.singleton import singleton
import os
import torch
import whisper
from sanic.request import File
import numpy as np
from whisper import tokenizer

from backend.utils.AudioHelper import AudioReader
from backend.utils.logger import logger


@singleton
class WhisperAsrService:
    def __init__(self):
        model_name = os.getenv("ASR_MODEL", "base")
        logger.info(f'loading {model_name} model ')
        if torch.cuda.is_available():
            self.model = whisper.load_model(model_name).cuda()
        else:
            self.model = whisper.load_model(model_name)
        logger.info(f'loading {model_name} model finished')

    def transcribe(self, audio: Union[np.ndarray, File], task: Union[str, None], language: Union[str, None]):
        options_dict = {"task": task}
        if language:
            options_dict["language"] = language

        if isinstance(audio, File):
            audio, curr_sample_rate = AudioReader.read_pcm16(audio.body)
        result = self.model.transcribe(audio.astype(np.float32) / 32768.0, **options_dict)

        return result

    def language_detection(self, audio: Union[np.ndarray, File]):

        if isinstance(audio, File):
            audio, curr_sample_rate = AudioReader.read_pcm16(audio.body)

        audio = whisper.pad_or_trim(audio.astype(np.float32) / 32768.0)

        # make log-Mel spectrogram and move to the same device as the model
        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)

        # detect the spoken language
        _, probs = self.model.detect_language(mel)
        detected_lang_code = max(probs, key=probs.get)

        result = {"detected_language": tokenizer.LANGUAGES[detected_lang_code],
                  "langauge_code": detected_lang_code}

        return result
