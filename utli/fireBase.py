import os
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
from firebase_admin import firestore
from utli.User import User, states
class dataBase():
    def __init__(self):
        # 引用私密金鑰
        # path/to/serviceAccount.json 請用自己存放的路徑
        cred = firebase_admin.credentials.Certificate('src/holoshop-b66bf-firebase-adminsdk-qoedz-8dfec4ed89.json')
        # 初始化firebase，注意不能重複初始化
        firebase_admin.initialize_app(cred)
        self.db = firebase_admin.firestore.client()

    def getUserData(self,id):
        path = "user/" + id
        collection_ref = self.db.document(path)
        doc = collection_ref.get()
        
        return doc.to_dict()
        
    def newUserData(self,id, profile):
        doc = { 
                'user_id' : id,
                'state' : 0,
                'group' : 0
            }
        self.db.collection("user").document(id).set(doc)

    def updateUserData(self,user):
        doc = self.user2Doc(user)
        self.db.collection("user").document(user.user_id).update(doc)

    def doc2User(self,doc):
        user = User(doc['user_id'])
        user.state = doc['state']
        user.group = doc['group']
        return user
    
    def user2Doc(self,user):
        doc = { 
                'user_id' : user.user_id,
                'state' : user.state,
                'group' : user.group
            }
        return doc
        
    def getProductData(self):
        path = "product"
        
        collection_ref = self.db.collection(path)
        doc = collection_ref.get()
        case = { el.id: el.to_dict() for el in doc }
        return case

    def deleteDB(self, path, id):

        self.db.collection(path).document(id).delete()
