# pptx2img

`pptx2img` is a Python library that converts PowerPoint (.pptx) files into image files (.png) using LibreOffice.

## Installation

To install `pptx2img`, use pip:

```bash
pip install pptx2img
```


## Usage
Here's an example of how to use the PPTXConverter class:

```bash
from pptx2img import PPTXConverter

converter = PPTXConverter()
converter.convert_pptx_to_images('path_to_pptx_file.pptx', 'output_folder')

```
