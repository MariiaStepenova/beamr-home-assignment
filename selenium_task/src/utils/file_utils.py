import shutil
import time
from pathlib import Path
from zipfile import ZipFile

from config.settings import DEFAULT_TIMEOUT, SIZE_MULTIPLIERS


def clean_directory(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)

    for item in directory.iterdir():
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)


def parse_size_to_bytes(size_text: str) -> int:
    value, unit = size_text.strip().split()

    value = float(value)
    unit = unit.upper()

    if unit not in SIZE_MULTIPLIERS:
        raise ValueError(f"Unsupported size unit: {unit}")

    return int(value * SIZE_MULTIPLIERS[unit])


def wait_for_download(file_name: str, download_dir: Path, timeout: int = DEFAULT_TIMEOUT) -> Path:
    downloaded_file = download_dir / file_name
    end_time = time.time() + timeout

    while time.time() < end_time:
        if downloaded_file.exists() and downloaded_file.stat().st_size > 0:
            return downloaded_file

        time.sleep(0.5)

    raise TimeoutError(f"File '{file_name}' was not downloaded within {timeout} seconds.")


def extract_archive(archive_path: Path, extract_dir: Path) -> list[Path]:
    extract_dir.mkdir(parents=True, exist_ok=True)

    with ZipFile(archive_path, "r") as archive:
        extracted_names = archive.namelist()
        archive.extractall(extract_dir)

    if not extracted_names:
        raise FileNotFoundError(f"No files were extracted from '{archive_path.name}'.")

    return [extract_dir / file_name for file_name in extracted_names]