from .utils import *
from datetime import datetime as dt
from .product import *
from .admin import *

ordersData = adminsData = productsData = pd.DataFrame()


# Memperbarui semua data transaksi
def renewTransactionsData() -> None:
    global ordersData, adminsData, productsData

    adminsData = getCsvData(adminsPath)
    productsData = getCsvData(productsPath)
    orders = getCsvData(ordersPath)
    orderDetails = getCsvData(ordersDetailsPath)

    orders_orderDetails = pd.merge(orders, orderDetails, on='order_id')
    orders_orderDetails_products = pd.merge(
        orders_orderDetails, productsData[['product_id', 'nama_produk']], on='product_id')

    ordersData = pd.merge(orders_orderDetails_products,
                          adminsData[['admin_id', 'nama']], on='admin_id')

    ordersData['total_harga'] = ordersData['harga_per_kg'] * \
        ordersData['quantity_kg']
    ordersData['total_harga'] = ordersData['total_harga'].astype(int)
    ordersData['total'] = ordersData.groupby(
        ['order_id'])['total_harga'].transform('sum')

    ordersData.sort_values(by=('tanggal_order'),
                           ascending=(True), inplace=True)
    customIndex(ordersData)


# Membuat transaksi baru
def newTransaction() -> None:

    renewTransactionsData()
    cart, productsAvaliable = [], productsData.query('is_hidden == False')

    customIndex(productsAvaliable)

    printCustom(f" Transaksi Baru ")

    if productsAvaliable.empty:
        printCustom("[!] Tidak Ada Produk Yang Tersedia!")
        return

    printTable(productsAvaliable, [
               'nama_produk', 'harga_per_kg', 'stok_kg'])

    printCustom('[X] Transaksi Selesai   [NO] Pilih Produk')
    while True:
        productIdx = input("[?] Silahkan Pilih Produk: ")
        if productIdx.casefold() == 'x':
            break
        if productIdx.isnumeric():
            if productIdx not in productsAvaliable.index.astype(str):
                continue
        else:
            continue

        productIdx = int(productIdx)
        productData = productsAvaliable.loc[[productIdx]]
        productId, productName, productPrice, productStock, productOut, productHidden = productData.values[
            0]

        if productId in [x['id_produk'] for x in cart]:
            print("[I] Produk sudah ada di keranjang! ")
            continue

        while True:
            qty = input("[?] Jumlah (Kg): ")
            if isFloat(qty):
                qty = float(qty)
                if qty <= productStock:
                    break
                else:
                    print(
                        f"[!] Stok Tidak Mencukupi! (Stok: {productStock} Kg)")

        totalPrice = int(productPrice * qty)
        cart.append({
            "id_produk": productId,
            "nama_produk": productName,
            "harga_int": productPrice,
            "jumlah": qty,
            "total_harga_int": totalPrice,
            "stok_baru": productStock - qty,
            "out_baru": productOut + qty
        })

        printCustom(f" Produk {productName} [{qty} Kg] Berhasil Ditambahkan! ")

    if len(cart) < 1:
        printCustom(" !Keranjang Kosong! ")
        return
    cart = pd.DataFrame(cart)

    customIndex(cart)

    cart['total_harga'] = 'Rp. ' + \
        cart['total_harga_int'].apply(lambda x: f"{x:,}".replace(',', '.'))
    cart['harga'] = 'Rp. ' + \
        cart['harga_int'].apply(lambda x: f"{x:,}".replace(',', '.'))

    totalAllPrice = cart['total_harga_int'].sum()

    clearConsole()

    printCustom(" Keranjang Belanja ")
    printTable(cart, [
        'nama_produk', 'harga', 'jumlah', 'total_harga'])

    printCustom("[X] Membatalkan Transaksi   [$] Nominal Bayar")
    print("".center(81, '-'))
    print(
        f"[=] Total Harga yang Harus dibayar: Rp. {totalAllPrice:,}".replace(',', '.'))

    while True:
        bayar = input(f"[?] Bayar: Rp. ")
        if bayar.isnumeric():
            bayar = int(bayar)
            if bayar >= totalAllPrice:
                break
            else:
                print("[!] Uang Tidak Mencukupi! ")
        elif bayar.casefold() == 'x':
            printCustom(" !Transaksi Dibatalkan! ")
            return

    kembalian = bayar - totalAllPrice
    print(f'[=] Kembalian: Rp. {kembalian:,}'.replace(',', '.'))
    print("".center(81, '-'))

    struk = inputTransaction(cart, totalAllPrice, bayar, kembalian)
    renewTransactionsData()
    printCustom(f" !Transaksi Berhasil [{struk}]! ")


