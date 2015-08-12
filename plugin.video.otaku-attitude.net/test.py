import urllib,urllib2,re

#VIDEO TEMPLATE - by ALBLS 2014.

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
      icon = 'special://home/addons/plugin.video.otaku-attitude.net/icon.png'
  return icon

def fixUrl(url):
  root = 'http://www.otaku-attitude.net/'
  if url[:5] != 'http:':
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

def getMagnetLink(magnet):
  playback_url = 'plugin://plugin.video.xbmctorrent/play/magnet' + magnet
  return playback_url

  #Navigate unctions
def CATEGORIES():
        addDir('Animes','http://www.otaku-attitude.net/liste-dl-animes.php',1,defIcon(''))
        addDir('Dramas','http://www.otaku-attitude.net/liste-dl-dramas.php',1,defIcon(''))
        addDir('Films','http://www.otaku-attitude.net/liste-dl-films.php',1,defIcon(''))
        addDir('O-A Fansub','http://www.otaku-attitude.net/liste-dl-fansub.php',1,defIcon(''))
                       
def INDEX(url):
        addDir('Non défini',url+'?genre=0',2,defIcon(''))
        addDir('Action',url+'?genre=1',2,defIcon(''))
        addDir('Amour & Amitié',url+'?genre=2',2,defIcon(''))
        addDir('Aventure',url+'?genre=3',2,defIcon(''))
        addDir('Combats & Arts Martiaux',url+'?genre=4',2,defIcon(''))
        addDir('Comédie',url+'?genre=5',2,defIcon(''))
        addDir('Contes & Récits',url+'?genre=6',2,defIcon(''))
        addDir('Cyber & Mecha',url+'?genre=7',2,defIcon(''))
        addDir('Drame',url+'?genre=8',2,defIcon(''))
        addDir('Ecchi',url+'?genre=9',2,defIcon(''))
        addDir('Enigme & Policiers',url+'?genre=10',2,defIcon(''))
        addDir('Epique & Heroïque',url+'?genre=11',2,defIcon(''))
        addDir('Espace & Sci-fiction',url+'?genre=12',2,defIcon(''))
        addDir('Fantastique & Mythe',url+'?genre=13',2,defIcon(''))
        addDir('Guerre & Conflit',url+'?genre=14',2,defIcon(''))
        addDir('Historique',url+'?genre=15',2,defIcon(''))
        addDir('Horreur',url+'?genre=16',2,defIcon(''))
        addDir('Magical Girl',url+'?genre=17',2,defIcon(''))
        addDir('Musical',url+'?genre=18',2,defIcon(''))
        addDir('Sport',url+'?genre=19',2,defIcon(''))
        addDir('Yaoi',url+'?genre=20',2,defIcon(''))
        addDir('Yuri',url+'?genre=21',2,defIcon(''))

def GROUP(url):
        page = getPage(url)
        match=re.compile('<a href="(.+?)" class="liste_dl"><img src="(.+?)" class="vignette" alt=".+?" /> <strong>(.+?)</strong><div class="field">.+?</div><div class="field">.+?</div><span class="syno ui-corner-all">(.+?)<br /><br /><div id="votants"><strong>.+?</strong></div></span></a>').findall(page)
        for url2, picture, name, plot in match:
                addDirPlot(htmlDecode(name),url2,3,defIcon(picture),htmlDecode(plot))

def VIDEOLINKS(url,name,icon):
        page = getPage(url)
        idepisode = ''
        match=re.compile('\'anime:(.+?)\'').findall(page)
        if len(match) > 0 : 
          idepisode = match[0]
        match=re.compile('<tr class="down.+?" id="(.+?)" >        <td class="cell"><strong>(.+?)</strong></td><td class="cell">(.+?)</td><td class="cell">(.+?)</td>').findall(page)
        for link_id,episode, format_video, resolution in match:
          urlvid = 'http://www.otaku-attitude.net/launch-download-anime-'+idepisode+'-ddl-'+link_id+'.html'
          addLink(htmlDecode(name)+' Ep.'+episode+' (Format:'+format_video+' Reso.:'+resolution.replace('×','x')+')',urlvid,defIcon(icon))

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

def addDirPlot(name,url,mode,iconimage,plot):
        print 'adddir *****'
        print 'name=\''+name+'\''
        print 'plot=\''+plot+'\''
        print 'url=\''+url+'\''
        print 'mode='+str(mode)+''
        print 'icon=\''+iconimage+'\''
        print '************'
        
name='Dangaizer 3'
url='fiche-anime-705-dangaizer-3.html'
mode=3
icon='http://images.otaku-attitude.net/themes/zen/images/dl/animes/dangaizer-3.png'

print '------------------------------------------------------------------------------------'
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Icon: "+str(icon)
print '------------------------------------------------------------------------------------'

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        INDEX(url)

elif mode==2:
        print ""+url
        GROUP(url)

elif mode==3:
        print ""+url
        VIDEOLINKS(url,name,icon)




