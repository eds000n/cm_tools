# To download a video
works for youtube and facebook videos
`yt-dlp <link>`

# To extract audio
`ffmpeg -i input.mp4 -q:a 0 -map a audio_output.mp3`

# To split audio
Roughty an mp3 file takes 1MB per 1 minute of sound, OpenAI has a limit of 25MB, so we give a max of 15*60 seconds to be safe
`ffmpeg -i audio_output.mp3 -f segment -segment_time 900 -c copy audio_output%03d.mp3`

# To get the transcript
To run this, I'm assuming you have your OpenAI environment set. I prefer using environment variables like:
```
export OPENAI_KEY='my_key'
export OPENAI_API_KEY='my_key2'
export CHAT_GPT_KEY='my_key3'
```

Then, you can run: `./transcript file1.mp3 file.mp3`

be patient, it takes some time. The script will generate a set of transcripts, one json per mp3 input. 
This will generate some costs, for a couple of files of 20M I got charged 0.15 USD. Be careful, always set a limit [here](https://platform.openai.com/account/billing/limits)

# Process JSON
use jq
