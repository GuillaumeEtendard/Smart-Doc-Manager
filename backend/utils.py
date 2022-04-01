import datetime
import pytesseract
import os
import cv2
from pdfminer.high_level import extract_text
import docx
import docx2txt

from ml.inference import predict_from_file

root = "./"
factures_path = "./invoices"
cv_path = "./resume"

os.listdir(factures_path)


# os.path.join(factures_path,os.listdir(factures_path)[1])

def processString(string):
    content = string.split("\n")
    content = list(filter(None, content))
    content = [s.strip() for s in content]
    content = list(filter(lambda k: '\uf0b7' not in k and not k.startswith('___'), content))
    content = list(filter(None, content))
    return content


def extractPDF(path):
    PDF_read = extract_text(path)
    print(PDF_read)
    return PDF_read


def extractDocx(path):
    text = docx2txt.process(path)
    print(text)
    return text


def extractImage(path):
    test_img = cv2.imread(path)
    test_txt = pytesseract.image_to_string(test_img)
    return test_txt


file_path = os.getcwd() + "/files/"


def save_file(filename, data):
    # filename = fileobject.filename
    print(filename)
    current_time = datetime.datetime.now()
    split_file_name = os.path.splitext(
        filename
    )  # split the file name into two different path (string + extention)
    file_name_unique = str(current_time.timestamp()).replace(
        ".", ""
    )  # for realtime application you must have genertae unique name for the file
    file_extension = split_file_name[1]  # file extention
    # data = (
    #    fileobject.file._file
    # )  # Converting tempfile.SpooledTemporaryFile to io.BytesIO

    with open(os.path.join(file_path, file_name_unique + file_extension), "wb") as f:
        f.write(data)

    return f.name


async def read_and_save_file(file):
    contents = await file.read()
    file_path = save_file(file.filename, contents)
    return file_path


async def processFile(file):
    content_type = file.content_type
    content = None
    file_path = None
    if content_type in ['image/jpg', 'image/jpeg', 'image/png', 'image/webp']:
        file_path = await read_and_save_file(file)
        content = extractImage(file_path)
    elif content_type == 'application/pdf':
        file_path = await read_and_save_file(file)
        content = extractPDF(file_path)
    elif content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        file_path = await read_and_save_file(file)
        content = extractDocx(file_path)

    file_type = predict_from_file(file_path)

    if content and file_type:
        return processString(content), file_type
    else:
        return None
