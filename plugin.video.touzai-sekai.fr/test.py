# This test program is for finding the correct Regular expressions on a page to insert into the plugin template.
# After you have entered the url between the url='here' - use ctrl-v
# Copy the info from the source html and put it between the match=re.compile('here')
# press F5 to run if match is blank close and try again.

import urllib2,urllib,re

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
  text = text.replace("_"," ")
  return text

def htmlEncode(text):
  text = text.replace(" ","+")
  text = text.replace("[","%5B")
  text = text.replace("]","%5D")
  text = text.replace("&","&amp;")
  return text

url = 'http://www.touzai-sekai.fr/telecharger_Blood_C_Episode_01_amatskaze_VostFR.html'
root = 'http://www.touzai-sekai.fr/'
icon = 'special://home/addons/plugin.video.touzai-sekai.fr/icon.png'
req = urllib2.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
response = urllib2.urlopen(req)
link=response.read()
response.close()
match=re.compile('var ip="(.+?)";var rep="(.+?)";var video_name="(.+?)"').findall(link)
for ip,rep,video_name in match:
  urlvid=''
  if ip == '88.190.55.110':
      urlvid='http://stream01.touzai-sekai.fr'
  elif ip == '195.154.237.153':
      urlvid='http://stream02.touzai-sekai.fr'
  else :
      urlvid='http://'+ip
  ext = video_name[-3:]
  print ext
  urlget = 'http://'+ip+'/generate_link3.php?ip='+ip+'&rep='+rep+'&video='+htmlEncode(video_name)
  print urlget
  reqg = urllib2.Request(urlget)
  reqg.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
  responseg = urllib2.urlopen(reqg)
  linkg=responseg.read()
  print linkg
  responseg.close()
  getmatch = re.compile('{"txt":"(.+?)","stream":""}').findall(linkg)
  for path in getmatch:
      path = path.replace('\\/','/')
      if path[-4:][:1]!='.':
          path = path[:path.rfind('/')+1]+video_name
      urlvid=urlvid+path
  print urlvid
    
