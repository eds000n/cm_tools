#!/usr/bin/python

from openai import OpenAI
import json 
import os
import sys

def transcript(file_name):
    audio_file = open(file_name, "rb")
    #transcript = openai.Audio.transcribe("whisper-1", audio_file)
    client = OpenAI()
    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    text = json.dumps(transcript.text, ensure_ascii=False)
    txt_file = os.path.splitext(file_name)[0] + ".txt"
    with open(txt_file, "w", encoding='utf8') as outfile:
       outfile.write(text)

def main():
    args = sys.argv[1:]
    for file_name in args:
        transcript(file_name)

if __name__ == '__main__':
    main()
