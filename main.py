import subprocess
import click
import os, tempfile

AUDIO_SAMPLE_RATE = 44100
FILE_FORMAT = "mp3"
output_path = ""
temp_path = os.path.join(tempfile.gettempdir(), f"{os.urandom(24).hex()}.{FILE_FORMAT}")


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
    "--disable-auto-play",
    "-dap",
    is_flag=True,
    help="Don't play the music after download & convert.",
)
@click.option(
    "--output", "-o", help="Output path for the file.", type=click.Path(exists=True)
)
@click.option("--ffmpeg-path", "-fp", help="Path to FFmpeg")
def main(output, youtube_url, disable_auto_play, ffmpeg_path):

    # Check if ffmpeg is available in current path
    if not ffmpeg_path:
        ffmpeg_path = "ffmpeg"

    try:
        subprocess.call([ffmpeg_path, "-version"], stdout=subprocess.DEVNULL)
    except FileNotFoundError:
        ffmpeg_error()
        return

    # Validation youtube url
    if "youtube.com" not in youtube_url:
        click.echo("Invalid youtube url!")
        return

    print(output)
    print(youtube_url)
    print(disable_auto_play)
    pass


if __name__ == "__main__":
    main()
