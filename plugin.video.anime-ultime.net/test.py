# This test program is for finding the correct Regular expressions on a page to insert into the plugin template.
# After you have entered the url between the url='here' - use ctrl-v
# Copy the info from the source html and put it between the match=re.compile('here')
# press F5 to run if match is blank close and try again.

import urllib2,urllib,re

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
                        streamNum = '0'
                        try:
                                streamNum = url2[url2.find('/')+1:]
                                streamNum = streamNum[:streamNum.find('-')]
                        except:
                                pass
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
                        print 'Name='+htmlDecode(name+matchNum)
                        print root+urlvid[1:]
                        

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


root = 'http://www.anime-ultime.net/'
url='http://www.anime-ultime.net/series-0-1/anime/1---#principal'

req = urllib2.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
response = urllib2.urlopen(req)
link=response.read()
response.close()
match=re.compile('<a href="(.+?)" onMouseOver=".+?" onMouseOut=".+?" style=".+?"><img class="lazy" data-href="(.+?)" alt=".+?" title="(.+?)" /></a>').findall(link)
for url,thumbnail,name in match:
        VIDEOLINKS(root+url,name,thumbnail)
                
