import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import From, To, Subject, PlainTextContent, HtmlContent, Mail
from sendgrid.helpers.mail import Attachment, FileContent, FileName, FileType, Disposition, ContentId
try:
    # Python 3
    import urllib.request as urllib
except ImportError:
    # Python 2
    import urllib2 as urllib
from bs4 import BeautifulSoup
import base64

import configparser
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
# dd/mm/YY H:M:S
datetimeOfReport = now.strftime("%d/%m/%Y %H:%M:%S")
# Read local file `config.ini`.
config = configparser.ConfigParser()
config.read('config.ini')


html_text = """
<html>
    <body>
	<h1>Statistical analysis of Testrock data</h1>
	<p>
Processing of the testrock data involved downloading the data from Cloudstor and running a TSG headless script to reimport the HyLogger data to a standard product.  This is because some node data was found to be processed with older versions of TSG.  Once the data has been standardised 3 headless scripts are run on the data to generate products.  The headless scripts produces csv files containing the wavelength extraction products.  The csvs contains information on the (1) gold-polystyrene MIR wavelength standard, (2) quartz absorption feature at 8625 nm, (3) 2160 nm kaolinite feature, from a sample on the test rock board, (4) mylar, pyrophyllite, kaolinite and talc absorption features from samples on the test rock board, and (5) rare earth absorption features from the NIR wavelength standard.  The products (2), (3) and (4) can be run on any TSG file, whereas (1) and (5) can only be run on testrocks and will only work if the standards are present in the data.
</p>
        <h1>MIR puck </h1>
		<p>
All instruments show a diurnal variation between the AM and PM measurements for the TIR.  The difference is typically less than 0.3 nm at 6245 nm.  The variation between the HyLogger3 instruments at 6245 nm is approximately 3nm, with HyLogger 3-2 and 3-6 having similar wavelengths, whereas 3-4 and 3-3 were similar between 2019 and July 2020.  Most of the HyLoggers appear to be relatively stable over the past 3 years but HyLogger 3-3 appears to have decreased by ~1.5 nm between July 2020 and July 2021 where it stabilised and has a wavelength similar to HyLogger 3-6.  HyLoggers 3-1 and 3-7 have the longest wavelength for the 6245 nm absorption at ~6250 nm, which is 3 nm longer than 3-2 and 3-6.
        </p>
		<p>    
        <font face="verdana" color="blue">
The following graph show you the result of QAQC in June, 2022.If you want to interactive with the new QAQC data, please click the graph link.
        </font></p> 
<div>
    <a href="https://plotly.com/~cg-admin/3/?share_key=Nnm4e4C0hCfO6kkcYwMALT" target="_blank" title="QAQC" style="display: block; text-align: center;">
	<img src="https://plotly.com/~cg-admin/3.png?share_key=Nnm4e4C0hCfO6kkcYwMALT" alt="QAQC" style="max-width: 100%;"   onerror="this.onerror=null;this.src='https://plotly.com/404.png';" />
	</a>
    <script data-plotly="cg-admin:3" sharekey-plotly="Nnm4e4C0hCfO6kkcYwMALT" src="https://plotly.com/embed.js" async></script>
</div>
</body>
</html>
"""
file_path = '.\\out\\20210819_MRTalltest_aux9.csv'
with open(file_path, 'rb') as f:
    data = f.read()
    f.close()
encoded = base64.b64encode(data).decode()
attachment = Attachment()
attachment.file_content = FileContent(encoded)
attachment.file_type = FileType('application/csv')
attachment.file_name = FileName('qaqc-report.csv')
attachment.disposition = Disposition('attachment')
attachment.content_id = ContentId('qaqc-report ID')

sendgrid_key = config.get('SENDGRID', 'KEY')
from_email = From(config.get('SENDGRID', 'FROM'))
to_email = To(config.get('SENDGRID', 'TO'))
subject = Subject("QAQC-Automation:Report ON:" + datetimeOfReport )

sendgrid_client = SendGridAPIClient(sendgrid_key)
html_content = HtmlContent(html_text)

soup = BeautifulSoup(html_text)
plain_text = soup.get_text()
plain_text_content = PlainTextContent( plain_text)

message = Mail(from_email, to_email, subject, plain_text_content, html_content)
message.attachment = attachment

try:
    response = sendgrid_client.send(message=message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except urllib.HTTPError as e:
    print(e.read())
    exit()