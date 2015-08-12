import urllib,urllib2,re
addonID = "plugin.video.mangas-streaming.fr"

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
      icon = 'special://home/addons/'+addonID+'/icon.png'
  return icon

def fixUrl(url):
  root = 'http://www.mangas-streaming.fr/'
  if url[:5] != 'http:':
      if url[:1] == '/':
        url = url[1:]
      url = root + url
  return url

def getPage(url):
  try:
      req = urllib2.Request(fixUrl(url))
      req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
      response = urllib2.urlopen(req)
      link=response.read()
      response.close()
      return link.replace('\n','').replace('\t','').replace('\r','')
  except Exception, e:
      print "URL : " + url
      print "fixed URL : " +  fixUrl(url)
      print "Erreur : " + e
      pass

def getYouTubeLink(video_id):
  playback_url = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=' + video_id
  return playback_url


#Navigate Functions
def CATEGORIES():
        addDir('Animé','http://www.mangas-streaming.fr/anime/',1,defIcon(''))
        addDir('Dramas','http://www.mangas-streaming.fr/dramas/',1,defIcon(''))

def SUBCATEGORIES(url):
        addDir('Lettre A',url+'lettre/A',2,defIcon(''))
        addDir('Lettre B',url+'lettre/B',2,defIcon(''))
        addDir('Lettre C',url+'lettre/C',2,defIcon(''))
        addDir('Lettre D',url+'lettre/D',2,defIcon(''))
        addDir('Lettre E',url+'lettre/E',2,defIcon(''))
        addDir('Lettre F',url+'lettre/F',2,defIcon(''))
        addDir('Lettre G',url+'lettre/G',2,defIcon(''))
        addDir('Lettre H',url+'lettre/H',2,defIcon(''))
        addDir('Lettre I',url+'lettre/I',2,defIcon(''))
        addDir('Lettre J',url+'lettre/J',2,defIcon(''))
        addDir('Lettre K',url+'lettre/K',2,defIcon(''))
        addDir('Lettre L',url+'lettre/L',2,defIcon(''))
        addDir('Lettre M',url+'lettre/M',2,defIcon(''))
        addDir('Lettre N',url+'lettre/N',2,defIcon(''))
        addDir('Lettre O',url+'lettre/O',2,defIcon(''))
        addDir('Lettre P',url+'lettre/P',2,defIcon(''))
        addDir('Lettre Q',url+'lettre/Q',2,defIcon(''))
        addDir('Lettre R',url+'lettre/R',2,defIcon(''))
        addDir('Lettre S',url+'lettre/S',2,defIcon(''))
        addDir('Lettre T',url+'lettre/T',2,defIcon(''))
        addDir('Lettre U',url+'lettre/U',2,defIcon(''))
        addDir('Lettre V',url+'lettre/V',2,defIcon(''))
        addDir('Lettre W',url+'lettre/W',2,defIcon(''))
        addDir('Lettre X',url+'lettre/X',2,defIcon(''))
        addDir('Lettre Y',url+'lettre/Y',2,defIcon(''))
        addDir('Lettre Z',url+'lettre/Z',2,defIcon(''))
        addDir('Chiffres',url+'lettre/1',2,defIcon(''))

def INDEX(url):
        page = getPage(url)
        match=re.compile('<h2 class="entry-title"><a href="(.+?)" rel="bookmark">(.+?)</a></h2>').findall(page)
        matchPic=re.compile('  <img alt="(.+?)"  src=".+?"/>  ').findall(page)
        pos = 0
        for url2,name in match:
                picture = matchPic[pos]
                if picture.rfind('"') > 0:
                  picture = picture[picture.rfind('"'):]
                addDir(name,url2,3,fixUrl(picture))
                pos = pos + 1

def VIDEOLINKS(url,name,icon):
        page = getPage(url)
        match=re.compile('<td> <a href="(.+?)">(.+?)</a></td>').findall(page)
        for urlvid,name in match:
                addLink(htmlDecode(name),fixUrl(urlvid),icon)

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
        

name='Angel Beats!'
url='/anime/show/16/Angel+Beats%21-vostfr-streaming-ddl-hd'
mode=3
icon='http://www.mangas-streaming.fr/uploads/8a8cf87d2cbd851b2c265f5a4109a99d497f137e.jpg'

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Icon: "+str(icon)

if mode==None or url==None or len(url)<1:
        CATEGORIES()
elif mode==1:
        SUBCATEGORIES(url)
elif mode==2:
        INDEX(url)
elif mode==3:
        VIDEOLINKS(url,name,icon)




