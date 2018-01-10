import shutil

import bs4

import requests
x = requests.get("https://www.entirelypets.com")
soup = bs4.BeautifulSoup(x.content, "html.parser")
linkList = soup.find_all("a")

hrefList = []
for link in linkList:
    text = link.attrs['href']
    hrefList.append(text)

httpList = []
for href in hrefList:
    if href.startswith("http"):
        httpList.append(href)

supportedImageExt = [
"ANI",
"BMP",
"CAL",
"FAX",
"GIF",
"IMG",
"JBG",
"JPE",
"JPEG",
"JPG",
"MAC",
"PBM",
"PCD",
"PCX",
"PCT",
"PGM",
"PNG",
"PPM",
"PSD",
"RAS",
"TGA",
"TIFF",
"WMF",
"SVG",
]

while len( httpList) > 0:
    link = httpList.pop()
    print("Trying link: " + str(link))
    try:
        try:
            linkList = []
            x = requests.get(link)
            soup = bs4.BeautifulSoup(x.content, "html.parser")
            linkList = soup.find_all("a")
        except requests.exceptions.ConnectionError:
            continue

        hrefList = []
        try:
            for link in linkList:
                text = link.attrs['href']
                hrefList.append(text)
        except KeyError, requests.exceptions.ConnectionError:
            pass

        for href in hrefList:
            if href.startswith("http"):
                if href not in httpList:
                    httpList.append(href)

        picList = soup.find_all("img")

        imgList = []
        try:
            for pic in picList:
                picture = pic.attrs['src']
                if (picture.split('.')[-1]).upper() in supportedImageExt:
                    print("\tFound: " + picture)
                    imgList.append(picture)

            for img in imgList:
                fileName = img.split('/')[-1]
                imgURL = img
                if not img.startswith("http"):
                    imgURL = text + "/" + img
                if fileName != "":
                    print("Downloading: " + fileName + " from " + imgURL)
                    r = requests.get(imgURL, stream=True)
                    if r.status_code == 200:
                        with open(fileName, 'wb') as f:
                            r.raw.decode_content = True
                            shutil.copyfileobj(r.raw, f)
        except KeyError, requests.exceptions.ConnectionError:
            pass
    except requests.exceptions.MissingSchema, requests.exceptions.ConnectionError:
        pass
