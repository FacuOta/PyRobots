from fastapi import HTTPException
from http import HTTPStatus
from passlib.context import CryptContext
import jwt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_SECRET = 'TWtIfiNR1jvIJ1vc'

def check_password_rules(password: str):
    if (any(x.isupper() for x in password) 
    and any(x.islower() for x in password) 
    and any(x.isdigit() for x in password)
    and len(password) <=16
    and len(password) >=8):
        return True


def check_valid_imagetype(mime: str):
   return ("image" in mime)

def check_valid_username(username: str):
    return (len(username) <=16)

def are_valid_credentials(username : str, password : str):
    return check_valid_username(username) and check_password_rules(password)

def hash_password(password : str):
    return pwd_context.hash(password)

def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET)
    return encoded_jwt

def decode_token(token):
    credentials_exception = HTTPException(
        status_code= HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        username = payload.get("username")
        if username is None:
            raise credentials_exception
    except:
        raise credentials_exception
    
    return username

def incorrect_username_password():
    raise HTTPException(status_code = HTTPStatus.UNAUTHORIZED, detail = "Incorrect Username or Password")

def no_user(username):
    raise HTTPException(status_code = HTTPStatus.NOT_FOUND, detail = f"No username by {username}")

def user_not_verified():
    raise HTTPException(status_code = HTTPStatus.UNAUTHORIZED, detail = "User has not verified its email adress")

def send_email(mail_usuario, codigo_verificacion):
    cuerpo = '''Gracias por registrarte en PyRobots!'''
    html = ' <p> <b> Su numero de verificacion es: </b>'  + str(codigo_verificacion) + '</p>'

    correo_organizacion = 'transformers.pyrobots@gmail.com'
    contra_organizacion = 'sdolbmmlzukxwnwo'


    message = MIMEMultipart()
    message['From'] = correo_organizacion
    message['To'] = mail_usuario
    message['Subject'] = 'Correo de verificacion'

    message.attach(MIMEText(cuerpo, 'plain'))
    message.attach(MIMEText(html, 'html'))

    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(correo_organizacion, contra_organizacion)
    text = message.as_string()
    session.sendmail(correo_organizacion, mail_usuario, text)
    session.quit()

def get_websocket_address(partida_id):
    return "ws://localhost:8000/lobbys/" + str(partida_id)