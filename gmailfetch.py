# import the required libraries
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from selenium.webdriver.chrome.options import Options
import pickle
import os.path
import re
import base64
import time
import email
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
from bs4 import BeautifulSoup, SoupStrainer

# Define the SCOPES. If modifying it, delete the token.pickle file.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def getEmails():
 	

	# Variable creds will store the user access token.
	# If no valid token found, we will create one.
	creds = None
	

	# The file token.pickle contains the user access token.
	# Check if it exists
	if os.path.exists('token.pickle'):

		# Read the token from the file and store it in the variable creds
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)

	# If credentials are not available or are invalid, ask the user to log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			print("penis")
			creds.refresh(Request())
		else:
      #you get the json from https://console.cloud.google.com/apis/credentials/oauthclient/648008577517-klkrk260il3jmijk123prrn5iesi77a7.apps.googleusercontent.com?project=gmailfetch-374220
			flow = InstalledAppFlow.from_client_secrets_file('client_secret_648008577517-klkrk260il3jmijk123prrn5iesi77a7.apps.googleusercontent.com.json', SCOPES)
			creds = flow.run_local_server(port=0)

		# Save the access token in token.pickle file for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	# Connect to the Gmail API
	service = build('gmail', 'v1', credentials=creds)

	# request a list of all the messages
	#result = service.users().messages().list(userId='me').execute()

	# We can also pass maxResults to get any number of emails. Like this:
	result = service.users().messages().list(maxResults=300, userId='me').execute()
	messages = result.get('messages')
	#print(messages)
	# messages is a list of dictionaries where each dictionary contains a message id.

	# iterate through all the messages
	for msg in messages:
		# Get the message from its id
		txt = service.users().messages().get(userId='me', id=msg['id']).execute()
		#print(txt)
		
		# Use try-except to avoid any Errors
		try:
			# Get value of 'payload' from dictionary 'txt'
			payload = txt['payload']
			headers = payload['headers']

			# Look for Subject and Sender Email in the headers
			for d in headers:
				if d['name'] == 'Subject':
					subject = d['value']
				if d['name'] == 'From':
					sender = d['value']


			# The Body of the message is in Encrypted format. So, we have to decode it.
			# Get the data and decode it with base 64 decoder.
			#parts = payload.get('parts')[0]
			#data = parts['body']['data']
			#data = data.replace("-","+").replace("_","/")
			#decoded_data = base64.b64decode(data)

			# Now, the data obtained is in lxml. So, we will parse
			# it with BeautifulSoup library
			#soup = BeautifulSoup(decoded_data , "lxml")
			#body = soup.body()

			# Printing the subject, sender's email and message
			if subject=="You got bumped from the playlist. Spin again!":
				#print("Subject: ", subject)
				#print("From: ", sender)
				# The Body of the message is in Encrypted format. So, we have to decode it.
				# Get the data and decode it with base 64 decoder.
				#print(txt)
				body = payload['body']
				data = body['data']

				#print(data)

				data = data.replace("-","+").replace("_","/")
				decoded_data = base64.b64decode(data)

				# Now, the data obtained is in lxml. So, we will parse
				# it with BeautifulSoup library
				# do 'pip install lxml' or youll get parse error
				soup = BeautifulSoup(decoded_data , "lxml")
				body = soup.body()
				print("Message: ", body)
				print('\n*********************END OF DATA**************************')

				urls = re.findall('http://[a-zA-Z0-9_./?=-]*', str(body))
				options = Options()
				options.add_argument("--user-data-dir=C:\\Users\\Ilya Rogers\\Documents\\udata")
				options.add_experimental_option("detach", True)
				options.page_load_strategy = 'normal'
				driver = webdriver.Chrome(options=options)
				driver.get(urls[1])
				time.sleep(2)

				
				selected = Select(driver.find_element(By.ID,"wheelSongId"))

				# select by visible text
				#selected.select_by_visible_text('Misconfiguration Sensation Station: Atomic Snow')
				selected.select_by_index(3)
				# select by value 
				#select.select_by_value('1')
				driver.find_element(By.ID, "submit").submit()
				driver.execute_script("connectWithSpotifyWheel()")

				#parse resulted html and go to the wheel link
				#use selenium to step through autorization
				#pick static song for now eventually read in whole list and pick randon one
				#spin wheel till you cant
				#remove email

		except:
			pass


getEmails()
#TODO: Close all instances of chrome before starting another