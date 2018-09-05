# owa-calendar-extractor
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django.svg)
![Google app script](https://img.shields.io/badge/google--app--script-stable-blue.svg)

Tool for downloading data from your Outlook Web Application calendar (selenium python script) and store to your Google Calendar (google app script)


## Installation
### Google calendar
1. Go to https://calendar.google.com
2. Create or just use existing calendar
3. Go to calendar Settings and sharing
4. Copy your **Google calendar identificator** (*Calendar integration* section)
	-	ID is in form - *randomstring*@group.calendar.google.com

### Google app scripts
1. Create Google app script - https://script.google.com/home
2. Copy-paste [gapp-owa-extractor.gs](https://github.com/igorsimko/owa-calendar-extractor/blob/master/gapp-owa-extractor.gs "gapp-owa-extractor.gs")
3. Set **Google calendar identificator**
4. Publish script 
	- Publish -> Deploy as web app
		- Project version: New
		- Who has access to the app: anyone, even anonymous
		- Click on update
	- Copy **Current web app URL** - It's your Google App script Rest API (get) URL

> You can test script via *test()* method and uncomment some lines (see
> Gscript)

### Python script
Run python script.

```sh
$ python headless.py
```
If there is no error or error.png screenshot, you will be able to see your OWA events in your Google calendar 
