import openai
import json 
import os
import sys

def transcript(file_name):
    audio_file = open(file_name, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    json_str = json.dumps(transcript)
    json_file = os.path.splitext(file_name)[0] + ".json"
    with open(json_file, "w") as outfile:
       outfile.write(json_str)

def main():
    args = sys.argv[1:]
    for file_name in args:
        transcript(file_name)

if __name__ == '__main__':
    main()
