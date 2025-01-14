from pdf2image import convert_from_path
from pdf2image.exceptions import (
PDFInfoNotInstalledError,
PDFPageCountError,
PDFSyntaxError
)
import os

file_path = ''
fileName = os.path.basename(file_path)
print(fileName)
dirName = os.path.dirname(file_path)
print(dirName)
dirStr, ext = os.path.splitext(file_path)
file = dirStr.split("\\")[-1]
print(file)
images = convert_from_path(file_path,
            fmt = "png",
            output_folder=dirName
            )