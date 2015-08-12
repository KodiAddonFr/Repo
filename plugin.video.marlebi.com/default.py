import util, urllib2

def playVideo(params):
    response = urllib2.urlopen(params['video'])
    if response and response.getcode() == 200:
        content = response.read()
        videoLink = util.extract(content, 'flashvars.File = "', '"')
        util.playMedia(params['title'], params['image'], videoLink, 'Video')
    else:
        util.showError(ADDON_ID, 'Could not open URL %s to get video information' % (params['video']))
    
def buildMenu():
    url = WEB_PAGE_BASE + 'animes.php'
    response = urllib2.urlopen(url)
    if response and response.getcode() == 200:
        content = response.read()
        videos = util.extractAll(content, '<td width="40%" align="center">', '/td>')
        for video in videos:
            params = {'submenu':1}
            params['video'] = WEB_PAGE_BASE + util.extract(video, 'a href="', '\"')
            params['image'] = WEB_PAGE_BASE + util.extract(video, 'img src="', '\"')
            params['title'] = util.extract(video, '<p align="center">', '</p>') 
            link = util.makeLink(params)
            util.addMenuItem(params['title'], link, 'DefaultVideo.png', params['image'], False)
        util.endListing()
    else:
        util.showError(ADDON_ID, 'Could not open URL %s to create menu' % (url))
		
def buildSubMenu(params):
    response = urllib2.urlopen(params['video'])
    if response and response.getcode() == 200:
        content = response.read()
        videos = util.extractAll(content, '<td width="40%" align="center">', '/td>')
        for video in videos:
            params = {'play':1}
            params['video'] = WEB_PAGE_BASE + util.extract(video, 'a href="', '\"')
            params['image'] = WEB_PAGE_BASE + util.extract(video, 'img src="', '\"')
            params['title'] = util.extract(video, '<p align="center">', '</p>') 
            link = util.makeLink(params)
            util.addMenuItem(params['title'], link, 'DefaultVideo.png', params['image'], False)
        util.endListing()
    else:
        util.showError(ADDON_ID, 'Could not open URL %s to create menu' % (url))

WEB_PAGE_BASE = 'http://www.marlebi.com/'
ADDON_ID = 'plugin.video.marlebi.com'

parameters = util.parseParameters()
if 'submenu' in parameters:
	buildSubMenu(parameters)
else:
	if 'play' in parameters:
		playVideo(parameters)
	else:
		buildMenu()
