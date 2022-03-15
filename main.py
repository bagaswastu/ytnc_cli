import subprocess
import click
import os, tempfile
import youtube_dl

AUDIO_SAMPLE_RATE = 44100
FILE_FORMAT = "mp3"


def process(speed: float, output_path: str, youtube_url: str, ffmpeg_path: str):

    dl_opts = {
        "format": "bestaudio[asr=%d]" % AUDIO_SAMPLE_RATE,
        "audioformat": FILE_FORMAT,
        "noplaylist": True,
        "quiet": True,
    }

    music_url = ""
    with youtube_dl.YoutubeDL(dl_opts) as ytdl:
        click.secho("Getting info...\n", fg="yellow")
        info = ytdl.extract_info(youtube_url, download=False)
        music_url = info["formats"][0]["url"]
        music_title = info["title"]
        music_uploader = info["uploader"]
        total_size = info["filesize"]

        # Convert total size to MB
        total_size = round(total_size / (1024 * 1024), 2)

        click.echo(f"Title\t\t: " + click.style(music_title, fg="magenta"))
        click.echo(f"Uploader\t: " + click.style(music_uploader, fg="magenta"))
        click.echo(f"Size\t\t: " + click.style(f"{total_size} MB", fg="magenta"))

    click.secho("\nDownload & converting...\n", fg="yellow")
    ffmpeg_command = [
        ffmpeg_path,
        "-y",  # Always overwrite
        "-i",
        music_url,
        "-filter:a",
        f"asetrate=44100*{speed},aresample=44100",  # Increase sample rate and resample at original rate
        output_path,
    ]

    command_output = subprocess.run(ffmpeg_command, stderr=subprocess.PIPE)

    # check error
    if command_output.returncode != 0:
        click.secho("Error: " + command_output.stderr.decode("utf-8"), fg="red")

    click.secho("\nCompleted!", fg="yellow")


def ffmpeg_error():
    click.secho(
        "ERROR, either you don't have FFmpeg installed or your FFmpeg path is wrong.\n",
        fg="red",
    )
    click.echo(
        "You need to download FFmpeg and then add to your path in order to use this tool."
    )
    click.echo("https://www.ffmpeg.org/download.html\n")
    click.echo(
        "Or, if you have FFmpeg already installed, you can set the path using --ffmpeg-path option."
    )


@click.command()
@click.argument("youtube_url")
@click.option(
    "--speed", "-s", default="1.25", help="Change speed of audio. (default: 1.25)"
)
@click.option(
    "--disable-auto-play",
    "-dap",
    is_flag=True,
    help="Don't play the music after download & convert.",
)
@click.option(
    "--output", "-o", help="Output path for the file.", type=click.Path(exists=True)
)
@click.option("--ffmpeg-path", "-fp", help="Path to FFmpeg")
def main(speed, output, youtube_url, disable_auto_play, ffmpeg_path):
    # Convert speed to float
    try:
        speed = float(speed)
    except ValueError:
        click.echo("Speed must be a number.")
        return

    # Using temp file as path if no output path is provided
    if not output:
        output = os.path.join(
            tempfile.gettempdir(), f"{os.urandom(24).hex()}.{FILE_FORMAT}"
        )

    # Check if ffmpeg is available in current path
    if not ffmpeg_path:
        ffmpeg_path = "ffmpeg"

    try:
        subprocess.call([ffmpeg_path, "-version"], stdout=subprocess.DEVNULL)
    except FileNotFoundError:
        ffmpeg_error()
        return

    # Validation youtube url
    if "youtube.com/watch?v=" not in youtube_url:
        click.echo("Invalid youtube url!")
        return

    # Processing the request
    process(speed, output, youtube_url, ffmpeg_path)

    # Completed state
    if not disable_auto_play:
        click.secho("Playing the music...\n", fg="yellow")
        click.launch(output)
        click.secho(f"Output File: {output}", fg="green")
    else:
        click.secho(f"Output file: {output}")


if __name__ == "__main__":
    main()
