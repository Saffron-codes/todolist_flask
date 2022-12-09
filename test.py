import bcrypt

# print(b'12'.decode())

salt = bcrypt.gensalt(rounds=12)
encodedPass = "hello123".encode()
hasedPassword = bcrypt.hashpw(encodedPass,salt)
print(hasedPassword)


if bcrypt.checkpw(encodedPass,hashed_password=hasedPassword):
    print("Password matched")
else:
    print("Not a match")
