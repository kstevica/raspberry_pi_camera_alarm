import subprocess  
from SimpleCV import Camera, Display, Image
import time  
import numpy
import os

def send_email(percentage):
            import smtplib
	    from email.MIMEMultipart import MIMEMultipart
	    from email.MIMEImage import MIMEImage
	    from email.MIMEText import MIMEText
		

            # Prepare actual message
	    msg = MIMEMultipart()
	    msg['From'] = "kstevica@gmail.com" # change to your mail
	    msg['To'] = "kstevica@gmail.com" # change to your mail
	    msg['Subject'] = "RPi Camera Alarm!"

	    imgcv = Image("image.jpg")
	    imgcv.save("imagesend.jpg", quality=50) # reducing quality of the image for smaller size

	    img1 = MIMEImage(open("imagesend.jpg","rb").read(), _subtype="jpg")
	    img1.add_header('Content-Disposition', 'attachment; filename="image.jpg"')
	    msg.attach(img1)

	    part = MIMEText('text', "plain")
	    part.set_payload(("Raspberry Pi camera alarm activated with level {:f}").format(percentage))
	    msg.attach(part)

            try:
                server = smtplib.SMTP("mail.htnet.hr", 25) #change to your SMTP provider
		server.ehlo()
                server.starttls()
                server.sendmail(msg['From'], msg['To'], msg.as_string())
                server.quit()
                print 'Successfully sent the mail'
            except smtplib.SMTPException as e:
    		print(e)


def imageDifference():
	if not os.path.isfile("image.jpg"):
 		subprocess.call("raspistill -n -t 1 -w 640 -h 480 -e jpg -o image.jpg", shell=True)
		time.sleep(0.5)
	img = Image("image.jpg")
	time.sleep(0.2)
	subprocess.call("raspistill -n -t 1 -w 640 -h 480 -e jpg -o image.jpg", shell=True)
	img2 = Image("image.jpg")

	diffimg = img2 - img	

	matrix = diffimg.getNumpy()
	flat = matrix.flatten()
	mean = matrix.mean()
	return mean

try:
	while True:
		percent = imageDifference()
		print percent
		if percent>6.2: # 6.2 is a good level to get activated during the day
			send_email(percent)
			print ("Camera alarm activated at level {:f}").format(percent)
			time.sleep(60)
		time.sleep(1.5)

except KeyboardInterrupt:
	print "Exit"
