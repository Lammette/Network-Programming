import re
f = open(r"Lab 10\tabla.html",encoding="utf-8")
txt = f.read()

print(re.findall(r'<td class="svtTablaTime">\s*(\d+\.\d+)\s*</td>', txt))