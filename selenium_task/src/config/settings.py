from pathlib import Path

BASE_URL = "https://heictojpg.com"

ROOT_DIR = Path(__file__).resolve().parents[2]

DOWNLOAD_DIR = ROOT_DIR / "downloads"
TEST_DATA_DIR = ROOT_DIR / "test_data"

DEFAULT_TIMEOUT = 30

OUTPUT_FILE_EXTENSION = ".jpg"
DOWNLOADED_ARCHIVE_FILE_NAME = "jpegmini_optimized.zip"

SIZE_MULTIPLIERS = {
    "KB": 1024,
    "MB": 1024 * 1024,
    "GB": 1024 * 1024 * 1024,
}
SIZE_UNITS = tuple(SIZE_MULTIPLIERS.keys())