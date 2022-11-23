from .utils import *

# Pendifinisian setiap variable yang akan digunakan
adminsData = pd.DataFrame()
isLogin = isSuper = False
loginData = pd.DataFrame()


# Memperbarui data admin dari file csv
def renewAdminsData():
    global adminsData

    adminsData = getCsvData(adminsPath)


# Memberikan output data admin
def getAdmins() -> pd.DataFrame:
    return adminsData.copy()


# Memberikan output data login
def getLogin() -> pd.Series | pd.DataFrame:
    return loginData.copy()


# Melakukan login
def doLogin(username: str, password: str,  datas: pd.Series | pd.DataFrame, isSuper: bool = False) -> bool:

    if isSuper:
        result = datas.loc[(datas['username'].apply(str) == username) & (
            datas['password'].apply(str) == password) & (datas['is_super']) & (datas['active'])]
        if result.empty:
            return False
    else:
        result = datas.loc[(datas['username'].apply(str) == username) & (
            datas['password'].apply(str) == password) & (datas['active'])]
        if result.empty:
            return False

    return result


# Tampilan Login
def loginAdmin() -> tuple:
    global loginData, isLogin, isSuper
    while (True):
        printCustom(
            "[1] Login Super Admin\n" +
            "[2] Login Admin\n" +
            "[X] Exit", char="-", isCenter=False)

        choice = input("[?] Masukkan Pilihan: ")

        if choice == '1' or choice == '2':
            username = input("[?] Masukkan Username: ")
            password = input("[?] Masukkan Password: ")
            superChoice = True if choice == '1' else False
        elif choice == 'x':
            exit()
        else:
            clearConsole()
            printCustom(" !Pilihan tidak tersedia! ")
            continue

        loginResult = doLogin(username, password, adminsData, superChoice)
        if isinstance(loginResult, (pd.Series, pd.DataFrame)):
            isLogin = True
            isSuper = superChoice
            loginData = loginResult

            return (isLogin, isSuper, loginData)
        else:
            clearConsole()
            printCustom(" !Gagal Login, Username atau Password Salah! ")
            continue


# Tampilan logout dengan tampilannya
def logoutAdmin() -> None:
    global loginData, isLogin, isSuper

    name = loginData['nama'].values[0]
    isLogin = isSuper = False
    loginData = None
    printCustom(f" !{name} Berhasil Logout! ")
    return (isLogin, isSuper, loginData)


