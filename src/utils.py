import pandas as pd
import random
import os
from tabulate import tabulate


# Pendifinisian Path untuk setiap file csv
adminsPath = "./databases/admins.csv"
productsPath = "./databases/products.csv"
ordersPath = "./databases/orders.csv"
ordersDetailsPath = "./databases/order_details.csv"


# Membersihkan console untuk CMD atau Terminal
def isFloat(string: str) -> bool:
    try:
        res = float(string)
        return (True if res >= 0 else False)
    except ValueError:
        return False


# check valid or not for phone number indonesia 08xxxx
def checkPhone(phone_number: str) -> bool:
    if not phone_number:
        return False
    if not (phone_number.startswith('08') or phone_number.startswith('+628')):
        return False
    return True


# Membersihkan console untuk CMD atau Terminal


def clearConsole() -> None:
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


# Memodifikasi data pada dataframe
def editData(data: pd.DataFrame, condition: int or pd.Series, column: tuple or list, value: tuple or list, path: str = None) -> pd.DataFrame:
    data.loc[condition, column] = value
    if path is not None:
        data.to_csv(path, index=False)
    return data


# Menambahkan data ke dataframe
def addData(data: pd.DataFrame, newData: dict or pd.DataFrame, path: str = None) -> pd.DataFrame:
    data = pd.concat([data, pd.DataFrame(newData)], ignore_index=True)
    if path is not None:
        data.to_csv(path, index=False)
    return data


# Menghapus data dari dataframe
def deleteData(data: pd.DataFrame, condition: int or pd.Series, path: str = None) -> pd.DataFrame:
    if isinstance(condition, int):
        data = data.drop(condition)
    else:
        data = data.drop(data.loc[condition].index)

    if path is not None:
        data.to_csv(path, index=False)
    return data


# Menghasilkan ID unik random
def generateUniqueId(series: pd.Series or pd.DataFrame, length: int = 7, uppercase: bool = True, prefix: str = "") -> str:
    generator = 'abcdefghijklmnopqrstuvwxyz0123456789'
    while (True):
        result = ''.join(random.choice(generator) for _ in range(length))
        if result not in series:
            return prefix + result.upper() if uppercase else prefix + result


# Fungsi Print dengan custom tampilan
def printCustom(string: str, length: int = 81, char: str = "=", isCenter: bool = True) -> None:
    strings = string.split("\n")

    print("".center(length, char))
    for string in strings:
        print(string.center(length) if isCenter else string)
    print("".center(length, char))


# Menampilkan data dalam bentuk tabel
def printTable(datas: pd.DataFrame, columns: list = None, showIndex: bool = True) -> None:
    data = datas.copy()
    data.columns = [_.replace("_", " ").title() for _ in data.columns]
    columns = data.columns if columns is None else [
        _.replace("_", " ").title() for _ in columns]
    data.fillna("Empty Data", inplace=True)
    data.replace({"-": "Empty Data"}, inplace=True)

    print(tabulate(data[columns], headers='keys', tablefmt='double_outline',
                   showindex=showIndex))


# Mereset index dan memberikan nama baru
def customIndex(df=pd.DataFrame) -> None:
    df.reset_index(drop=True, inplace=True)
    df.index += 1
    df.index.name = "No"


# Mengecek apakah file csv ada atau tidak
def checkCsvFiles(csvc: list) -> None:
    for csvs in csvc:
        for csv, column in csvs.items():
            dirs = csv.split("/")[0:-1]

            bdir = ""
            for dir in dirs:
                if not os.path.exists(bdir + dir):
                    os.mkdir(bdir + dir)
                bdir += dir + "/"
            if not os.path.exists(csv):
                pd.DataFrame(columns=column).to_csv(csv, index=False)


# Mengambil data dari csv dengan memberikan output DataFrame
def getCsvData(path: str, sortColumn: str or list = None, asc: bool or list = [False, True]) -> pd.DataFrame:
    result = pd.read_csv(path)

    sortColumn = [result.columns[-1], result.columns[1]
                  ] if sortColumn is None else sortColumn
    result.sort_values(by=sortColumn, ascending=asc, inplace=True)
    customIndex(result)

    return result
