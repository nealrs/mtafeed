from bs4 import BeautifulSoup
import requests
from flask import Flask, request, redirect, session, render_template
from datetime import datetime
from time import gmtime, strftime
import os
import uuid
import pytz
import json

app = Flask(__name__)

#presignoff = " Go to MTA dot info to learn more. "
presignoff = " "

def getFeed(mode):
	try:
		url = "http://tripplanner.mta.info/mobileApps/serviceStatus/serviceStatusPage.aspx?mode="+mode
		headers = {'Accept-Encoding': 'identity'}
		req = requests.get(url, headers=headers)
		print "Retrieved feed!!"
		return req.text
	except Exception as e:
		print "Error retrieving feed"
		raise
		return False


def getDetailUrl(mode):
	return "http://tripplanner.mta.info/mobileApps/serviceStatus/statusMessage.aspx?mode="+mode


def oxfordComma(items):
    length = len(items)
    if length == 1:
        return items[0]
    if length == 2:
        return '{} and {}'.format(*items)
    else:
		return '{}, and {}'.format(', '.join(items[:-1]), items[-1])


def getSubway():
	good = []
	detour = []
	change = []
	delay =[]
	work=[]

	good_sentence = ""
	detour_sentence = ""
	change_sentence = ""
	delay_sentence = ""
	work_sentence = ""

	feed = getFeed("subway")
	if feed:
		soup = BeautifulSoup(feed, 'html.parser')
		rows = soup.find_all("tr")

		for r in rows:
			line=""

			imgs = r.find_all("img")
			for i in imgs:
				line = line + (i.get('src'))[-5:-4].upper()
			if imgs == []:
				line = "Staten Island"

			status =  r.select('td')[1].get_text(strip=True)

			if status == "GOOD SERVICE":
				if line == "Staten Island":
					good.append(line)
				else:
					good.extend(line)

			if status == "PLANNED WORK":
				if line == "Staten Island":
					work.append(line)
				else:
					work.extend(line)

			if status == "SERVICE CHANGE":
				if line == "Staten Island":
					change.append(line)
				else:
					change.extend(line)

			if status == "DELAYS":
				if line == "Staten Island":
					delay.append(line)
				else:
					delay.extend(line)

	print "good service: "
	print good
	print "planned work: "
	print work
	print "service change: "
	print change
	print "delays: "
	print delay

	if good:
		good_sentence = oxfordComma(good)+ " trains are running fine."

	if work:
		work_sentence = "Some "+oxfordComma(work)+ " trains have scheduled work."

	if change:
		change_sentence = "There's a service change on the "+ oxfordComma(change)+ "."

	if delay:
		delay_sentence = "And blurgh, the "+oxfordComma(delay)+ " trains are running with delays."

	alltrains =  good_sentence + " " +  work_sentence + " " + change_sentence + " " + delay_sentence + presignoff + "Stand clear of the closing doors please!"
	return alltrains


def getBus():
	good = []
	detour = []
	change = []
	delay =[]

	good_sentence = ""
	detour_sentence = ""
	change_sentence = ""
	delay_sentence = ""
	work_sentence = ""

	feed = getFeed("bus")
	if feed:
		soup = BeautifulSoup(feed, 'html.parser')
		rows = soup.find_all("tr")

		for r in rows:
			line = (r.select('td')[0].get_text(strip=True)).replace(" - ", " to ")
			status =  r.select('td')[1].get_text(strip=True)

			if status == "GOOD SERVICE":
				good.append(line)

			if status == "PLANNED DETOUR":
				detour.append(line)

			if status == "SERVICE CHANGE":
				change.append(line)

			if status == "DELAYS":
				delay.append(line)

	print "good service: "
	print good
	print "planned detour: "
	print detour
	print "service change: "
	print change
	print "delay: "
	print delay

	if good:
		good_sentence = oxfordComma(good) + " busses are running fine."

	if detour:
		detour_sentence = "There are detours on routes: "+ oxfordComma(detour) + "."

	if change:
		change_sentence = "Be aware of service changes on "+ oxfordComma(change) + " busses."

	if delay:
		delay_sentence = "Routes "+ oxfordComma(delay) + " are running with delays."

	allbusses =  good_sentence + " " +  detour_sentence + " " +  change_sentence + " " + delay_sentence + presignoff +"Please exit through the rear door!"
	return allbusses


