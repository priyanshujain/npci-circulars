import os
from bs4 import BeautifulSoup
import http.client
import urllib.parse

BASE_URL = "www.npci.org.in"


def circular_url(circular_type: str) -> str:
    urls = {
        "circular": "/what-we-do/upi/circular",
        "cts": "/what-we-do/cts/circulars",
        "nach": "/what-we-do/nach/circulars",
        "rupay": "/what-we-do/rupay/circulars",
        "imps": "/what-we-do/imps/circulars",
        "netc-fastag": "/what-we-do/netc-fastag/circulars",
        "99": "/what-we-do/99/circulars",
        "nfs": "/what-we-do/nfs/circulars",
        "aeps": "/what-we-do/aeps/circulars",
        "bhim-aadhaar": "/what-we-do/bhim-aadhaar/circulars",
        "e-rupi": "/what-we-do/e-rupi/circulars",
        "bharat-billpay": "/what-we-do/bharat-billpay/circulars",
    }
    return urls.get(circular_type, "/what-we-do/upi/circular")


def download_circulars(circular_type: str):
    url = circular_url(circular_type)

    conn = http.client.HTTPSConnection(BASE_URL)
    payload = ""
    headers = {}
    conn.request("GET", url, payload, headers)
    response = conn.getresponse()

    if response.status == 200:
        soup = BeautifulSoup(response.read(), "html.parser")

        # Find all sections with class="pdf-item"
        pdf_items = soup.find_all("div", class_="pdf-item")

        download_folder = f"files/{circular_type}"
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        # Iterate over each pdf-item section
        for pdf_item in pdf_items:
            # Find the download link within the section
            download_link = pdf_item.find("a")

            # Check if download link exists
            if download_link:
                # Extract the URL of the PDF file
                pdf_url = download_link.get("href")

                # Download the PDF file
                pdf_filename = pdf_url.split("/")[-1]
                pdf_path = os.path.join(download_folder, pdf_filename)
                pdf_url = urllib.parse.quote(pdf_url)
                with open(pdf_path, "wb") as pdf_file:
                    conn = http.client.HTTPSConnection(BASE_URL)
                    conn.request("GET", pdf_url, payload, headers)
                    pdf_response = conn.getresponse()
                    if pdf_response.status != 200:
                        print(f"Failed to download: {pdf_filename}")
                        continue
                    pdf_file.write(pdf_response.read())

                print(f"Downloaded: {pdf_filename}")
    else:
        print("Failed to download the page")


if __name__ == "__main__":
    circular_type = "upi"

    download_circulars(circular_type)
