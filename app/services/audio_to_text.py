import json 
import os
import sys
import logging
import hashlib

from openai import OpenAI
from app.db import transcript_repo

def audio_to_text(file_name, audio_stream):
    """
    Args:
        audio_stream: stream of the audio

    Returns:
        string: The transcript of the audio
    """
    client = OpenAI()
    logger = logging.getLogger()
    audio_hash = compute_checksum(audio_stream)
    logger.info("sha256 is {}".format(audio_hash))
    transcript, found = transcript_repo.find(audio_hash)
    if not found:
        logger.info("transcript not found, calling whisper model")
        transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_stream)
        #json_str = json.dumps(transcript.text, ensure_ascii=False)
        #transcript_repo.insert(file_name, json_str, audio_hash)
        transcript_repo.insert(file_name, transcript.text, audio_hash)
        #return json_str
        return transcript.text

    #json_str = json.dumps(transcript, ensure_ascii=False)
    #return json_str
    return transcript

def compute_checksum(data):
    hash_object = hashlib.sha256()

    # Read data from BytesIO object in chunks and update the hash object
    data.seek(0)  # Move the file pointer to the beginning of the BytesIO object
    chunk_size = 4096  # Adjust chunk size as needed
    while True:
        chunk = data.read(chunk_size)
        if not chunk:
            break
        hash_object.update(chunk)

    # Return the hexadecimal representation of the computed checksum
    return hash_object.hexdigest()
