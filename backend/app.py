#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @FileName  :app.py
# @Time      :2023/1/7 17:02
# @Author    :lovemefan
# @email     :lovemefan@outlook.com

from sanic import Sanic, Request
from sanic.exceptions import RequestTimeout, NotFound
from sanic.response import json, HTTPResponse
import os

from backend.exception.SpeechException import MissParameters
from backend.model.ResponseBody import ResponseBody
from backend.route.RecognitionRoute import recognition_route

from backend.utils.StatusCode import StatusCode

app = Sanic("whisper-webserver")


@app.exception(RequestTimeout)
async def timeout(request, exception):
    response = {
        "reasons": ['Request Timeout'],
        "exception": StatusCode.REQUEST_TIMEOUT.name
    }
    return json(response, 408)


@app.exception(NotFound)
async def notfound(request, exception):
    response = {
        "reasons": [f'Requested URL {request.url} not found'],
        "exception": StatusCode.NOT_FOUND.name
    }

    return json(response, 404)


@app.exception(MissParameters)
async def notfound(request, exception):
    response = {
        "reasons": [str(exception)],
        "exception": StatusCode.MISSPARAMETERS.name
    }

    return json(response, 404)



app.blueprint(recognition_route)

if __name__ == '__main__':
    port = 8888
    # if env $port is none ,get the config port or default port
    port = os.environ.get('PORT', port)
    app.run(host="0.0.0.0", port=port)