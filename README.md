# encircle_whisperer
Telegram Bot that converts videos into video_notes (circles) and audio into voices

## Requirements
- Python 3.7+
- python-telegram-bot
- ffmpeg-python

## Usage
1. Create file ```.env``` with telegram bot's API token 
2. Start bot with ```python main.py```
3. In Telegram send video or audio file to your bot
4. Bot sends back circle version of video or voice message version of audio

## Notes
- Video must be shorter than 60 seconds and with exact resolution of 640x640
- Voice message waveform generated only for files smaller than 1MB
