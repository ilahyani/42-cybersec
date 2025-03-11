import sys
import os
from PIL import Image
from PIL.ExifTags import TAGS

supported_files = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

def scorpion():
    files = sys.argv[1:]
    files = [file for file in files if os.path.splitext(file)[1].lower() in supported_files]

    for file in files:
        if img := Image.open(file):
            print(f"Availabe Metadata for {file}")
            metadata = {
                'filename': img.filename,
                'format': img.format,
                'mode': img.mode,
                'size': img.size,
                'width': img.width,
                'height': img.height,
            }
            exifdata = img.getexif()
            for tagid in exifdata:
                tagname = TAGS.get(tagid, tagid)
                value = exifdata.get(tagid)
                metadata[tagname] = value
            for key, value in metadata.items():
                print(f"  {key}: {value}")

if __name__ == "__main__":
    scorpion()
