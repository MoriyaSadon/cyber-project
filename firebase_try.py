import firebase_admin
from firebase_admin import db
from firebase_class import Firebase


# users = Firebase("Users")
#
# print(users.get_childs_lst())
#
# print(users.get_data("moriya"))
#
# moriya_ref = users.get_child_ref("moriya")
# moriya = Firebase("Users/moriya")
# moriya.update_value("name", "moriya")
#
# print(moriya.get_data("password"))
#
# print(users.ref.get())
#
# word = "fuck"
# censored = Firebase("Censored")
# user = Firebase(f"Censored/{word}")
# user.update_value("on", "yes")
#
# message = "hi how are you"
# lst = censored.get_childs_lst()
# for word in lst:
#     if word in message.lower():
#         print("yes")
#
#
# word1 = Firebase(f"Censored/{word}")
# word1.update_value("on", "yes")

from hashlib import sha256

username = sha256("shira".encode()).hexdigest()
password = sha256("9876".encode()).hexdigest()

user = Firebase(f"Users/{username}")
user.update_value("name", username)
user.update_value("password", password)













# # connect to the database
# cred_obj = firebase_admin.credentials.Certificate(r'C:\Users\mamriot\Desktop\school\computer science\python\final_project\final-project.json')
# default_app = firebase_admin.initialize_app(cred_obj, {'databaseURL': "https://final-project-38405-default-rtdb.europe-west1.firebasedatabase.app"})
#
# # get the root ref
# ref = db.reference("/")
#
# # ref.set({"Users": {"username": "moriya", "password": "1234"}})
#
# # make a child and add username and password
# ref_users = ref.child("Users")
# # ref_users.update({"name": "moriya"})
# # ref_users.update({"password": "1234"})
# # ref_users.update({"name": "shira"})
#
# # get password for ex
# # data = ref_users.get()
# # print(data.get("password"))
#
# moriya_ref = ref_users.child("moriya")
# moriya_ref.update({"name": "moriya"})
# moriya_ref.update({"password": "5678"})
#
# shira_ref = ref_users.child("shira")
# shira_ref.update({"name": "shira"})
# shira_ref.update({"password": "987"})
#
# # get the name of the child
#
# # get all childs names
# valueAtRef = ref.get(False, True)
# print([*valueAtRef])
# # db.reference("/name").set("moriya")





