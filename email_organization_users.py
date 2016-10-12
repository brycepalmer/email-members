# Get list of users from a github organization
#Bryce Palmer
#bryce.palmer5@gmail.com
#Directions: 
# pip install pygithub
# pip install smtplib
# pip install tinys3

from github import Github
import smtplib
import tinys3
import os

def send_email(toEmail):
	fromEmail = 'testa3484@gmail.com'
	fromPassword = 'this is a test'
	SUBJECT = 'my subject'
	TEXT = 'email body text'
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromEmail, fromPassword)
	
	msg = 'Subject: %s\n\n%s' % (SUBJECT, TEXT)
	#msg = 'this is text'
	server.sendmail(fromEmail, toEmail, msg,'subject')
	server.quit()
	
def upload_to_bucket(file):
	S3_ACCESS_KEY = 'AKIAJCW7RDWGJ6P24SXQ'
	S3_SECRET_KEY = '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'
	conn = tinys3.Connection(S3_ACCESS_KEY,S3_SECRET_KEY,tls=True,endpoint='s3-us-west-2.amazonaws.com')
	f = open(file,'rb')
	print file
	print conn.upload('emails-for-no-named-members/%s' % (file),f,'github-nameless-users')
	#print conn.upload(file,f,'github-nameless-users')
	#print conn.get('emails-for-no-named-members/%s' % (file),'github-nameless-users')
	print 'uploaded data to S3'
	
def add_text_to_file(text,organization):
	file = '%s.txt' % (organization)
	print file
	try:
		with open(file, "a") as myfile:
			myfile.write('%s\n' % (text))
			return file
	except IOError:
		# generate the file
		os.mkdir(file)
		with open(file, "a") as myfile:
			myfile.write('%s\n' % (text))
			return file


#varialbe to be used
token = '5994e4a469c8b409335933fa9d75c7a05cb848fb'
organization = 'members-must-have-profile-names'

# First create a Github instance:
git = Github(token)
org = git.get_organization(organization)
members = org.get_members()

#Check for names that are None and send emails
for member in members:
	if member.name is None:
		#send email to them with the link to set their name
		if member.email is not None:
			text = 'Sending email to %s' % (member.email)
			print text
			send_email(member.email)
			file = add_text_to_file(member.email, organization)
print "Done!\n"

#Save list on AWS
upload_to_bucket(file)

