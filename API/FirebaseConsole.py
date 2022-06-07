import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from django.conf import settings
import os


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

    for user in user_ref:
        print('{} ==> {}'.format(user.id, user.to_dict()))

def find_admin_user(username):
    db = initialize_firebase()
    user_ref = db.collection('admin_user').where('username', '==', username).stream()

    for user in user_ref:
        print('{} ==> {}'.format(user.id, user.to_dict()))
        return user.to_dict()

    return None

