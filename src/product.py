from .utils import *

productsData = pd.DataFrame()


def renewProductsData():
    global productsData

    productsData = getCsvData(productsPath)


def getProducts() -> pd.DataFrame:
    return productsData


def modifyProduct(action: str) -> None:
    global productsData

    def success(prompt: str, name: str, price: int, stock: int, is_hidden: bool) -> None:
        renewProductsData()
        clearConsole()

        printCustom(
            f" Berhasil {prompt.title()} Data Product ")
        printCustom(f"[I] Nama Produk: {name}" +
                    f"\n[I] Harga (per-Kg): {price}" +
                    f"\n[I] Stok (Kg): {stock}" +
                    f"\n[I] Sembunyikan: {is_hidden}", char='-', isCenter=False)

    printCustom(
        f" {'Sembunyikan/Tampilkan' if action == 'sembunyikan' else action.title()} Produk ")
    if action == 'edit' or action == 'sembunyikan' or action == 'stok':
        printTable(productsData, ['nama_produk',
                   'harga_per_kg', 'stok_kg', 'is_hidden'])
        totalStock = productsData['stok_kg'].sum()

        printCustom(f"[=] Total Stok Seluruh Product: {totalStock}")
        printCustom("[X] Kembali   [NO] Pilih Nomor Produk")
        while True:
            productIdx = input("[?] Pilih Produk: ")
            if productIdx in productsData.index.map(str):
                break
            elif productIdx.casefold() == 'x':
                return

        productIdx = int(productIdx)
        productData = productsData.loc[[productIdx]]
        productId = productData['product_id'].values[0]
    else:
        print('[X] Isi dengan X untuk Membatalkan')

    if action == 'edit' or action == 'tambah':
        if action == 'tambah':
            productId = generateUniqueId(
                productsData['product_id'], prefix='P-')

        while True:
            productName = input(
                "[?] Nama Produk Baru: ") or (productData['nama_produk'].values[0] if action == 'edit' else "")
            if productName.casefold() == 'x':
                return
            elif action == 'edit' and productName == productData['nama_produk'].values[0]:
                break
            elif not productsData['nama_produk'].str.casefold().eq(productName.casefold()).any() and productName != "":
                break
            else:
                print("[I] Nama Produk Sudah Terdaftar!")
        while True:
            productPrice = input(
                "[?] Harga (per-Kg): ") or (str(productData['harga_per_kg'].values[0]) if action == "edit" else "")
            if productPrice.isnumeric():
                productPrice = int(productPrice)
                break
        while True:
            productStock = input(
                "[?] Stok (Kg): ") or (str(productData['stok_kg'].values[0]) if action == "edit" else "")
            if isFloat(productStock):
                productStock = float(productStock)
                break

        stock_out = productData['out_kg'].values[0] if action == 'edit' else 0
        is_hidden = productData['is_hidden'].values[0] if action == 'edit' else False

        newProduct = pd.DataFrame({
            'product_id': productId,
            'nama_produk': productName,
            'harga_per_kg': productPrice,
            'stok_kg': productStock,
            'out_kg': stock_out,
            'is_hidden': is_hidden
        }, index=[0])

        if action == 'edit':
            productsData = editData(
                productsData, productsData['product_id'] == productId, newProduct.keys(), newProduct.values, productsPath)
        else:
            productsData = addData(productsData, newProduct, productsPath)

        success(action.title(), productName, productPrice, productStock, False)
    elif action == 'sembunyikan':
        productData['is_hidden'] = not productData['is_hidden'].values[0]
        productsData = editData(
            productsData, productsData['product_id'] == productId, productData.keys(), productData.values, productsPath)

        success('Sembunyikan/Tampilkan', productData['nama_produk'].values[0], productData['harga_per_kg'].values[0],
                productData['stok_kg'].values[0], productData['is_hidden'].values[0])
    elif action == 'stok':
        while True:
            productStock = input(
                "[?] Stok: ") or productData['stok_kg'].values[0]
            if isFloat(productStock):
                productStock = float(productStock)
                break

        productsData = editData(
            productsData, productsData['product_id'] == productId, ('stok_kg'), (productStock), productsPath)

        success('Edit Stok', productData['nama_produk'].values[0], productData['harga_per_kg'].values[0],
                productStock, productData['is_hidden'].values[0])
    else:
        printCustom(" Action not Found ")
        return
