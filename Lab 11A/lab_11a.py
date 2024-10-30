import urllib.request
import re

req = urllib.request.Request('https://www.svtplay.se/kanaler?date=2020-11-01')
with urllib.request.urlopen(req) as response:
   data = response.read().decode("utf-8")
   tabla = re.findall(r'<td class="svtTablaTime">\s*(\d+\d.\d+)\s*<\/td>\s*<td.*?>\s*<h4.*?>\s*Simpsons\s*<\/h4>\s*.*\s*.* \s*.*\s*.*\s*.*\s*.*?[.]\D*(\d+)\D*(\d+)\D*(\d+)\W*(.*?)[.]', data )
   print(data)