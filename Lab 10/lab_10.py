import re
f = open(r"Lab 10\tabla.html",encoding="utf-8")
txt = f.read()

tabla = re.findall(r'<td class="svtTablaTime">\s*(\d+\d.\d+)\s*<\/td>\s*<td.*?>\s*<h4.*?>\s*Simpsons\s*<\/h4>\s*.*\s*.* \s*.*\s*.*\s*.*\s*.*?[.]\D*(\d+)\D*(\d+)\D*(\d+)\W*(.*?)[.]', txt )

for i in range(0,len(tabla)):
    print("--------------------")
    print(f"Tid:\t{tabla[i][0]}")
    print(f"Säsong:\t{tabla[i][1]}")
    print(f"Avsnitt:{tabla[i][2]}/{tabla[i][3]}")
    print(f"Handling: {tabla[i][4]}")