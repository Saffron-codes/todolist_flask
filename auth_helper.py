from models import *
import jwt
import bcrypt
class AuthHelper:
    def hello():
        print('Hello')
    def signup(self,name:str,email:str,password:str)->str:
        user:User = User.query.filter_by(email=email).first()
        if(user == None):
            salt = bcrypt.gensalt(rounds=12)
            hasedPassword = bcrypt.hashpw(password.encode(),salt)
            print(hasedPassword.decode())
            user = User(name=name,email=email,password=hasedPassword.decode())
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)
            # print("******************",user.id)
            payload = {
                'id':user.id,
                'name':user.name,
                'email':user.email,
                'password':hasedPassword.decode("utf-8")
            }
            secrect_key = '123ef'
            token = jwt.encode(payload=payload,key=secrect_key)
            return token
        else:
            return 'error'
    def login(self,email:str,password:str)->str:
        user:User = User.query.filter_by(email=email).first()
        encoded_password = password.encode()
        hashed_password = str(user.password).encode()
        # print(str(user.password).encode())
        # print(password.encode())
        if(user):
            if bcrypt.checkpw(password=encoded_password,hashed_password=hashed_password):
                print("match")
                payload = {
                    'id':user.id,
                    'name':user.name,
                    'email':user.email,
                    'password':str(user.password)
                }
                secrect_key = '123ef'
                token = jwt.encode(payload=payload,key=secrect_key)
                return token
            else:
                print("does not match")
                return "error"
        else:
            return "error"
    def decodeJwt(self,token:str):
        return jwt.decode(token,key='123ef',algorithms='HS256')
    def getAllTodos(self,userId:int):
        t = Todo.query.filter_by(user_id=userId).order_by(Todo.createdAt.desc())
        # for s in t:
        #     print(s.content)
        return t
    