# Selenium Task

Automated UI test for HEIC to JPG conversion using Selenium WebDriver and Page Object Model (POM).

## Requirements

- Python 3.10+
- Google Chrome
- ChromeDriver compatible with the installed Chrome version

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

## Test Data

The test uses the sample HEIC image located at:

```text
test_data/IMG_8028.HEIC
```

## Running Tests

Run all tests:

```bash
pytest
```

Run a specific test:

```bash
pytest tests/test_heic_compression.py
```

## Test Scenario

The automated test performs the following steps:

1. Navigate to the Heic2Jpeg homepage (https://heictojpg.com/)
2. Use the drag-and-drop mechanism to upload the selected file into the drop zone and
initiate optimization
3. Wait until the file compression completes
4. Assert on the web page that the compressed file size is smaller than the original, and
note the reduction
5. Click the Download button
6. Wait for the file to download
7. Compare the reference and compressed file sizes to verify that the compressed file is
smaller and that extension is JPG.