def getLIRR():
	good = []
	detour = []
	change = []
	delay = []
	work = []
	good_sentence = ""
	detour_sentence = ""
	change_sentence = ""
	delay_sentence = ""
	work_sentence = ""

	feed = getFeed("LIRR")
	if feed:
		soup = BeautifulSoup(feed, 'html.parser')
		rows = soup.find_all("tr")

		for r in rows:
			line = (r.select('td')[0].get_text(strip=True)).replace(" - ", " to ")
			status =  r.select('td')[1].get_text(strip=True)

			if status == "GOOD SERVICE":
				good.append(line)

			if status == "PLANNED DETOUR":
				detour.append(line)

			if status == "SERVICE CHANGE":
				change.append(line)

			if status == "DELAYS":
				delay.append(line)

			if status == "PLANNED WORK":
				work.append(line)

	print "good service: "
	print good
	print "planned detour: "
	print detour
	print "service change: "
	print change
	print "delay: "
	print delay
	print "planned work: "
	print work

	if good:
		good_sentence = oxfordComma(good)+ " trains are running fine."

	if detour :
		print detour
		detour_sentence = "There are detours on the "+ oxfordComma(detour) + " lines."

	if change:
		change_sentence = "Be aware of service changes on "+oxfordComma(change)+ " trains."

	if work:
		work_sentence = "There is work planned on the "+oxfordComma(work)+ " lines."

	if delay:
		delay_sentence = oxfordComma(delay)+ " trains are running with delays."


	alltrains =  good_sentence + " " +  detour_sentence + " " +  change_sentence + " " + work_sentence + " " +delay_sentence + presignoff +" Tickets please!"
	return alltrains


def getMNR():
	good = []
	detour = []
	change = []
	delay = []
	work = []
	good_sentence = ""
	detour_sentence = ""
	change_sentence = ""
	delay_sentence = ""
	work_sentence = ""

	feed = getFeed("MetroNorth")
	if feed:
		soup = BeautifulSoup(feed, 'html.parser')
		rows = soup.find_all("tr")

		for r in rows:
			line = (r.select('td')[0].get_text(strip=True)).replace(" - ", " to ")
			status =  r.select('td')[1].get_text(strip=True)

			if status == "GOOD SERVICE":
				good.append(line)

			if status == "PLANNED DETOUR":
				detour.append(line)

			if status == "SERVICE CHANGE":
				change.append(line)

			if status == "DELAYS":
				delay.append(line)

			if status == "PLANNED WORK":
				work.append(line)

	print "good service: "
	print good
	print "planned detour: "
	print detour
	print "service change: "
	print change
	print "delay: "
	print delay
	print "planned work: "
	print work

	if good:
		good_sentence = oxfordComma(good)+ " trains are running fine."

	if detour :
		print detour
		detour_sentence = "There are detours on the "+ oxfordComma(detour) + " lines."

	if change:
		change_sentence = "Be aware of service changes on "+oxfordComma(change)+ " trains."

	if work:
		work_sentence = "There is work planned on the "+oxfordComma(work)+ " lines."

	if delay:
		delay_sentence = oxfordComma(delay)+ " trains are running with delays."


	alltrains =  good_sentence + " " +  detour_sentence + " " +  change_sentence + " " + work_sentence + " " +delay_sentence + presignoff +" Tickets please!"
	return alltrains


