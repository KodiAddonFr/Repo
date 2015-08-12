import urllib,urllib2,re
import bs4 as BeautifulSoup


#VIDEO TEST TEMPLATE - by ALBLS 2014.

#Tools functions 
def htmlDecode(text):
  text = text.replace("&EACUTE;","É")
  text = text.replace("&eacute;","é")
  text = text.replace("&egrave;","è")
  text = text.replace("&ecirc;","ê")
  text = text.replace("&quot;","\"")
  text = text.replace("&#039;","'")
  text = text.replace("&agrave;","à")
  text = text.replace("&acirc;","â")
  text = text.replace("&iuml;","ï")
  text = text.replace("&ocirc;","ô")
  text = text.replace("&deg;","°")
  text = text.replace("&amp;","&")
  return text
  
def htmlEncode(text):
  text = text.replace(" ","+")
  text = text.replace("[","%5B")
  text = text.replace("]","%5D")
  text = text.replace("&","&amp;")
  return text
  
def htmlEncodeUrl(text):
  text = text.replace(" ","%20")
  text = text.replace("[","%5B")
  text = text.replace("]","%5D")
  text = text.replace("&","&amp;")
  return text

def defIcon(icon):
  if icon == '':
      icon = 'special://home/addons/plugin.video.sky-animes/icon.png'
  return icon

def fixUrl(url):
  root = 'http://www.sky-animes.com/'
  if url[:5] != 'http:':
      url = root + url
  return url

def getPage(url):
  try:
      req = urllib2.Request(fixUrl(url))
      req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
      response = urllib2.urlopen(req)
      link=response.read() #.replace('\n','').replace('\t','').replace('\r','')
      response.close()
      return link
  except Exception, e:
      print "URL : " + url
      print "fixed URL : " +  fixUrl(url)
      print "Erreur : " + str(e)
      return ''

def getSoup(url):
  html = getPage(url)
  soup = BeautifulSoup.BeautifulSoup(html)
  return soup
  
def getYouTubeLink(video_id):
  playback_url = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=' + video_id
  return playback_url

def getDailyMotionLink(url):
  playback_url = 'plugin://plugin.video.dailymotion_com/?mode=playVideo&url='+urllib.quote_plus(url)+')'
  return playback_url

#Navigate functions
def CATEGORIES():
        addDir('Animes en cours','http://www.sky-animes.com/streaming-animes-en-cours',1,defIcon('http://www.sky-animes.com/themes/SkY-AniMeS/images//titres/animes en cours.png'))
        addDir('Animes terminés','http://www.sky-animes.com/streaming-animes-termines',1,defIcon('http://www.sky-animes.com/themes/SkY-AniMeS/images//titres/animes termines.png'))
        addDir('Dramas en cours','http://www.sky-animes.com/streaming-dramas-en-cours',1,defIcon('http://www.sky-animes.com/themes/SkY-AniMeS/images//titres/dramas en cours.png'))
        addDir('Dramas terminés','http://www.sky-animes.com/streaming-dramas-termines',1,defIcon('http://www.sky-animes.com/themes/SkY-AniMeS/images//titres/animes termines.png'))
        addDir('Films','http://www.sky-animes.com/streaming-films',1,defIcon('http://www.sky-animes.com/themes/SkY-AniMeS/images//titres/films.png'))
        addDir('OAVs','http://www.sky-animes.com/streaming-oavs',1,defIcon('http://www.sky-animes.com/themes/SkY-AniMeS/images//titres/oavs.png'))
                       
def SUBCATEGORIES(url,icon):
        soup = getSoup(url)
        for select in soup.findAll('select',{ "id":"triGenre" }):
          for option in select.findAll('option'):
            name = option.text
            urltmp = option.get('value')
            url2 = url +'?genre='+ htmlEncodeUrl(urltmp)
            img = icon
            addDir(name,url2,2,img)
              
def INDEX(url):
        page = getPage(url)
        match=re.compile('<td width="206" valign="middle" height="16" style="padding: 0; padding-left: 20px; margin: 0; white-space: nowrap;"><a href="(.+?)"><b>(.+?)</b></a></td>').findall(page)
        for url2,name in match:
          addDir(name,fixUrl(url2),3,defIcon(''))
        
def VIDEOLINKS(url,name,icon):
        soup = getSoup(url)
        for td in soup.findAll('td',{"style":"padding-left: 12px;"}):
          for big in td.findAll('big'):
            for a in big.parent.findAll('a'):
              vidname = big.text
              href = a.get('href').replace('#','')
              vidurl = 'http://www.sky-animes.com//index.php?file=Download&nuked_nude=index&op=do_dl&dl_id='+href+'&nb=1'
              addLink(vidname,vidurl,defIcon(icon))

#Specific XBMC

def addLink(name,url,iconimage):
        print 'addLink *****'
        print 'name=\''+name+'\''
        print 'url=\''+url+'\''
        print 'icon=\''+iconimage+'\''
        print '*************'

def addDir(name,url,mode,iconimage):
        print 'adddir *****'
        print 'name=\''+name+'\''
        print 'url=\''+url+'\''
        print 'mode='+str(mode)+''
        print 'icon=\''+iconimage+'\''
        print '************'
        
name='Dramas en cours'
url='http://www.sky-animes.com/streaming-dramas-en-cours'
mode=1
icon='http://www.sky-animes.com/themes/SkY-AniMeS/images//titres/dramas en cours.png'


print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Icon: "+str(icon)

if mode==None or url==None or len(url)<1:
        CATEGORIES()
elif mode==1:
        SUBCATEGORIES(url,icon)
elif mode==2:
        INDEX(url)
elif mode==3:
        VIDEOLINKS(url,name,icon)