# Memodifikasi stok produk
def updateStock(productId: str, productStock: int, stockOut: int = None, path: str = productsPath) -> None:
    global productsData

    stockOut = stockOut if stockOut is not None else productsData.loc[
        productsData['product_id'] == productId]['out_kg'].values[0]

    productsData = editData(
        productsData, productsData['product_id'] == productId, ('stok_kg', 'out_kg'), (productStock, stockOut), path)


# Memasukkan data transaksi
def inputTransaction(orders: list or pd.DataFrame, total: int, bayar: int, kembalian: int, ordersFile: str = ordersPath, orderDetailsFile: str = ordersDetailsPath) -> None:
    loginData = getLogin()

    if isinstance(orders, list):
        orders = pd.DataFrame(orders)
    orders.rename(columns={'id_produk': 'product_id',
                  'harga_int': 'harga_per_kg', 'jumlah': 'quantity_kg'}, inplace=True)

    ordersData = pd.read_csv(ordersFile)
    ordersDetailsData = pd.read_csv(orderDetailsFile)

    orderId = generateUniqueId(ordersData['order_id'], prefix='OD-')
    orders['order_id'] = orderId

    newOrders = {
        'order_id': [orderId],
        'admin_id': [loginData['admin_id'].values[0]],
        'tanggal_order': [dt.now().strftime('%Y-%m-%d %H:%M')],
        'bayar': [bayar],
        'kembalian': [kembalian]
    }
    for i, order in orders.iterrows():
        updateStock(order['product_id'],
                    order['stok_baru'], order['out_baru'])
    ordersData = addData(ordersData, newOrders, ordersFile)
    ordersDetailsData = addData(
        ordersDetailsData, orders[[
            'order_id', 'product_id', 'harga_per_kg', 'quantity_kg']], orderDetailsFile)

    return orderId


# Menampilkan data transaksi
def myTransactions(adminId: str = None) -> None:
    global ordersData
    loginData = getLogin()

    df = ordersData.copy()
    df = df[~df['order_id'].duplicated(keep='first')]
    if adminId is None:
        printCustom(" Data Transaksi Seluruh Admin ")
        customIndex(df)
        df.rename(columns={'nama': 'nama_admin'}, inplace=True)
        printTable(df, ['order_id', 'tanggal_order',
                   'nama_admin', 'total', 'bayar', 'kembalian'])
    else:
        df = df.query(f'`admin_id` == "{adminId}"')
        customIndex(df)
        printCustom(
            f' Data Transaksi Yang ditangani {loginData["nama"].values[0]} ')
        printTable(df, ['order_id', 'tanggal_order',
                   'nama', 'total', 'bayar', 'kembalian'])

    printCustom(
        f' [X] Kembali   [NO] Detail Transaksi (No)   [ID] Detail Transaksi (Order ID)')
    while True:
        dfIdx = input("[?] Pilih Transaksi: ")
        if dfIdx.casefold() == 'x':
            return
        elif df['order_id'].eq(dfIdx.upper()).any():
            dfData = df[df['order_id'] == dfIdx.upper()]
            break
        elif dfIdx.isnumeric():
            dfIdx = int(dfIdx)
            if dfIdx in df.index:
                dfData = df.loc[[dfIdx]]
                break

    dfDataId = dfData['order_id'].values[0]

    dfDetail = ordersData.query(f'`order_id` == "{dfDataId}"')
    dfIDAdmin = dfDetail['admin_id'].values[0]
    dfTotal = f'{dfDetail["total"].values[0]:,}'.replace(',', '.')
    dfBayar = f'{dfDetail["bayar"].values[0]:,}'.replace(',', '.')
    dfKembalian = f'{dfDetail["kembalian"].values[0]:,}'.replace(',', '.')

    customIndex(dfDetail)
    clearConsole()

    printCustom(f" Detail Transaksi [{dfDataId}] ")
    printTable(dfDetail, ['nama_produk', 'harga_per_kg',
               'quantity_kg', 'total_harga'])
    print(f"[+] ID Admin yang Menangani : {dfIDAdmin} ")
    print(f"[+] Total : Rp. {dfTotal} ")
    print(f"[+] Bayar: Rp. {dfBayar}")
    print(f"[+] Kembalian: Rp. {dfKembalian}")

    ret = input("\n[?] Cek Transaksi Lain [Y/N]: ").casefold() == 'y'
    if ret:
        clearConsole()
        myTransactions(adminId)
    else:
        return