def getBT():
	good = []
	detour = []
	change = []
	delay = []
	work = []
	good_sentence = ""
	detour_sentence = ""
	change_sentence = ""
	delay_sentence = ""
	work_sentence = ""

	feed = getFeed("BT")
	if feed:
		soup = BeautifulSoup(feed, 'html.parser')
		rows = soup.find_all("tr")

		for r in rows:
			line = (r.select('td')[0].get_text(strip=True)).replace(" - ", " to ")
			status =  r.select('td')[1].get_text(strip=True)

			if status == "GOOD SERVICE":
				good.append(line)

			if status == "PLANNED DETOUR":
				detour.append(line)

			if status == "SERVICE CHANGE":
				change.append(line)

			if status == "DELAYS":
				delay.append(line)

			if status == "PLANNED WORK":
				work.append(line)

	print "good service: "
	print good
	print "planned detour: "
	print detour
	print "service change: "
	print change
	print "delay: "
	print delay
	print "planned work: "
	print work

	if good:
		good_sentence = "The "+oxfordComma(good)+ " are all running fine."

	if detour :
		print detour
		detour_sentence = "There are detours on the "+oxfordComma(detour)+ "."

	if change:
		change_sentence = "Be aware of service changes on the "+oxfordComma(change)+ "."

	if work:
		work_sentence = "There is work planned on the "+oxfordComma(work)+ "."

	if delay:
		delay_sentence = "The "+oxfordComma(delay)+ " are backed up."


	allroutes =  good_sentence + " " +  detour_sentence + " " +  change_sentence + " " + work_sentence + " " +delay_sentence + presignoff +" Sunglasses off, lights on!"
	return allroutes


def dates():
	# establish current date in PT timezone
	tz = pytz.timezone('America/New_York')
	today = datetime.now(tz)
	today_utc = today.astimezone(pytz.UTC)
	date = today.strftime("%Y-%m-%d")
	locale = today.strftime("%a, %B %d").lstrip("0").replace(" 0", " ")

	# debug lines for date info #
	print date
	print locale
	print today_utc
	print '\n'
	return today_utc, locale

# Subway feed
@app.route('/subway', methods=['GET'])
def subway():
	date, locale = dates()
	feed = {}
	feed['uid'] = str(uuid.uuid4())
	feed['updateDate'] = date.strftime('%Y-%m-%dT%H:%M:%S.0Z')
	feed['mainText'] = getSubway()
	feed['titleText'] = "NYC Subway Status "+ locale
	feed['redirectionURL'] = getDetailUrl("subway")
	feed_json = json.dumps(feed)
	print feed_json
	return feed_json


# Subway feed
@app.route('/bus', methods=['GET'])
def bus():
	date, locale = dates()
	feed = {}
	feed['uid'] = str(uuid.uuid4())
	feed['updateDate'] = date.strftime('%Y-%m-%dT%H:%M:%S.0Z')
	feed['mainText'] = getBus()
	feed['titleText'] = "NYC Bus System Status "+ locale
	feed['redirectionURL'] = getDetailUrl("bus")
	feed_json = json.dumps(feed)
	print feed_json
	return feed_json


# Long Island Railroad feed
@app.route('/lirr', methods=['GET'])
def lirr():
	date, locale = dates()
	feed = {}
	feed['uid'] = str(uuid.uuid4())
	feed['updateDate'] = date.strftime('%Y-%m-%dT%H:%M:%S.0Z')
	feed['mainText'] = getLIRR()
	feed['titleText'] = "Long Island Railroad Status "+ locale
	feed['redirectionURL'] = getDetailUrl("LIRR")
	feed_json = json.dumps(feed)
	print feed_json
	return feed_json


# MetroNorth feed
@app.route('/mnr', methods=['GET'])
def mnr():
	date, locale = dates()
	feed = {}
	feed['uid'] = str(uuid.uuid4())
	feed['updateDate'] = date.strftime('%Y-%m-%dT%H:%M:%S.0Z')
	feed['mainText'] = getMNR()
	feed['titleText'] = "Metro North Railroad Status "+ locale
	feed['redirectionURL'] = getDetailUrl("MetroNorth")
	feed_json = json.dumps(feed)
	print feed_json
	return feed_json


# Bridge & Tunnel feed
@app.route('/bt', methods=['GET'])
def bt():
	date, locale = dates()
	feed = {}
	feed['uid'] = str(uuid.uuid4())
	feed['updateDate'] = date.strftime('%Y-%m-%dT%H:%M:%S.0Z')
	feed['mainText'] = getBT()
	feed['titleText'] = "NYC Bridge & Tunnel Status "+ locale
	feed['redirectionURL'] = getDetailUrl("BT")
	feed_json = json.dumps(feed)
	print feed_json
	return feed_json


# Marketing page w/ list of feeds / screenshot of feed app? link to Alexa Skill page
@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

if __name__ == "__main__":
	app.run(debug=True)
