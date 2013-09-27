from flask import Flask, render_template
from flask import request
import urllib
import time
import datetime
import xml.dom.minidom
import pytz
import json
import re
app = Flask(__name__)
app.debug = True

cache=dict()

@app.route("/ajaxserver",methods=['POST', 'GET'])
def getweather():
#  
#    All input musts be validated...
#
  lat=request.args.get('lat','')
  lon=request.args.get('lon','')
  position=request.args.get('pos','')
  m=re.match('(.*)N (.*)E',position)
  if m:
      lat=m.group(1)
      lon=m.group(2)
  # Lat and lon can be rounded to make better caching behaviour
  moment=request.args.get('timestamp','')
  time=request.args.get('time','')
  date=request.args.get('date','')
  #if(moment==''):
  moment=date+'T'+time+'Z'    
  print moment
  # moment must allow for less strict time specification
  url="http://api.met.no/weatherapi/locationforecastlts/1.1/?lat="+lat+";lon="+lon
  print url
  # Checks if url is cached and still not has timed out
  if (url in cache) and (cache[url+"time"]>datetime.datetime.now(pytz.utc)):
      dom=cache[url]
      storage="Cached"
  else:
      f = urllib.urlopen(url)
      info=f.info()
      exhead=''.join(info.getfirstmatchingheader('Expires')).split(': ')
      extime=exhead[1].rstrip()
      # Caches the expiration time as a UTC-time-object 
      cache[url+'time']=pytz.utc.localize(datetime.datetime.strptime(extime,"%a, %d %b %Y %H:%M:%S %Z"))
      # Check for valid response
      dom=xml.dom.minidom.parseString(f.read())
      cache[url]=dom
      storage="Fetching"
  timenodes=dom.getElementsByTagName('time')
  temperature=''
  clness=''
  for tnode in timenodes:
      # Looks for a node with the correct time
      if tnode.getAttribute('from')==moment:
        nodes=tnode.getElementsByTagName('temperature')
        if len(nodes)>=1:
           temperature=nodes[0].getAttribute('value')
        nodes=tnode.getElementsByTagName('cloudiness')
        if len(nodes)>=1:
           clness=nodes[0].getAttribute('percent')
  return json.dumps({'temp' : temperature, 'lat':lat,'lon':lon,'time':moment,'cloudiness':clness,'st':storage})

@app.route("/")
def home():
    return render_template('home.html')



if __name__ == "__main__":
    app.run(host='0.0.0.0')
