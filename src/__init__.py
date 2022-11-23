__utils__ = ['is_float', 'clear_console', 'edit_data', 'add_data',
             'delete_data', 'generate_unique_id', 'print_custom', 'adminsPath', 'productsPath', 'ordersPath', 'ordersDetailsPath', 'adminsData']
__admin__ = ['doLogin', 'renewAdminsData', 'getAdmins', 'loginAdmin',
             'logoutAdmin', 'modifyAdmin', 'firstStart']
__product__ = ['renewProductsData', 'getProducts', 'modifyProduct']
__transaction__ = ['renewTransactionsData', 'newTransaction', 'updateStock',
                   'inputTransaction', 'myTransactions']

__all__ = __utils__ + __admin__ + __product__ + __transaction__
