import argparse
import subprocess
import time
from pathlib import Path
from dataclasses import dataclass
from openpyxl import Workbook
import shutil

@dataclass
class EncodingResult:
    filename: Path
    qp: int
    encoding_time_sec: float
    encoding_fps: float
    size_bytes: int

def calculate_frame_count(input_file: Path, width: int, height: int) -> int:
    file_size = input_file.stat().st_size
    frame_size = width * height * 3 // 2

    if file_size % frame_size != 0:
        raise ValueError(
            f"{input_file} size is not divisible by frame size "
            f"for resolution {width}x{height}"
        )

    return file_size // frame_size

def parse_resolution(resolution: str) -> tuple[int, int]:
    width, height = resolution.split("x")
    return int(width), int(height)

def run_x264(input_file: Path, resolution: str, total_frames: int, qp: int, output_dir: Path) -> EncodingResult:
    output_file = output_dir / f"output_qp_{qp}.264"

    command = [
        "x264",
        "--qp", str(qp),
        "--input-res", resolution,
        "-o", str(output_file),
        str(input_file),
    ]

    start_time = time.perf_counter()
    subprocess.run(command, check=True)
    elapsed_time = time.perf_counter() - start_time

    output_size = output_file.stat().st_size
    encoding_fps = total_frames / elapsed_time

    return EncodingResult(
        filename=output_file,
        qp=qp,
        encoding_time_sec=elapsed_time,
        encoding_fps=encoding_fps,
        size_bytes=output_size
    )

def export_report(data: list[EncodingResult], filename: str = "report.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws.title = "Results"

    ws.append([
        "Encoded filename",
        "QP",
        "Time (s)",
        "FPS",
        "Encoded file size"
    ])

    for item in data:
        ws.append([
            str(item.filename),
            item.qp,
            round(item.encoding_time_sec, 3),
            round(item.encoding_fps, 3),
            item.size_bytes
        ])

    wb.save(filename)


def validate_args(args) -> None:
    if shutil.which("x264") is None:
        raise RuntimeError("x264 executable not found in PATH")

    input_file = Path(args.input)

    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    if not input_file.is_file():
        raise ValueError(f"Input path is not a file: {input_file}")

    if not (1 <= args.qp_start <= 51):
        raise ValueError("qp-start must be between 1 and 51")

    if not (1 <= args.qp_end <= 51):
        raise ValueError("qp-end must be between 1 and 51")

    if args.qp_start > args.qp_end:
        raise ValueError("qp-start must be less than or equal to qp-end")

    try:
        width, height = parse_resolution(args.resolution)

        if width <= 0 or height <= 0:
            raise ValueError("width and height must be positive")

    except ValueError:
        raise ValueError("resolution must be in widthxheight format, for example 352x288")

def main():
    try:
        parser = argparse.ArgumentParser(description="Run x264 with different QP values.")

        parser.add_argument("--input", required=True, help="Path to input .yuv file")
        parser.add_argument("--resolution", required=True, help="Input resolution, example: 352x288")
        parser.add_argument("--qp-start", type=int, default=1)
        parser.add_argument("--qp-end", type=int, default=51)
        parser.add_argument("--output-dir", default="outputs")

        args = parser.parse_args()

        validate_args(args)

        input_file = Path(args.input)
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        width, height = parse_resolution(args.resolution)
        total_frames = calculate_frame_count(input_file, width, height)

        results = []

        for qp in range(args.qp_start, args.qp_end + 1):
            print(f"Running x264 with QP={qp}...")

            result = run_x264(
                input_file=input_file,
                resolution=args.resolution,
                qp=qp,
                total_frames=total_frames,
                output_dir=output_dir,
            )

            results.append(result)

        export_report(results)
        print("Report saved to report.xlsx")

    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    except subprocess.CalledProcessError as e:
        print(f"Error: x264 failed with exit code {e.returncode}")
        sys.exit(1)

if __name__ == "__main__":
    main()
