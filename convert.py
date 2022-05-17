# importing necessary libraries
import img2pdf
import os
import sys
from PIL import Image
from PyPDF2 import PdfFileMerger
  

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Remember to pass the directory of the images")
    elif os.path.exists(sys.argv[1]):
        # Read files
        folder = sys.argv[1]
        files = os.listdir(folder)
        pdfs = []
        for file in files:
            if os.path.isfile(os.path.join(folder, file)):
                img_path = "{}/{}".format(folder, file)
                pdf_path = "{}.pdf".format(file)
                with Image.open(img_path) as image:
                    pdf_bytes = img2pdf.convert(image.filename)
                    with open(pdf_path, "wb") as f:
                        f.write(pdf_bytes)
                        print("Successfully made pdf file", img_path)
                        pdfs.append(pdf_path)
        
        # Merge
        merger = PdfFileMerger()
        try:
            for pdf in pdfs:
                merger.append(pdf)
            merger.write("Final result.pdf")
        except Exception as err:
            print(err)
        finally:
            merger.close()
