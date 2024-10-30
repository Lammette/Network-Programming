import re
f = open(r"Lab 10\tabla.html",encoding="utf-8")
txt = f.read()

tabla = re.findall(r'<td class="svtTablaTime">\s*(\d+\d.\d+)\s*<\/td>\s*<td.*?>\s*<h4.*?>\s*Simpsons\s*<\/h4>\s*.*\s*.* \s*.*\s*.*\s*.*\s*.*?[.]\D*(\d+)\D*(\d+)\D*(\d+)\W*(.*?)[.]', txt )

for i in tabla:
    print("--------------------")
    print(f"Tid:\t{i[0]}")
    print(f"Säsong:\t{i[1]}")
    print(f"Avsnitt:{i[2]}/{i[3]}")
    print(f"Handling: {i[4]}")