import argparse
import subprocess
import sys
from pathlib import Path


def create_clip(
    input_file: Path,
    output_file: Path,
    start: float,
    duration: float,
    fade_in: float = 0.25,
    fade_out: float = 0.50,
    loudness: float = -16.0,
    bitrate: str = "192k",
):
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    if duration <= 0:
        raise ValueError("Duration must be greater than 0.")

    if start < 0:
        raise ValueError("Start time cannot be negative.")

    if fade_in < 0 or fade_out < 0:
        raise ValueError("Fade durations cannot be negative.")

    if fade_in + fade_out >= duration:
        raise ValueError("Fade durations must be shorter than the clip.")

    output_file.parent.mkdir(parents=True, exist_ok=True)

    fade_out_start = duration - fade_out

    audio_filter = (
    f"loudnorm=I={loudness}:TP=-1.5:LRA=11,"
    f"afade=t=in:st=0:d={fade_in},"
    f"afade=t=out:st={fade_out_start}:d={fade_out}"
)

    command = [
        "ffmpeg",
        "-y",
        "-ss",
        str(start),
        "-i",
        str(input_file),
        "-t",
        str(duration),
        "-vn",
        "-af",
        audio_filter,
        "-codec:a",
        "libmp3lame",
        "-b:a",
        bitrate,
        "-ar",
        "44100",
        "-ac",
        "2",
        str(output_file),
    ]

    print("\nCreating jingle...")
    print(f"Source:   {input_file}")
    print(f"Start:    {start:.2f}s")
    print(f"Duration: {duration:.2f}s")
    print(f"Output:   {output_file}\n")

    try:
        subprocess.run(command, check=True)
    except FileNotFoundError:
        print("ERROR: FFmpeg was not found.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: FFmpeg failed with exit code {exc.returncode}.", file=sys.stderr)
        sys.exit(exc.returncode)

    print(f"\n✓ Created {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Create a normalized Cocoon game jingle from a source audio file."
    )

    parser.add_argument("input", type=Path, help="Source audio file")
    parser.add_argument("output", type=Path, help="Output MP3 file")

    parser.add_argument(
        "--start",
        type=float,
        required=True,
        help="Starting position in seconds",
    )

    parser.add_argument(
        "--duration",
        type=float,
        default=15.0,
        help="Clip duration in seconds (default: 15)",
    )

    parser.add_argument(
        "--fade-in",
        type=float,
        default=0.25,
        help="Fade-in duration in seconds",
    )

    parser.add_argument(
        "--fade-out",
        type=float,
        default=0.50,
        help="Fade-out duration in seconds",
    )

    parser.add_argument(
        "--loudness",
        type=float,
        default=-16.0,
        help="Target integrated loudness in LUFS",
    )

    parser.add_argument(
        "--bitrate",
        default="192k",
        help="MP3 bitrate (default: 192k)",
    )

    args = parser.parse_args()

    create_clip(
        input_file=args.input,
        output_file=args.output,
        start=args.start,
        duration=args.duration,
        fade_in=args.fade_in,
        fade_out=args.fade_out,
        loudness=args.loudness,
        bitrate=args.bitrate,
    )


if __name__ == "__main__":
    main()