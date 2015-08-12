import urllib,urllib2,re,xbmcplugin,xbmcgui
try:
    import StorageServer
except:
    import storageserverdummy as StorageServer
cache = StorageServer.StorageServer("plugin.video.touzai-sekai", 24) # (Your plugin name, Cache time in hours)

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
  
def htmlEncode(text):
  text = text.replace(" ","+")
  text = text.replace("[","%5B")
  text = text.replace("]","%5D")
  text = text.replace("!","%21")
  text = text.replace("&","&amp;")
  return text
  
def htmlEncodeUrl(text):
  text = text.replace(" ","%20")
  text = text.replace("[","%5B")
  text = text.replace("]","%5D")
  text = text.replace("!","%21")
  text = text.replace("&","&amp;")
  return text

def fixUrl(url):
  root = 'http://www.touzai-sekai.fr/'
  if url[:1] == '"':
      url = url.replace('"','')
  if url[:1] == '\'':
      url = url.replace('\'','')
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
      return ''

def CATEGORIES():
        icon = 'special://home/addons/plugin.video.touzai-sekai.fr/icon.png'
        root = 'http://www.touzai-sekai.fr/'
        link=cache.cacheFunction(getPage,root)
        match=re.compile('<li><a href="(.+?)">Anime (.+?)</a></li>').findall(link)
        for url,name in match:
                url=url[:url.find('"')]
                if name.find('</li>')==-1:
                    addDir(htmlDecode('Anime '+name),url+'.1',1,icon)
                       
def INDEX(url):
        pagenum = url[url.rfind('.')-len(url)+1:]
        root = 'http://www.touzai-sekai.fr/'
        icon = 'special://home/addons/plugin.video.touzai-sekai.fr/icon.png'
        link=cache.cacheFunction(getPage,url)
        match=re.compile('<div class=info><a class=nameA href=(.+?) style=\'color:#353535;text-align:center;\'>(.+?)</a><span class=ellipsis></span></div>').findall(link)
        for url2,name in match:
            link2=cache.cacheFunction(getPage,url2)
            picture = re.compile('<img class=imgA src=\'(.+?)\' .+? />').findall(link2)
            img=''
            for urlimg in picture:
                    img =  urlimg
            addDir(name,root+url2,2,img)
        if link.find('prevnext_right')>0 and link.find('prevnext_right disabled')<0:
            addDir('Page '+str(int(pagenum) + 1),url[:url.rfind('.')+1]+str(int(pagenum) + 1),1,icon)

def VIDEOLINKS(url,name,icon):
        root = 'http://www.touzai-sekai.fr/'
        link=cache.cacheFunction(getPage,url)
        link = link[link.find('<div id=liens_ep>'):]
        link = link[:link.find('</div>')]
        match=re.compile('<a href=(.+?)>(.+?)</a>').findall(link)
        for url2,name in match:
            link2=cache.cacheFunction(getPage,url2)
            match2=re.compile('var ip="(.+?)";var rep="(.+?)";var video_name="(.+?)"').findall(link2)
            for ip,rep,video_name in match2:
                    print 'Add Video:'+htmlDecode(video_name)
                    urlvid=''
                    if ip == '88.190.55.110':
                            urlvid='http://stream01.touzai-sekai.fr'
                    elif ip == '195.154.237.153':
                            urlvid='http://stream02.touzai-sekai.fr'
                    else :
                            urlvid='http://'+ip
                    urlget = 'http://'+ip+'/generate_link3.php?ip='+ip+'&rep='+rep+'&video='+htmlEncode(video_name)
                    linkg=getPage(urlget)
                    ext = video_name[:-3]
                    getmatch = re.compile('{"txt":"(.+?)","stream":"(.+?)"}').findall(linkg)
                    for path,path2 in getmatch:
                            if path2 != '':
                                path = path2
                            print 'Add Path:'+path
                            path = path.replace('\\/','/')
                            if path[-4:][:1]!='.':
                                path = path[:path.rfind('/')+1]+video_name
                            urlvid=urlvid+path
                            addLink(htmlDecode(name),htmlEncodeUrl(urlvid),icon)
                    getmatch = re.compile('{"txt":"(.+?)","stream":""}').findall(linkg)
                    for path in getmatch:
                            print 'Add Path:'+path
                            path = path.replace('\\/','/')
                            if path[-4:][:1]!='.':
                                path = path[:path.rfind('/')+1]+video_name
                            urlvid=urlvid+path
                            addLink(htmlDecode(name),htmlEncodeUrl(urlvid),icon)

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
