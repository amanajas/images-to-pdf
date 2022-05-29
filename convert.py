# importing necessary libraries
import os
import sys
import imghdr
from PIL import Image
from PyPDF2 import PdfFileMerger


DEFAULT_OUTPUT_FILE = "result.pdf"
DEFAULT_OUTPUT_FOLDER = "output"


def generate_pdf_from_image(path_to_images):
    # Read files
    print("Path to convert:", path_to_images)
    files = os.listdir(path_to_images)
    if len(files) > 0:
        # Creating output folder
        if not os.path.exists(DEFAULT_OUTPUT_FOLDER):
            os.mkdir(DEFAULT_OUTPUT_FOLDER)
        for file in files:
            img_path = os.path.join(path_to_images, file)
            if os.path.isfile(img_path) and imghdr.what(img_path) in ['png', 'jpeg']:
                pdf_path = "{}.pdf".format(os.path.join(DEFAULT_OUTPUT_FOLDER, file))
                with Image.open(img_path) as image:
                    image.save(pdf_path)
                    print("Successfully made pdf file out of", img_path, "named", pdf_path)
    else:
        print("-- No action required")
    print("Finishing generating")


def merge_pdfs(file_name):
    print("Merging...")
    pdfs = os.listdir(DEFAULT_OUTPUT_FOLDER)
    print("-- PDF amount", len(pdfs))
    if len(pdfs) > 0:
        # Merge
        merger = PdfFileMerger()
        for pdf in pdfs:
            merger.append(os.path.join(DEFAULT_OUTPUT_FOLDER, pdf))
        print("Creating final PDF", file_name)
        merger.write(os.path.join(DEFAULT_OUTPUT_FOLDER, file_name))
        merger.close()
        print("Removing old generated PDFs...")
        for pdf in pdfs:
            if file_name not in pdf:
                os.remove(os.path.join(DEFAULT_OUTPUT_FOLDER, pdf))
    else:
        print("-- No action required")
    print("Finished merging")
  

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Remember to pass the directory of the images and the name of the file to save them as pdf:")
        print(".e.g with opt filename: python convert.py images <final.pdf>")
    else:
        folder = sys.argv[1]
        # Checking if path exists and is valid
        if not os.path.isdir(folder):
            print("Folder of images is not valid")
        else:
            # Getting optional filename
            opt_filename = sys.argv[2] if len(sys.argv) > 2 else None
            # Checking if the name of the file is correct
            if opt_filename is None or ".pdf" not in opt_filename:
                print("Output file name incorrect or missing! Setting the default name:", DEFAULT_OUTPUT_FILE)
                opt_filename = "{}".format(DEFAULT_OUTPUT_FILE)
            # Searching images and converting to individual PDFs
            generate_pdf_from_image(folder)
            # Merging PDFs
            merge_pdfs(opt_filename)
