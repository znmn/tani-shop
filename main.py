from src.admin import *
from src.product import *
from src.transaction import *


def main():
    # Mengecek apakah file-file csv sudah ada
    checkCsvFiles([{adminsPath: ['admin_id', 'nama', 'username', 'password', 'is_super',
                                 'no_hp', 'alamat', 'active']},
                   {productsPath: ['product_id', 'nama_produk',
                                   'harga_per_kg', 'stok_kg', 'out_kg', 'is_hidden']},
                   {ordersPath: ['order_id', 'tanggal_order',
                                 'admin_id', 'bayar', 'kembalian']},
                   {ordersDetailsPath: ['order_id', 'product_id', 'harga_per_kg', 'quantity_kg']}])

    # Memperbarui data-data csv
    renewAdminsData(), renewProductsData(), renewTransactionsData()

    clearConsole()
    printCustom(" Selamat Datang di TaniShop ")
    firstStart()  # Cek apakah pertama dijalankan

    isLogin, isSuper, loginData = loginAdmin()  # Login

    clearConsole()
    printCustom(
        f"[I] Selamat Datang: {loginData['nama'].values[0]}\n" +
        f"[I] Kamu Login Sebagai: {'Super Admin' if isSuper else 'Admin'}\n" +
        f"[I] ID Admin: {loginData['admin_id'].values[0]}", char='-', isCenter=False)
    input("[!] Tekan Enter untuk melanjutkan...")

    clearConsole()
    while (isLogin):
        if isSuper:
            printCustom(" Menu Utama Super Admin ")
            printCustom(
                "[1] Tambah Admin\n" +
                "[2] Edit dan Lihat Admin\n" +
                "[3] Hapus Admin\n" +
                "[4] Tambah Produk Baru\n" +
                "[5] Edit dan Lihat Produk\n" +
                "[6] Sembunyikan/Tampilkan Produk\n" +
                "[7] Manage Stok\n" +
                "[8] Riwayat Seluruh Transaksi\n" +
                "[0] Logout \n" +
                "[X] Exit", char="-", isCenter=False)

            choice = input("[?] Masukkan Pilihan: ")

            clearConsole()
            if choice == '1':
                modifyAdmin('tambah')
            elif choice == '2':
                modifyAdmin('edit')
            elif choice == '3':
                isLogin, isSuper, loginData = modifyAdmin('hapus')
            elif choice == '4':
                modifyProduct('tambah')
            elif choice == '5':
                modifyProduct('edit')
            elif choice == '6':
                modifyProduct('sembunyikan')
            elif choice == '7':
                modifyProduct('stok')
            elif choice == '8':
                myTransactions()
            elif choice == '0':
                isLogin, isSuper, loginData = logoutAdmin()
            elif choice.casefold() == 'x':
                clearConsole()
                exit()
            else:
                printCustom(
                    " !Pilihan Tidak Ditemukan! \n !Silahkan Pilih Menu Yang Tersedia! ", char='-')
        else:
            printCustom(" Menu Utama Admin ")
            printCustom(
                "[1] Transaksi Baru\n" +
                "[2] Riwayat Transaksi Yang ditangani Saya\n" +
                "[0] Logout \n" +
                "[X] Exit", char="-", isCenter=False)
            choice = input("[?] Masukkan Pilihan: ")

            clearConsole()
            if choice == '1':
                newTransaction()
            elif choice == '2':
                myTransactions(
                    loginData['admin_id'].values[0])
            elif choice == '0':
                isLogin, isSuper, loginData = logoutAdmin()
            elif choice.casefold() == 'x':
                clearConsole()
                exit()
            else:
                printCustom(
                    " !Pilihan Tidak Ditemukan! \n !Silahkan Pilih Menu Yang Tersedia! ", char='-')

        input("[I] Tekan Enter Untuk Melanjutkan...")
        clearConsole()
    main()


main()
