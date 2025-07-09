import bcrypt

# Contraseña a hashear
password = "123456789".encode('utf-8')

# Generar un salt
salt = bcrypt.gensalt()

# Hashear la contraseña
hashed_password = bcrypt.hashpw(password, salt)

print(f"Password original: {password.decode()}")
print(f"Password hasheado: {hashed_password}")

# Verificar la contraseña
password_ingresada = "123456789".encode('utf-8')
if bcrypt.checkpw(password_ingresada, hashed_password):
    print("La contraseña es correcta.")
else:
    print("La contraseña es incorrecta.")