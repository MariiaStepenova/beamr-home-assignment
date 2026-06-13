import pytest_check

from config.settings import (
    DOWNLOAD_DIR,
    DOWNLOADED_ARCHIVE_FILE_NAME,
    OUTPUT_FILE_EXTENSION,
    TEST_DATA_DIR,
)
from utils.file_utils import extract_archive, parse_size_to_bytes, wait_for_download


TEST_FILE = TEST_DATA_DIR / "IMG_8028.heic"


def test_heic_file_is_converted_to_smaller_jpg(home_page):
    original_size_bytes = TEST_FILE.stat().st_size

    home_page.open()
    home_page.upload_file_by_drag_and_drop(TEST_FILE)
    home_page.wait_for_conversion_result(TEST_FILE)

    compressed_size_text = home_page.get_compressed_file_size_text(TEST_FILE)
    compressed_size_bytes = parse_size_to_bytes(compressed_size_text)

    reduction_percent = ((original_size_bytes - compressed_size_bytes) / original_size_bytes) * 100
    print(f"Compression reduced file size by {reduction_percent:.2f}%")

    pytest_check.less(
        compressed_size_bytes,
        original_size_bytes,
        "Compressed file size displayed on the page should be smaller than the original file size.",
    )

    home_page.click_download_all_button()

    downloaded_archive = wait_for_download(DOWNLOADED_ARCHIVE_FILE_NAME, DOWNLOAD_DIR)
    converted_files = extract_archive(downloaded_archive, DOWNLOAD_DIR)
    converted_file = converted_files[0]

    pytest_check.equal(
        converted_file.suffix.lower(),
        OUTPUT_FILE_EXTENSION,
        f"Converted file extension should be {OUTPUT_FILE_EXTENSION}.",
    )

    converted_file_size_bytes = converted_file.stat().st_size

    pytest_check.less(
        converted_file_size_bytes,
        original_size_bytes,
        "Downloaded compressed file should be smaller than the original file.",
    )