# Modifikasi data admin
def modifyAdmin(mode: str, first: bool = False) -> None:
    global adminsData, isLogin, isSuper, loginData

    def printData(adminId: str, name: str, noHp: str, addr: str, uname: str, passwd: str, super: bool) -> None:
        printCustom(f"[I] ID: {adminId}" +
                    f"\n[N] Nama: {name}" +
                    f"\n[H] NO HP: {'No Data' if noHp == '-' else noHp}" +
                    f"\n[A] Alamat: {'No Data' if addr == '-' else addr}" +
                    f"\n[U] Username: {uname}" +
                    f"\n[P] Password: {'*'*len(passwd)}" +
                    f"\n[S] Super Admin: {super}", char="-", isCenter=False)

    printCustom(f" {mode.title()} Data Admin ")
    if mode == 'edit' or mode == 'tambah':
        if mode == 'edit':
            printTable(adminsData.query('active == True'), [
                       'admin_id', 'username', 'nama', 'no_hp', 'alamat'])
            printCustom('[X] Batal   [NO] Pilih Nomor Admin')

            while True:
                adminIndex = input("[?] Silahkan Pilih Admin: ")
                if adminIndex.isnumeric():
                    adminIndex = int(adminIndex)
                    if adminIndex in adminsData.index:
                        break
                    else:
                        print("[I] Nomor Admin Tidak Ditemukan! ")
                elif adminIndex.casefold() == 'x':
                    return
            adminData = adminsData.loc[[adminIndex]]
        elif not first:
            print('[X] Isi dengan X untuk Membatalkan')

        adminId = adminData['admin_id'].values[0] if mode == 'edit' else generateUniqueId(
            adminsData['admin_id'], prefix="ADM-")

        name = input("[?] Nama: ").title(
        ) or (adminData['nama'].values[0] if mode == 'edit' else "Admin")
        if name.casefold() == 'x' and not first:
            return

        noHp = input("[?] No HP: ") or (
            adminData['no_hp'].values[0] if mode == 'edit' else "-")
        addr = input("[?] Alamat: ") or (
            adminData['alamat'].values[0] if mode == 'edit' else "-")
        while True:
            uname = input("[?] Username: ").casefold(
            ) or (adminData['username'].values[0] if mode == 'edit' else "")
            if uname == "":
                print('[!] Username tidak boleh kosong!')
            elif uname not in adminsData['username'].values or (mode == 'edit' and uname == adminData['username'].values[0]):
                break
            else:
                print(f"[!] Username {uname} Sudah Terdaftar! ")

        while True:
            passwd = input(
                "[?] Password: ") or (adminData['password'].values[0] if mode == 'edit' else "")
            if len(passwd) >= 6:
                break
            else:
                print("[!] Password Minimal 6 Karakter! ")

        if mode == 'edit':
            super = (input("[?] Super Admin? [Y/N]: ").casefold(
            ) or ("y" if adminData['is_super'].values[0] else "n")) == "y"
        else:
            super = True if first else input(
                "[?] Super Admin? [Y/N]: ").casefold() == 'y'

        newAdmin = {
            "admin_id": adminId if mode == 'edit' else [adminId],
            "nama": name if mode == 'edit' else [name],
            "username": uname if mode == 'edit' else [uname],
            "password": passwd if mode == 'edit' else [passwd],
            "is_super": super if mode == 'edit' else [super],
            "no_hp": noHp if mode == 'edit' else [noHp],
            "alamat": addr if mode == 'edit' else [addr],
            "active": True if mode == 'edit' else [True]
        }

        if mode == 'edit':
            adminsData = editData(
                adminsData, adminsData['admin_id'] == adminId, list(newAdmin.keys()), tuple(newAdmin.values()), adminsPath)
        else:
            adminsData = addData(adminsData, newAdmin, adminsPath)

        renewAdminsData()
        clearConsole()

        printCustom(f" Berhasil {mode.title()} Data Admin ")
        printData(adminId, name, noHp, addr, uname, passwd, super)
        if first:
            input("[I] Tekan Enter Untuk Melanjutkan...")
            clearConsole()

    elif mode == 'hapus':
        printTable(adminsData.query('active == True'), [
            'admin_id', 'username', 'nama', 'no_hp', 'alamat'])

        print('[X] Isi Dengan X Untuk Membatalkan')

        while True:
            adminIndex = input("[?] Silahkan Pilih Admin: ")
            if adminIndex.isnumeric():
                adminIndex = int(adminIndex)
                if adminIndex in adminsData.index:
                    break
                else:
                    print("[I] Nomor Admin Tidak Ditemukan! ")
            elif adminIndex.casefold() == 'x':
                return

        adminData = adminsData.loc[[adminIndex]]
        adminId = adminData['admin_id'].values[0]
        clearConsole()
        printData(adminId, adminData['nama'].values[0], adminData['no_hp'].values[0], adminData['alamat'].values[0],
                  adminData['username'].values[0], adminData['password'].values[0], adminData['is_super'].values[0])

        confirm = input(
            f"[?] Apakah Anda Yakin Ingin Menghapus Data Admin diatas [Y/N]? ").casefold() == 'y'
        if confirm:
            adminsData = editData(
                adminsData, adminsData['admin_id'] == adminId, ('active'), (False), adminsPath)
            renewAdminsData()
            clearConsole()
            printCustom(f" !Data Admin dengan ID {adminId} Berhasil Dihapus! ")
            if adminId == loginData['admin_id'].values[0]:
                isLogin = isSuper = False
                loginData = None
                renewAdminsData()
                printCustom(" !Anda Telah Logout, karena Akun telah dihapus! ")
        else:
            clearConsole()
            printCustom(f" !Data Admin dengan ID {adminId} Batal Dihapus! ")
        return (isLogin, isSuper, loginData)
    else:
        print("[I] Mode tidak tersedia! ")
        return (False)


# Tampilan awal ketika belum ada akun Super Admin
def firstStart() -> None:
    global adminsData

    if adminsData.query('is_super == True & active == True').empty:
        printCustom(
            " !Anda Tidak Memiliki Pengguna Super Admin! \n !Silahkan Buat Pengguna Super Admin Terlebih Dahulu! ", char='-')
        modifyAdmin('tambah', True)
