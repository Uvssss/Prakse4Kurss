from urllib.request import urlopen
import json
html = urlopen("https://www.nordpoolgroup.com/api/marketdata/page/59?currency=,,,EUR")
data_json = json.loads(html.read())
print(data_json)
# json_object = json.dumps(data_json, indent=4)
# with open("json/data.json", "w") as outfile:
#     outfile.write(json_object)