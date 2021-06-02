import json


def read_json_stream(file):
    buffer = ""
    line = file.readline()
    if line:
        buffer += line + "\r\n"
    else:
        # Empty line means start of new object
        yield json.loads(buffer)
        buffer = ""
