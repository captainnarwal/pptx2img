import unittest
import os
import stat
from pptx2img import PPTXConverter, FileHandlingError, ConversionError, LibreOfficeNotFoundError

class TestPPTXConverter(unittest.TestCase):

    def setUp(self):
        """Set up test environment."""
        self.converter = PPTXConverter()
        self.test_pptx_file = "test_presentation.pptx"
        self.output_folder = "test_output"

        # Create a dummy PPTX file for testing
        self._create_dummy_pptx(self.test_pptx_file)

    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.test_pptx_file):
            os.remove(self.test_pptx_file)
        if os.path.exists(self.output_folder):
            # Attempt to remove files and folder
            for file in os.listdir(self.output_folder):
                file_path = os.path.join(self.output_folder, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
            try:
                os.rmdir(self.output_folder)
            except OSError:
                pass  # Directory might not be empty or in use

    def _create_dummy_pptx(self, file_path):
        """Create a dummy PPTX file."""
        with open(file_path, "wb") as f:
            f.write(b"dummy PPTX content")

    def test_convert_pptx_to_images_success(self):
        """Test successful conversion of PPTX to images."""
        try:
            self.converter.convert_pptx_to_images(self.test_pptx_file, self.output_folder)
            # Check if the output folder contains files
            files = os.listdir(self.output_folder)
            self.assertGreater(len(files), 0, "No files were created in the output folder.")
            # Check if files have the correct naming pattern
            for file_name in files:
                self.assertTrue(file_name.startswith("test_presentation_slide_"), f"Unexpected file name: {file_name}")
                self.assertTrue(file_name.endswith(".png"), f"Unexpected file extension: {file_name}")
        except Exception as e:
            self.fail(f"Conversion failed with error: {e}")

    def test_convert_pptx_file_not_found(self):
        """Test conversion with a non-existent PPTX file."""
        with self.assertRaises(FileNotFoundError):
            self.converter.convert_pptx_to_images("non_existent_file.pptx", self.output_folder)

    def test_output_folder_creation_error(self):
        """Test conversion when output folder cannot be created."""
        # Simulate a permissions error by setting the folder to read-only
        try:
            os.mkdir(self.output_folder)
            # Change folder permissions to read-only
            os.chmod(self.output_folder, stat.S_IREAD)
            with self.assertRaises(FileHandlingError):
                self.converter.convert_pptx_to_images(self.test_pptx_file, self.output_folder)
        finally:
            # Restore permissions and clean up
            os.chmod(self.output_folder, stat.S_IWRITE)
            if os.path.exists(self.output_folder):
                for file in os.listdir(self.output_folder):
                    file_path = os.path.join(self.output_folder, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                os.rmdir(self.output_folder)

if __name__ == "__main__":
    unittest.main()
