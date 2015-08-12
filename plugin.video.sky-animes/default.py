#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui
import bs4 as BeautifulSoup

try:
    import StorageServer
except:
    import storageserverdummy as StorageServer
cache = StorageServer.StorageServer("plugin.video.sky-animes", 24) # (Your plugin name, Cache time in hours)

addonID = "plugin.video.sky-animes"

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
  text = text.replace("é","&eacute;")
  text = text.replace("è","&egrave;")
  text = text.replace(" ","+")
  text = text.replace("[","%5B")
  text = text.replace("]","%5D")
  text = text.replace("&","&amp;")
  return text
  
def htmlEncodeUrl(text):
    text = text.replace("é","&eacute;")
    text = text.replace("è","&egrave;")
    text = text.replace("ô","&ocirc;")
    text = text.replace("à","&agrave;")
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
  root = 'http://www.sky-animes.com/'
  if url[:5] != 'http:':
      url = root + url
  return url

def getPage(url):
  try:
      req = urllib2.Request(fixUrl(url))
      req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; fr-FR; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
      response = urllib2.urlopen(req)
      link = response.read()
      response.close()
      #.encode('utf-8')
      return link #.replace('\n','').replace('\t','').replace('\r','')
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
        addDir('Animes en cours','http://www.sky-animes.com/streaming-animes-en-cours',1,'http://www.sky-animes.com/themes/SkY-AniMeS/images//titres/animes%20en%20cours.png')
        addDir('Animes terminés','http://www.sky-animes.com/streaming-animes-termines',1,'http://www.sky-animes.com/themes/SkY-AniMeS/images//titres/animes%20termines.png')
        addDir('Dramas en cours','http://www.sky-animes.com/streaming-dramas-en-cours',1,'http://www.sky-animes.com/themes/SkY-AniMeS/images//titres/dramas%20en%20cours.png')
        addDir('Dramas terminés','http://www.sky-animes.com/streaming-dramas-termines',1,'http://www.sky-animes.com/themes/SkY-AniMeS/images//titres/dramas%20termines.png')
        addDir('Films','http://www.sky-animes.com/streaming-films',1,'http://www.sky-animes.com/themes/SkY-AniMeS/images//titres/films.png')
        addDir('OAVs','http://www.sky-animes.com/streaming-oavs',1,'http://www.sky-animes.com/themes/SkY-AniMeS/images//titres/oavs.png')

def SUBCATEGORIES(url,icon):
        soup = getSoup(url)
        for select in soup.findAll('select',{ "id":"triGenre" }):
          for option in select.findAll('option'):
            name = option.text.encode('utf-8')
            urltmp = option.get('value').encode('utf-8')
            url2 = url +'?genre='+ htmlEncodeUrl(urltmp)
            addDir(name,url2,2,defIcon(''))

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
def translation(id):
    return addon.getLocalizedString(id).encode('utf-8')


def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param


def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setProperty("IsPlayable", "true")
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok


def addLinkWithPlot(name,plot,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setProperty("IsPlayable", "true")
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot": plot } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&icon="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
params=get_params()

url=None
name=None
mode=None
icon=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        icon=urllib.unquote_plus(params["icon"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

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



xbmcplugin.endOfDirectory(int(sys.argv[1]))
