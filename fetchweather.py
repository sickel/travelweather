from flask import Flask
from flask import request
import urllib
import time
import datetime
import xml.dom.minidom
import pytz
import json
app = Flask(__name__)
app.debug = True

cache=dict()

@app.route("/",methods=['POST', 'GET'])
def getweather():
  # All input musts be validated...
  lat=request.args.get('lat','')
  lon=request.args.get('lon','')
  # Lat and lon can be rounded to make better caching behaviour
  moment=request.args.get('time','')
  # moment must allow for less strict time specification
  url="http://api.met.no/weatherapi/locationforecastlts/1.1/?lat="+lat+";lon="+lon
  
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

if __name__ == "__main__":
    app.run()
