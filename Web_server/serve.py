from genericpath import isfile
from msilib.schema import File
from flask import Flask, render_template, safe_join, abort, send_file
import os
import datetime as dt
from pathlib import Path

# create a server
app = Flask(__name__)

baseFolderPath = r'C:\Users\Aldo Hadid\Downloads\drive-download-20221005T124356Z-001'

@app.route('/')
def index():
    return "Hello World"

def getTimeStampString(tSec: float) -> str:
    tObj = dt.datetime.fromtimestamp(tSec)
    tStr = dt.datetime.strftime(tObj, '%Y-%m-%d %H:%M:%S')
    return tStr

def getReadableByteSize(num, suffix='B') -> str:
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

@app.route('/reports/', defaults = {'reqPath':""})
@app.route('/reports/<path:reqPath>')
def reports(reqPath):
    absPath = safe_join(baseFolderPath, reqPath)

    if not os.path.exists(absPath):
        return abort(404)

    if os.path.isfile(absPath):
        return send_file(absPath)

    def fObjFromScan(x):
        fileStat = x.stat()
        fBytes = getReadableByteSize(fileStat.st_size)
        fTime = getTimeStampString(fileStat.st_mtime)
        return {
                'name': x.name, 
                'size': fBytes, 
                'mTime': fTime,
                'fLink': os.path.relpath(x.path, baseFolderPath)
                }
    fNames = [fObjFromScan(x) for x in os.scandir(absPath)]
    return render_template('files.html.j2', files=fNames)

# run the server
app.run(host="0.0.0.0", port=50100, debug=True)

