from werkzeug.security import generate_password_hash, check_password_hash




hash = generate_password_hash('12345')

print(hash)

check = check_password_hash(hash, '12345')

print(check)