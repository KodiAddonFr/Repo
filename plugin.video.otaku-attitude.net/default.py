import urllib,urllib2,re,xbmcplugin,xbmcgui

try:
    import StorageServer
except:
    import storageserverdummy as StorageServer
cache = StorageServer.StorageServer("plugin.video.otaku-attitude.net", 24) # (Your plugin name, Cache time in hours)
 
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
                       
def addCheckDir(name,url,mode,iconimage):
        page = cache.cacheFunction(getPage,url)
        match=re.compile('<div class="incorrect" style=".+?">(.+?)</div>').findall(page)
        if len(match)==0:
            addDir(name,url,mode,iconimage)

def INDEX(url):
        addCheckDir('Non défini',url+'?genre=0',2,defIcon(''))
        addCheckDir('Action',url+'?genre=1',2,defIcon(''))
        addCheckDir('Amour & Amitié',url+'?genre=2',2,defIcon(''))
        addCheckDir('Aventure',url+'?genre=3',2,defIcon(''))
        addCheckDir('Combats & Arts Martiaux',url+'?genre=4',2,defIcon(''))
        addCheckDir('Comédie',url+'?genre=5',2,defIcon(''))
        addCheckDir('Contes & Récits',url+'?genre=6',2,defIcon(''))
        addCheckDir('Cyber & Mecha',url+'?genre=7',2,defIcon(''))
        addCheckDir('Drame',url+'?genre=8',2,defIcon(''))
        addCheckDir('Ecchi',url+'?genre=9',2,defIcon(''))
        addCheckDir('Enigme & Policiers',url+'?genre=10',2,defIcon(''))
        addCheckDir('Epique & Heroïque',url+'?genre=11',2,defIcon(''))
        addCheckDir('Espace & Sci-fiction',url+'?genre=12',2,defIcon(''))
        addCheckDir('Fantastique & Mythe',url+'?genre=13',2,defIcon(''))
        addCheckDir('Guerre & Conflit',url+'?genre=14',2,defIcon(''))
        addCheckDir('Historique',url+'?genre=15',2,defIcon(''))
        addCheckDir('Horreur',url+'?genre=16',2,defIcon(''))
        addCheckDir('Magical Girl',url+'?genre=17',2,defIcon(''))
        addCheckDir('Musical',url+'?genre=18',2,defIcon(''))
        addCheckDir('Sport',url+'?genre=19',2,defIcon(''))
        addCheckDir('Yaoi',url+'?genre=20',2,defIcon(''))
        addCheckDir('Yuri',url+'?genre=21',2,defIcon(''))

def GROUP(url):
        page = cache.cacheFunction(getPage,url)
        match=re.compile('<a href="(.+?)" class="liste_dl"><img src="(.+?)" class="vignette" alt=".+?" /> <strong>(.+?)</strong><div class="field">.+?</div><div class="field">.+?</div><span class="syno ui-corner-all">(.+?)<br /><br /><div id="votants"><strong>.+?</strong></div></span></a>').findall(page)
        for url2, picture, name, plot in match:
                addDirPlot(htmlDecode(name),url2,3,defIcon(picture),htmlDecode(plot))
        numpage = re.compile('scroll=(.+?)').findall(url)
        if len(numpage) > 0:
            nextScroll = str(int(url[url.find('scroll=')+7:])+1)
            nextPage = str(int(nextScroll) + 1)
        else:
            nextPage = '2'
            nextScroll = '1'
        matchNext = re.compile('<div id="infinite-stop"></div>').findall(page)
        if len(matchNext)==0:
                url = url[:url.find('&scroll=')]
                addDir('Page '+nextPage,url+'&scroll='+nextScroll,2,defIcon(''))

def VIDEOLINKS(url,name,icon):
        page = cache.cacheFunction(getPage,url)
        root='http://www.otaku-attitude.net/launch-download-'
        idepisode = ''
        match=re.compile('fiche = \'(.+?):(.+?)\'').findall(page)
        for typ, id in match: 
            root = root + typ+'-'+id
        print page
        match=re.compile('<tr class="down.+?" id="(.+?)" >        <td class="cell"><strong>(.+?)</strong></td><td class="cell">(.+?)</td><td class="cell">(.+?)</td>').findall(page)
        for link_id,episode, format_video, resolution in match:
            urlvid = root+'-ddl-'+link_id+'.html'
            addLink(htmlDecode(name)+' Ep.'+episode+' (Format:'+format_video+' Reso.:'+resolution.replace('×','x')+')',urlvid,defIcon(icon))
        match=re.compile('<tr class="down.+?" id="(.+?)" ><td class="cell"><strong>(.+?)</strong></td><td class="cell">(.+?)</td><td class="cell">(.+?)</td>').findall(page)
        for link_id,episode, format_video, resolution in match:
            urlvid = root+'-ddl-'+link_id+'.html'
            addLink(htmlDecode(name)+' Ep.'+episode+' (Format:'+format_video+' Reso.:'+resolution.replace('×','x')+')',urlvid,defIcon(icon))

#Specific XBMC
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


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&icon="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        

def addDirPlot(name,url,mode,iconimage,plot):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&icon="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setInfo( type="Video", infoLabels={ "plot": plot } )
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
        INDEX(url)

elif mode==2:
        GROUP(url)

elif mode==3:
        VIDEOLINKS(url,name,icon)



xbmcplugin.endOfDirectory(int(sys.argv[1]))
