import os
import subprocess
import shutil
import platform

class FileHandlingError(Exception):
    """Custom exception raised for file handling issues."""
    pass

class ConversionError(Exception):
    """Custom exception raised for conversion errors."""
    pass

class LibreOfficeNotFoundError(Exception):
    """Custom exception raised when LibreOffice is not found."""
    pass

class PPTXConverter:
    def __init__(self):
        self.libreoffice_path = self._find_libreoffice_path()

    def _find_libreoffice_path(self):
        """Find the path to LibreOffice based on the operating system."""
        if platform.system() == "Windows":
            paths = [
                r"C:\Program Files\LibreOffice\program\soffice.exe",
                r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"
            ]
        elif platform.system() == "Linux":
            paths = ["/usr/bin/libreoffice", "/usr/local/bin/libreoffice"]
        else:
            raise LibreOfficeNotFoundError("Unsupported operating system")

        for path in paths:
            if os.path.isfile(path):
                return path
        raise LibreOfficeNotFoundError("LibreOffice executable not found")

    def convert_pptx_to_images(self, pptx_file, output_folder):
        """Convert a PPTX file to images, saving them in the specified output folder."""
        if not os.path.isfile(pptx_file):
            raise FileNotFoundError(f"The file {pptx_file} does not exist.")

        try:
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
        except OSError as e:
            raise FileHandlingError(f"Failed to create output directory: {e}")

        pptx_name = os.path.splitext(os.path.basename(pptx_file))[0]
        temp_output_dir = os.path.join(output_folder, "temp_conversion")
        if not os.path.exists(temp_output_dir):
            os.makedirs(temp_output_dir)

        command = [
            self.libreoffice_path,
            "--headless",
            "--convert-to", "png",
            "--outdir", temp_output_dir,
            pptx_file
        ]

        try:
            subprocess.run(command, check=True)
            self._rename_and_move_images(temp_output_dir, output_folder, pptx_name)
        except subprocess.CalledProcessError as e:
            raise ConversionError(f"LibreOffice conversion failed: {e}")
        finally:
            self._cleanup_temp_dir(temp_output_dir)

    def _rename_and_move_images(self, temp_dir, output_dir, pptx_name):
        """Rename and move images from the temporary directory to the final output folder."""
        try:
            files = sorted(os.listdir(temp_dir))
            for idx, file_name in enumerate(files):
                if file_name.endswith(".png"):
                    new_name = f"{pptx_name}_slide_{idx + 1}.png"
                    src = os.path.join(temp_dir, file_name)
                    dst = os.path.join(output_dir, new_name)
                    shutil.move(src, dst)
        except (OSError, IOError) as e:
            raise FileHandlingError(f"Error handling files: {e}")

    def _cleanup_temp_dir(self, temp_dir):
        """Remove the temporary directory and its contents."""
        try:
            shutil.rmtree(temp_dir)
        except OSError as e:
            raise FileHandlingError(f"Failed to remove temporary directory: {e}")

