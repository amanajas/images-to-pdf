# importing necessary libraries
import os
import sys
from PIL import Image
from PyPDF2 import PdfFileMerger


DEFAULT_OUTPUT_FILE = "result.pdf"
DEFAULT_OUTPUT_FOLDER = "output"


def generate_pdf_from_image(path_to_images):
    # Read files
    print("Path to convert:", path_to_images)
    files = os.listdir(path_to_images)
    pdfs = []
    if len(files) > 0:
        # Creating output folder
        if not os.path.exists(DEFAULT_OUTPUT_FOLDER):
            os.mkdir(DEFAULT_OUTPUT_FOLDER)
        for file in files:
            if os.path.isfile(os.path.join(path_to_images, file)):
                img_path = "{}/{}".format(path_to_images, file)
                pdf_path = "{}/{}.pdf".format(DEFAULT_OUTPUT_FOLDER, file)
                with Image.open(img_path) as image:
                    image.save(pdf_path)
                    pdfs.append(pdf_path)
                    print("Successfully made pdf file out of", img_path, "named", pdf_path)
    return pdfs


def merge_pdfs(pdfs, file_name):
    # Merge
    merger = PdfFileMerger()
    print("Merging...")
    for pdf in pdfs:
        merger.append(pdf)
    print("Creating final PDF", file_name)
    merger.write(file_name)
    merger.close()
    print("Removing old generated PDFs...")
    for pdf in pdfs:
        os.remove(pdf)
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
                opt_filename = "{}/{}".format(DEFAULT_OUTPUT_FOLDER, DEFAULT_OUTPUT_FILE)
            else:
                opt_filename = "{}/{}".format(DEFAULT_OUTPUT_FOLDER, opt_filename)
            # Searching images and converting to individual PDFs
            generated_pdfs = generate_pdf_from_image(folder)
            # Check if there are PDFs to merge
            if len(generated_pdfs) == 0:
                print("There is nothing to merge")
            else:
                # Merging PDFs
                print("PDF amount", len(generated_pdfs))
                merge_pdfs(generated_pdfs, opt_filename)
