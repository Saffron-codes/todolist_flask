from models import *
import jwt
import bcrypt
class AuthHelper:
    def hello():
        print('Hello')
    def signup(self,name:str,email:str,password:str)->str:
        # hasedPassword = bcrypt.kdf(password=password.encode(),salt=b'hello',desired_key_bytes=32,rounds=100)
        salt = bcrypt.gensalt(rounds=16)
        hasedPassword = bcrypt.hashpw(password.encode(),salt)
        # print(hasedPassword)
        user = User(name=name,email=email,password=hasedPassword)
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        print("******************",user.id)
        payload = {
            'id':user.id,
            'name':user.name,
            'email':user.email,
            'password':hasedPassword.decode("utf-8")
        }
        secrect_key = '123ef'
        token = jwt.encode(payload=payload,key=secrect_key)
        return token
    def login(self,email:str,password:str)->str:
        user:User = User.query.filter_by(email=email).first()
        print(user.password)
        if(user):
            if bcrypt.checkpw(password.encode(),user.password):
                print("match")
                payload = {
                    'id':user.id,
                    'name':user.name,
                    'email':user.email,
                    'password':user.password.decode("utf-8")
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
        for s in t:
            print(s.content)
        return t
    