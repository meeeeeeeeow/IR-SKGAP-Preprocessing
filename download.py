from urllib.request import Request, urlopen
from PyPDF2 import PdfFileWriter, PdfFileReader
import io

url = "https://openaccess.thecvf.com/content/CVPR2021/papers/Reddy_Im2Vec_Synthesizing_Vector_Graphics_Without_Vector_Supervision_CVPR_2021_paper.pdf"
writer = PdfFileWriter()

remoteFile = urlopen(Request(url)).read()
memoryFile = io.BytesIO(remoteFile)
pdfFile = PdfFileReader(memoryFile)


for pageNum in range(pdfFile.getNumPages()):
    currentPage = pdfFile.getPage(pageNum)
    #currentPage.mergePage(watermark.getPage(0))
    writer.addPage(currentPage)


outputStream = open("output.pdf","wb")
writer.write(outputStream)
outputStream.close()