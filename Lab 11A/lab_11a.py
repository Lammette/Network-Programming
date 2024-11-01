import urllib.request
import re

# "(ch-\w*).*?schedule.*?\[(.*?)\] Get channel schedule
#{\\"descriptionRaw\\":\\"(?:(.*?))\\",\\"name\W*(.*?)\\.*?subHeading\\":\\"(?:(.*?))\\.*?startTime.*?(\d{2}:\d{2}).*?start.*?(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}) #get programs

req = urllib.request.Request('https://www.svtplay.se/kanaler?date=2024-10-31')
with urllib.request.urlopen(req) as response:
   data = response.read().decode("utf-8")
   tabla = re.findall(r'<td class="svtTablaTime">\s*(\d+\d.\d+)\s*<\/td>\s*<td.*?>\s*<h4.*?>\s*Simpsons\s*<\/h4>\s*.*\s*.* \s*.*\s*.*\s*.*\s*.*?[.]\D*(\d+)\D*(\d+)\D*(\d+)\W*(.*?)[.]', data )
   print(data)