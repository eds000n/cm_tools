# Install 
usual with pip

`pip install -r requirements.txt`

## To download a video
works for youtube and facebook videos
`yt-dlp <link>`

## To extract audio
`ffmpeg -i input.mp4 -q:a 0 -map a audio_output.mp3`

## To split audio
Roughty an mp3 file takes 1MB per 1 minute of sound, OpenAI has a limit of 25MB, so we give a max of 15*60 seconds to be safe
`ffmpeg -i audio_output.mp3 -f segment -segment_time 900 -c copy audio_output%03d.mp3`

## To get the transcript
To run this, I'm assuming you have your OpenAI environment set. I prefer using environment variables like:
```
export OPENAI_KEY='my_key'
export OPENAI_API_KEY='my_key2'
export CHAT_GPT_KEY='my_key3'
```

Then, you can run: `./transcript file1.mp3 file.mp3`

be patient, it takes some time. The script will generate a set of transcripts, one json per mp3 input. 
This will generate some costs, for a couple of files of 20M I got charged 0.15 USD. Be careful, always set a limit [here](https://platform.openai.com/account/billing/limits)

## Process JSON
use jq

## To cut a video
-ss indicates the start time and -t the duration
`ffmpeg -i input.mp4 -ss 00:08:41 -t 00:00:39 -c:v copy -c:a copy clipped_output.mp4`


# http usage
uvicorn server:app --reload

curl -X POST localhost:8000/transcribe -d '{"file":"SGVsbG8gV29ybGQh"}' -H "Content-Type: application/json"
curl -v -X POST localhost:8000/transcribe -H "Content-Type: multipart/form-data" -H "accept: application/json" -F "audio_file=@test_audio.mp3"

# docker
This application is containerized in a Dockerfile
build it with
`docker build --build-arg OPENAI_API_KEY -t arguedas_app .`

then push it wherever you may need. Note that we're passing the `OPENAI_API_KEY` as a build argument and then passing it to the built image. This may not be secure, this is a temporary solution.
See docker [docs](https://docs.docker.com/reference/dockerfile/#arg)

`docker run -p 8000:8000 arguedas_app`

# Tests
There's no single test, if this project is to evolve, tests are the next thing to be added together with some linter/style checker

export ADMIN_USERNAME=admin
export ADMIN_PWD=admin
export SECRET_KEY=132kabcj34
export SALT=324m923x

docker build --build-arg OPENAI_API_KEY --build-arg ADMIN_USERNAME --build-arg=ADMIN_PWD --build-arg SALT --build-arg SECRET_KEY -t arguedas_app .

curl -X POST http://localhost:8000/login  -d username=admin -d password=admin
curl -H "Authorization: Bearer <admin_token>" -X PUT http://localhost:8000/admin/approve/user1
curl -H "Authorization: Bearer <admin_token>" -X PUT http://localhost:8000/admin/reject/user1

uvicorn app.server:app --reload
