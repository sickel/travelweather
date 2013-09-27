from flask import Flask
from flask import request
import urllib
import xml.dom.minidom
# import xml.etree.ElementTree as ET
import json
app = Flask(__name__)
app.debug = True

@app.route("/",methods=['POST', 'GET'])
def hello():
  lat=request.args.get('lat','')
  lon=request.args.get('lon','')
  time=request.args.get('time','')
  url="http://api.met.no/weatherapi/locationforecastlts/1.1/?lat="+lat+";lon="+lon

  f = urllib.urlopen(url)
  # Check for valid response
  dom=xml.dom.minidom.parseString(f.read())
  timenodes=dom.getElementsByTagName('time')
  for tnode in timenodes:
    if tnode.getAttribute('from')==time:
        nodes=tnode.getElementsByTagName('temperature')
        if len(nodes)>=1:
           temperature=nodes[0].getAttribute('value')
        nodes=tnode.getElementsByTagName('cloudiness')
        if len(nodes)>=1:
           clness=nodes[0].getAttribute('percent')
  return json.dumps({'temp' : temperature, 'lat':lat,'lon':lon,'time':time,'cloudiness':clness})

if __name__ == "__main__":
    app.run()
