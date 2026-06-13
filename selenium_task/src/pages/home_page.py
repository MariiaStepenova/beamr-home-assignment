from pathlib import Path

from selenium.webdriver.common.by import By

from config.settings import OUTPUT_FILE_EXTENSION, SIZE_MULTIPLIERS
from pages.base_page import BasePage


class HomePage(BasePage):
    PATH = "/"

    DOWNLOAD_ALL_BUTTON = (By.ID, "download-all-button")
    DROP_ZONE = (By.CSS_SELECTOR, ".dropzone")
    RESULT_CARD_BY_FILE_NAME = "//a[contains(@class, 'upload-box')][contains(., '{file_name}')]"

    def upload_file_by_drag_and_drop(self, file_path):
        self._wait_for_visible(self.DROP_ZONE)
        self._drag_and_drop_file(file_path)

    def wait_for_conversion_result(self, source_file_path):
        self._wait_for_visible((By.XPATH, self.RESULT_CARD_BY_FILE_NAME.format(
            file_name=self._get_output_file_name(source_file_path)
        )))

    def get_compressed_file_size_text(self, source_file_path):
        result_card = self._wait_for_visible((By.XPATH, self.RESULT_CARD_BY_FILE_NAME.format(
            file_name=self._get_output_file_name(source_file_path)
        )))

        for line in result_card.text.splitlines():
            if any(unit in line for unit in SIZE_MULTIPLIERS):
                return line

        raise ValueError(f"Could not find file size in result card: {result_card.text}")

    def click_download_all_button(self):
        self._wait_for_clickable(self.DOWNLOAD_ALL_BUTTON).click()

    @staticmethod
    def _get_output_file_name(source_file_path):
        return Path(source_file_path).stem + OUTPUT_FILE_EXTENSION

    def _drag_and_drop_file(self, file_path):
        file_path = Path(file_path).resolve()

        input_element = self.driver.execute_script("""
            const input = document.createElement('input');
            input.type = 'file';
            input.style.display = 'none';

            input.addEventListener('change', () => {
                const file = input.files[0];

                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);

                const dropZone = document.querySelector('.dropzone');

                ['dragenter', 'dragover', 'drop'].forEach(eventName => {
                    dropZone.dispatchEvent(
                        new DragEvent(eventName, {
                            bubbles: true,
                            cancelable: true,
                            dataTransfer: dataTransfer
                        })
                    );
                });
            });

            document.body.appendChild(input);
            return input;
        """)

        input_element.send_keys(str(file_path))