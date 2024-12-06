import json

def saveAsJson(output_file, data):
    with open(output_file, "w") as f:
        json.dump(data, f)