import base64
import json
import os

def main():
    config_arg = os.getenv("MESSAGE")
    print("input = " + config_arg)

    fullMessage = json.loads(config_arg)
    print("data = " + fullMessage["data"])

    decoded = base64.b64decode(fullMessage["data"]).decode('utf-8')
    jsonObj = json.loads(decoded)
    fileName = jsonObj["body"]['sourceFile']
    print("filename = " + fileName)

    os.makedirs('tmp')
    text_file = open("/tmp/sourceFileName.txt", "w+")
    n = text_file.write(fileName)
    text_file.close()

    savedfile = open("/tmp/sourceFileName.txt", "r")
    contents = savedfile.read()
    print("FileContents = " + contents)
    savedfile.close()

