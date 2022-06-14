import pandas as pd


def readData():
    filename = "productos.csv"
    data = pd.read_csv(filename,
                       names=["product name", "price", "company", "category"])

    return data


def splitProvider(data, cell):
    #Separamos la informacion en la fila, en el caso de proveedores que consisten en dos palabras o más como "Tía Rosa" lo consideramos como una sola palabra
    bank = []
    bankList = []
    for index, row in data.iterrows():
        bankList.append(row[cell])
        if row[cell] not in bank:
            bank.append(row[cell])
    #print("\nLista de los proveedores \n")
    #print(provBank)
    #print("\nLa lista que se usara para contar\n\n", provBankList)

    return bank, bankList


def name_(data):
    #Separación de la lista de nombres del producto en bancos de palabras
    wordBank = []
    for index, row in data.iterrows():
        wordBank.append(row[0].split())
    #print("BANK\n", wordBank)

    bankList = [word for sublist in wordBank for word in sublist]

    #print("\nWordBankFlatten\n")
    #print(bankList)

    bank = []
    for word in bankList:
        #print(word)
        if word not in bank:
            bank.append(word)

    #print(bank)
    #print("\n")

    return bank, bankList


def frecuencia(data):
    cat = []
    for index, row in data.iterrows():
        if row[3] not in cat:
            cat.append(row[3])

    #print(cat)

    pCat = pd.DataFrame(0, columns=[cat], index=["p(Ck)"])
    pCatCount = pd.DataFrame(0, columns=[cat], index=["p(Ck)"])

    #print(pCat)

    for index, row in data.iterrows():
        for categoria in cat:
            if row[3] == categoria:
                pCat[categoria] = pCat[categoria] + 1
                pCatCount[categoria] = pCatCount[categoria] + 1

    for categoria in cat:
        pCat[categoria] = pCat[categoria] / len(data)

    #print("\nDataframe con la frecuencia de la clase k entre el total de ejemplos con los que contamos\n")
    #print(pCat)
    #print("\n")
    #print(pCatCount)

    return cat, pCat, pCatCount


def frecuenciaXCat(data, cat, pCatCount, bank, bankList, splitPerWord):
    #Creación de tabla de frecuencias por proveedores en cada clase
    probMatrix = pd.DataFrame(0, columns=[cat], index=[bank])
    #print(probMatrix)

    if splitPerWord == True:
        for index, row in data.iterrows():
            temp = row[0].split()
            tempCat = row[3]
            for word in temp:
                probMatrix.loc[word,
                               tempCat] = probMatrix.loc[word, tempCat] + 1
    else:
        for index, row in data.iterrows():
            temp = bankList[index]
            tempCat = row[3]
            probMatrix.loc[temp, tempCat] = probMatrix.loc[temp, tempCat] + 1

    #print("\nDataframe con las frecuencias de palabra por clase\n")
    #print(probMatrix)
    #print("\n")

    #print(bank)
    for word in bank:
        for categoria in cat:
            #print(probMatrix.loc[word, categoria])
            #print(pCatCount[categoria])
            probMatrix.loc[word,
                           categoria] = probMatrix.loc[word, categoria] / (
                               pCatCount[categoria]).iloc[0][0]

    #print(probMatrix)

    return probMatrix


def probXCat(nameMatrix, name, cat, bank, splitPerWord):
    pxCat = pd.DataFrame(1, columns=[cat], index=["p(Xi|Ck)"])

    if splitPerWord == True:
        product = name.split()
    else:
        product = name

    for word in bank:
        for categoria in cat:
            if word in product:
                #print(pxCat[categoria])
                pxCat[categoria] = pxCat[categoria] * (
                    nameMatrix.loc[word, categoria]).iloc[0][0]

    #print(pxCat)
    return pxCat


def clasificar(probName, probPrecio, probProv, cat, pCat):
    mxCat = pd.DataFrame(1, columns=[cat], index=["m(Xi)"])
    suma = 0
    for categoria in cat:
        #print(probName[categoria])
        #print(probPrecio[categoria])
        #print(probProv[categoria])
        if (probName[categoria]).iloc[0][0] != 0:
            mxCat[categoria] = (pCat[categoria]).iloc[0][0] * (
                probName[categoria]).iloc[0][0]
        if (probPrecio[categoria]).iloc[0][0] != 0:
            mxCat[categoria] = (mxCat[categoria]).iloc[0][0] * (
                probPrecio[categoria]).iloc[0][0]
        if (probProv[categoria]).iloc[0][0] != 0:
            mxCat[categoria] = (mxCat[categoria]).iloc[0][0] * (
                probProv[categoria]).iloc[0][0]

    for categoria in cat:
        if (mxCat[categoria]).iloc[0][0] != 1:
            suma = suma + (mxCat[categoria]).iloc[0][0]

    categoriaSug = []
    res = 0
    i = 0
    for categoria in cat:
        #print(mxCat[categoria])
        if (mxCat[categoria]).iloc[0][0] != 1:
            res = (mxCat[categoria]).iloc[0][0] / suma
            if res > i:
                categoriaSug = categoria
                i = res
            elif res == i:
                categoriaSug.append(categoria)

    #print(suma)
    #print(mxCat)
    print(categoriaSug)



import sys
def main():

    if len(sys.argv) != 4:
        exit()
       
    data = readData()
    cat, pCat, pCatCount = frecuencia(data)

    # Calculos para la fila de nombre
    nameBank, nameBankList = name_(data)
    splitPerWord = True
    nameProbMatrix = frecuenciaXCat(data, cat, pCatCount, nameBank,
                                    nameBankList, splitPerWord)
    # name = input("Escribe el nombre del producto: ")
    name = sys.argv[1]
    namePxCat = probXCat(nameProbMatrix, name, cat, nameBank, splitPerWord)

    # Calculos para la fila del precio
    precioIndex = 1
    precioBank, precioBankList = splitProvider(data, precioIndex)
    splitPerWord = False
    precioProbMatrix = frecuenciaXCat(data, cat, pCatCount, precioBank,
                                      precioBankList, splitPerWord)
            
    # precio = input("Escribe el precio del producto: ")
    precio = sys.argv[2]
    precioPxCat = probXCat(precioProbMatrix, precio, cat, precioBank,
                           splitPerWord)

    # Calculos para la fila del proveedor
    provIndex = 2
    provBank, provBankList = splitProvider(data, provIndex)
    splitPerWord = False
    provProbMatrix = frecuenciaXCat(data, cat, pCatCount, provBank,
                                    provBankList, splitPerWord)

    
    # proveedor = input("Escribe el proveedor del producto: ")
    proveedor = sys.argv[3]
    provPxCat = probXCat(provProbMatrix, proveedor, cat, provBank,
                         splitPerWord)

    clasificar(namePxCat, precioPxCat, provPxCat, cat, pCat)


main()