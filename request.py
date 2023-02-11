import requests
import sys
import os

def downloadFile(url, fileName):
    with open(fileName, "wb") as file:
        response = requests.get(url)
        file.write(response.content)


downloadPath = './DH/'
for i in range(1,13):
    url = 'https://vn.riki.edu.vn/Online/Data/upload/files/Tailieu/N2%20Junbi/ngu-phap-nang-cao/Bai-'+ str(i) +'.pdf'
    fileName = 'DH'+ str(i) +'.pdf'     
    print('downloading file to: ' + downloadPath)
    downloadFile(url, downloadPath + fileName)
    print('file downloaded...')
    print('exiting program...')