import pandas as pd
import xlrd
import string

def readExcelFiles():
    path = './data/'
    filename = "Image Dataset Map.xlsx"

    xl = pd.ExcelFile(path + filename)

    sheets = xl.sheet_names

    excelSheets = {}

    for sheet in sheets:
        excelSheets[sheet] = xl.parse(sheet, header=None)
        excelSheets[sheet].index += 1
        excelSheets[sheet].columns = map(lambda x: string.ascii_lowercase[x], excelSheets[sheet].columns)

    return excelSheets
    # print excelSheets["Grid 1"]
    # print excelSheets["Grid 1"]['a']
    # print excelSheets["Grid 1"]['a'][1]