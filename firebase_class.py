import firebase_admin
from firebase_admin import db

# connect to the database
cred_obj = firebase_admin.credentials.Certificate(r'C:\Users\mamriot\Desktop\school\computer science\python\final_project\final-project.json')
default_app = firebase_admin.initialize_app(cred_obj, {'databaseURL': "https://final-project-38405-default-rtdb.europe-west1.firebasedatabase.app"})

class Firebase:
    def __init__(self, ref):
        self.ref = db.reference(ref)

# get the root ref
# ref = db.reference("/")

    def get_child_ref(self, child):
        ref_child = self.ref.child(child)
        return ref_child

    def get_data(self, value):
        all_data = self.ref.get()
        return all_data.get(value)

    def update_value(self, value, new_data):
        self.ref.update({value: new_data})

    def get_childs_lst(self):
        valueAtRef = self.ref.get(False, True)
        return [*valueAtRef]





