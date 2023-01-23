#  I need an if statement to check if data index is 0 to get todays data.
#  for all data stuff

from urllib.request import urlopen
import json
html = urlopen("https://www.nordpoolgroup.com/api/marketdata/page/59?currency=,,,EUR")
data_json = json.loads(html.read())
for index in range(1,len(data_json["data"]["Rows"])):
  sSplit=data_json["data"]["Rows"][index]["StartTime"].split("T")
  eSplit=data_json["data"]["Rows"][index]["EndTime"].split("T")
  sSplit=data_json["data"]["Rows"][index]["StartTime"].replace('T', ' ')
  eSplit=data_json["data"]["Rows"][index]["EndTime"].replace('T', ' ')  
    print(sSplit+" - "+eSplit+"  Value: "+data_json["data"]["Rows"][index]["Columns"][1]["Value"]+" EUR")
