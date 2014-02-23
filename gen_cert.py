#!/usr/bin/python
#
# gen_cert.py v1.2 written by Ish Sookun <http://hacklog.in/about>
# PDF 
# For details about this project please visit http://hacklog.in/peg.
#
# This work is licensed under a Creative Commons Attribution 3.0 Unported License.
# License details at http://creativecommons.org/licenses/by/3.0.
#

from pyPdf import PdfFileWriter, PdfFileReader
import StringIO
import os
import sys
import base64
import haslib
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import PCMYKColor
from reportlab.pdfbase.pdfmetrics import stringWidth

#page_width = defaultPageSize[0]
#page_height = defaultPageSize[1]
packet = StringIO.StringIO()
# Create a new PDF with reportlab
attendee = sys.argv[1]
# Creating a certificate hash code
hasher = hashlib.md5(attendee)
certID = base64.urlsafe_b64encode(hasher.digest()[0:5])
# attendee_width = stringWidth(attendee, "Times-Roman", 30)
gold = PCMYKColor(26,23,45,11)
can = canvas.Canvas(packet, pagesize=letter)
can.setFillColor(gold)
can.setFont("Times-Roman", 50)
# Specify the x,y coordinate for attendee name
can.drawCentredString(420, 225, attendee, mode=None)
# Specify Font size & coordinates for certificate number
black = PCMYKColor(0,0,0,61)
can.setFillColor(black)
can.setFont("Courier", 8)
can.drawString(668, 75, "Cert ID: 13-"+certID, mode=None)
can.save()

# Move to the beginning of the StringIO buffer
packet.seek(0)
new_pdf = PdfFileReader(packet)

# Read existing PDF
existing_pdf = PdfFileReader(file("New.pdf", "rb"))
output = PdfFileWriter()

# Add new PDF
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)

# Write merged content to PDF
outputStream = file(attendee + ".pdf", "wb")
output.write(outputStream)
outputStream.close()

if os.path.isfile(attendee + ".pdf"):
    print attendee + ".pdf created"
else:
    print "Error encountered while creating " + attendee + ".pdf"
