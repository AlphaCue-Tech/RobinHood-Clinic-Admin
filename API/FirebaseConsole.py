import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from django.conf import settings
import os
from Utility.Functions import timeConvert, current_milli_time

def initialize_firebase():
    json_file = os.path.join(settings.BASE_DIR, 'API/robinhood-clinic-firebase-adminsdk-mwkvd-cde212e319.json')

    try:
        firebase_admin.get_app()
    except:
        # initializations
        cred = credentials.Certificate(json_file)
        firebase_admin.initialize_app(cred)

    db = firestore.client()

    return db

def test_print():
    db = initialize_firebase()

    emp_ref = db.collection('customers')
    docs = emp_ref.stream()

    for doc in docs:
        print('{} => {} '.format(doc.id, doc.to_dict()))

def find_user(username):
    db = initialize_firebase()
    user_ref = db.collection('users').where('username', '==', username).stream()
    user_list = []
    for user in user_ref:
        data = user.to_dict()
        data['id'] = user.id
        #print('{} ==> {}'.format(user.id, user.to_dict()))
        user_list.append(data)

    if len(user_list)>0:
        return user_list[0]
    else:
        return None

def find_admin_user(username):
    db = initialize_firebase()
    user_ref = db.collection('admin_user').where('username', '==', username).stream()

    for user in user_ref:
        print('{} ==> {}'.format(user.id, user.to_dict()))
        return user.to_dict()

    return None

def get_all_users():
    db = initialize_firebase()
    user_ref = db.collection('users').stream()
    user_list = []

    for user in user_ref:
        print('{} ==> {}'.format(user.id, user.to_dict()))
        d = user.to_dict()
        d['id'] = user.id
        d['lastLogin'] = timeConvert(d['lastLogin'])
        user_list.append(d)

    return user_list

def get_all_users_dict():
    db = initialize_firebase()
    user_ref = db.collection('users').stream()
    user_dict = {}

    for user in user_ref:
        d = user.to_dict()
        d['lastLogin'] = timeConvert(d['lastLogin'])

        user_dict[user.id] = d

    return user_dict

def get_all_admin_users_dict():
    db = initialize_firebase()
    user_ref = db.collection('admin_user').stream()
    admin_user_dict = {}

    for user in user_ref:
        d = user.to_dict()
        admin_user_dict[user.id] = d

    return admin_user_dict

def get_all_invoices():
    db = initialize_firebase()
    invoice_ref = db.collection('invoices').stream()
    invoice_list = []

    for invoice in invoice_ref:
        print('{} ==> {}'.format(invoice.id, invoice.to_dict()))
        d = invoice.to_dict()
        d['id'] = invoice.id
        d['CUSTOMER_NAME'] = d['customerId'].get().to_dict()['name']
        d['CUSTOMER_PHONE'] = d['customerId'].get().to_dict()['phone']
        d['invoiceBy'] = d['invoiceBy'].get().to_dict()['username']

        invoice_list.append(d)

    return invoice_list

def get_all_products():
    db = initialize_firebase()
    pro_ref = db.collection('products').stream()
    pro_list = []

    for pro in pro_ref:
        print('{} ==> {}'.format(pro.id, pro.to_dict()))
        d = pro.to_dict()
        d['id'] = pro.id
        pro_list.append(d)

    return pro_list

def get_all_products_dict():
    db = initialize_firebase()
    pro_ref = db.collection('products').stream()
    pro_dict = {}

    for pro in pro_ref:
        d = pro.to_dict()
        d['id'] = pro.id

        pro_dict[pro.id] = d

    return pro_dict

def create_user(username, password):
    if find_user(username) is None:
        db = initialize_firebase()
        users_ref = db.collection('users').document()
        cur_time = current_milli_time()
        users_ref.set({
            'username':username,
            'password':password,
            'lastLogin':cur_time
        })
        return True
    else:
        return False

def add_item(name, cost):
    db = initialize_firebase()
    pros_ref = db.collection('products').document()

    pros_ref.set({
        'name': name,
        'cost': cost
    })

def get_single_invoice(id):
    db = initialize_firebase()
    invoice_ref = db.collection('invoices').document(id)
    all_pro_dict = get_all_products_dict()
    try:
        invoice = invoice_ref.get()
        invoice_dict = invoice.to_dict()
        invoice_dict['id'] = id
        item_list = []

        for key, value in invoice_dict['items'].items():
            it = {
                'id': key,
                'quantity': value,
                'name': all_pro_dict[key]['name'],
                'cost': all_pro_dict[key]['cost'],
                'total': all_pro_dict[key]['cost']*value
            }
            item_list.append(it)
        invoice_dict['ITEM_LIST'] = item_list

        invoice_dict['CUSTOMER'] = invoice_dict['customerId'].get().to_dict()

        return invoice_dict
    except:
        return None
