import urllib,urllib2,re,xbmcplugin,xbmcgui

#TV DASH - by You 2008.

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
  
def CATEGORIES():
        icon = 'special://home/addons/plugin.video.anime-ultime.net/icon.png'
        addDir('Anime #','http://www.anime-ultime.net/series-0-1/anime/1---#principal',1,icon)
        addDir('Anime A','http://www.anime-ultime.net/series-0-1/anime/a---#principal',1,icon)
        addDir('Anime B','http://www.anime-ultime.net/series-0-1/anime/b---#principal',1,icon)
        addDir('Anime C','http://www.anime-ultime.net/series-0-1/anime/c---#principal',1,icon)
        addDir('Anime D','http://www.anime-ultime.net/series-0-1/anime/d---#principal',1,icon)
        addDir('Anime E','http://www.anime-ultime.net/series-0-1/anime/e---#principal',1,icon)
        addDir('Anime F','http://www.anime-ultime.net/series-0-1/anime/f---#principal',1,icon)
        addDir('Anime G','http://www.anime-ultime.net/series-0-1/anime/g---#principal',1,icon)
        addDir('Anime H','http://www.anime-ultime.net/series-0-1/anime/h---#principal',1,icon)
        addDir('Anime I','http://www.anime-ultime.net/series-0-1/anime/i---#principal',1,icon)
        addDir('Anime J','http://www.anime-ultime.net/series-0-1/anime/j---#principal',1,icon)
        addDir('Anime K','http://www.anime-ultime.net/series-0-1/anime/k---#principal',1,icon)
        addDir('Anime L','http://www.anime-ultime.net/series-0-1/anime/l---#principal',1,icon)
        addDir('Anime M','http://www.anime-ultime.net/series-0-1/anime/m---#principal',1,icon)
        addDir('Anime N','http://www.anime-ultime.net/series-0-1/anime/n---#principal',1,icon)
        addDir('Anime O','http://www.anime-ultime.net/series-0-1/anime/o---#principal',1,icon)
        addDir('Anime P','http://www.anime-ultime.net/series-0-1/anime/p---#principal',1,icon)
        addDir('Anime Q','http://www.anime-ultime.net/series-0-1/anime/q---#principal',1,icon)
        addDir('Anime R','http://www.anime-ultime.net/series-0-1/anime/r---#principal',1,icon)
        addDir('Anime S','http://www.anime-ultime.net/series-0-1/anime/s---#principal',1,icon)
        addDir('Anime T','http://www.anime-ultime.net/series-0-1/anime/t---#principal',1,icon)
        addDir('Anime U','http://www.anime-ultime.net/series-0-1/anime/u---#principal',1,icon)
        addDir('Anime V','http://www.anime-ultime.net/series-0-1/anime/v---#principal',1,icon)
        addDir('Anime W','http://www.anime-ultime.net/series-0-1/anime/w---#principal',1,icon)
        addDir('Anime X','http://www.anime-ultime.net/series-0-1/anime/x---#principal',1,icon)
        addDir('Anime Y','http://www.anime-ultime.net/series-0-1/anime/y---#principal',1,icon)
        addDir('Anime Z','http://www.anime-ultime.net/series-0-1/anime/z---#principal',1,icon)
                       
def INDEX(url):
        root = 'http://www.anime-ultime.net/'
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" onMouseOver="(.+?)" onMouseOut=".+?" style=".+?"><img class="lazy" data-href="(.+?)" alt=".+?" title="(.+?)" /></a>').findall(link)
        for url,pic,thumbnail,name in match:
                pic = pic[17:]
                pic = pic[:pic.rfind(' ')]
                #print pic
                addDir(htmlDecode(name),root+url,2,pic)

def VIDEOLINKS(url,name,icon):
        root = 'http://www.anime-ultime.net/'
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)">(.+?)</a>').findall(link)
        for url2, typ in match:
                if (typ == 'Stream'):
                    matchNum = ' (?)'
                    try:
                            matchNum = ' (Ep.:'+re.findall('-\d\d-',url2)[-1][1:][:-1]+')'
                    except:
                            try:
                                    matchNum = ' (Ep.:'+re.findall('-\d\d_\d-',url2)[-1][1:][:-1].replace('_','.')+')'
                                    pass
                            except:
                                    pass
                    req2 = urllib2.Request(root+url2)
                    req2.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                    response2 = urllib2.urlopen(req2)
                    link2=response2.read()
                    response2.close()
                    match2=re.compile('\'file\': \'(.+?)\'').findall(link2)
                    urlvid = ''
                    for url3 in match2:
                            urlvid = url3
                    if urlvid[len(urlvid)-3:]=='xml':
                           req3 = urllib2.Request(root+urlvid[1:])
                           req3.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                           response3 = urllib2.urlopen(req3)
                           link3=response3.read()
                           response3.close()
                           match3hd=re.compile('<media:content url="(.+?)" duration=".+?" />').findall(link2)
                           for url4 in match3hd:
                                   urlvid = url4[len(root)-1:]
                    addLink(htmlDecode(name+matchNum),root+urlvid[1:],icon)

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
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
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
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        INDEX(url)
        
elif mode==2:
        print ""+url
        VIDEOLINKS(url,name,icon)



xbmcplugin.endOfDirectory(int(sys.argv[1]))
