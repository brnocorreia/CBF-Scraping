import os
import requests
from dotenv import load_dotenv

load_dotenv()

PDF_FOLDER_PATH = os.getenv("PDF_FOLDER_PATH")


def download_pdf_file(url: str) -> bool:
    """Download PDF from given URL to local directory.

    :param url: The url of the PDF file to be downloaded
    :return: True if PDF file was successfully downloaded, otherwise False.
    """

    # Request URL and get response object
    response = requests.get(url, stream=True)

    # isolate PDF filename from URL
    pdf_file_name = ("jogo_" + os.path.basename(url)[3:]).replace("b","")
    if response.status_code == 200:
        # Save in PDF_FOLDER_PATH
        path = PDF_FOLDER_PATH
        filepath = os.path.join(path, pdf_file_name)
        with open(filepath, 'wb') as pdf_object:
            pdf_object.write(response.content)
            print(f'{pdf_file_name} was successfully saved!')
            pdf_object.close()
            return True
    else:
        print(f'Uh oh! Could not download {pdf_file_name},')
        print(f'HTTP response status code: {response.status_code}')
        return False

