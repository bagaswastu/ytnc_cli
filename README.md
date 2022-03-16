# Youtube Nightcore CLI (ytnc)
ytnc is a CLI application for downloading YouTube videos, converting them into nightcore music, and playing it to your default audio player.

You can also use it to convert into a slowed-reverb type of music by adding `--speed` option to `0.9`.

You need to have FFmpeg installed on your system to use this application.

[Download ytnc (windows only)](https://github.com/bagaswastu/ytnc_cli/releases)

```
$ ytnc --help
Usage: ytnc.exe [OPTIONS] YOUTUBE_URL

Options:
  -s, --speed TEXT           Change speed of audio. (default: 1.25)
  -dap, --disable-auto-play  Don't play the music after download & convert.
  -o, --output PATH          Output path for the file.
  -fp, --ffmpeg-path TEXT    Path to FFmpeg
  --help                     Show this message and exit.
```

## How it works
The application will find & download the video using `youtube-dl`, and then the app will download the `.mp3` file and filter it using [FFmpeg](https://github.com/FFmpeg/FFmpeg).

## Run the project
- Clone this repository
- Go to src folder by typing 
  ```bash
  $ cd src
  ```
- Install required dependencies by 
  ```bash
  $ pip install -r requirements.txt
  ```
- And then run the app 
  ```bash
  $ python ytnc.py
  ```