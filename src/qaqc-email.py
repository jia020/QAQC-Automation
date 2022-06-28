import smtplib

gmail_user = 'cg-admin@csiro.au'
gmail_password = 'abc'

sent_from = gmail_user
to = ['Lingbo.Jiang@csiro.au']
subject = 'OMG Super Important Message'
body = 'Hey, what is up?\n\n- You'

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

try:
    print('1')
    server = smtplib.SMTP('smtp-relay.csiro.au',25)	
    server.ehlo()
    print('2')
    #ret = server.login(gmail_user, gmail_password)
    print('3')
    server.sendmail(sent_from, to, email_text)
    server.close()

    print('Email sent!')
except BaseException as err:
    print(f"Unexpected {err=}, {type(err)=}")
