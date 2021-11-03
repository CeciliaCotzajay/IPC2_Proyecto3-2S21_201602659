# cadena = "cadena otra"
# copia = cadena.replace("\n","")
# copia2 = copia.replace("\t","")
# print("cadenaVefificada********************:", copia2)
# c ="100"
# e ="12"
# g = float(c)*float(e)
# # print(round(g,2))
# print("{0:.2f}".format(g))

# a = ["a","b","c","d","e","f"]
#
# for l in a:
#     if l == "c":
#         pass
#     else:
#         print(l)

# palabra = "123456k"
# listaCaracter = []
# for l in palabra:
#     listaCaracter.append(l)
# print(listaCaracter)

# nit = '8338817'
# listaCaracter = []
# for c in nit:
#     listaCaracter.append(c)
# tam = len(listaCaracter)
# pos = 0
# paso1 = 0
# while tam > 1:
#     paso1 += int(listaCaracter[pos]) * tam
#     tam -= 1
#     pos += 1
# paso3 = paso1 % 11
# paso4 = 11-paso3
# paso5 = paso4 % 11
# ultimoCaracter = listaCaracter.pop()
# if paso5 == 10:
#     if ultimoCaracter == 'K' or ultimoCaracter == 'k':
#         print(False)
#     else:
#         print(True)
# else:
#     if paso5 == int(ultimoCaracter):
#         print(False)
#     else:
#         print(True)
# print(ultimoCaracter)

cantFac_Correctas = 312
tex = str(cantFac_Correctas)
cerosRestantes = 8 - len(tex)
print(cerosRestantes)