from sqlalchemy.orm import sessionmaker
from DAO import User, Auth
from DAO import engine
from misc import hash_password, time

session = sessionmaker(bind=engine)


# ======================================== AUTH =============
def create_auth(user_id):
    sess = session()
    auth = Auth(user_id=user_id)

    sess.add(auth)
    sess.commit()
    sess.close()

    return auth


def get_auth(user_id: int):
    sess = session()
    auth = sess.query(Auth).filter(Auth.user_id == user_id).one()
    sess.close()

    return {'id': auth.id, 'user_id': auth.user_id, 'token': auth.token, 'token_expire_date': auth.token_expire_date}


def delete_auth(user_id: int):
    sess = session()

    auth = sess.query(Auth).filter(Auth.user_id == user_id).one()

    sess.delete(auth)
    sess.commit()
    new_auth = create_auth(user_id=user_id)
    return new_auth


def is_token_alive(user_id: int):
    auth = get_auth(user_id)

    if auth.get('token_expire_date') <= time:
        return False
    else:
        return True


def if_token_is_expire(user_id: int):
    if is_token_alive(user_id):
        pass
    else:
        return delete_auth(user_id)


# ======================================== USER =============
def get_user_by_id(user_id: int):
    sess = session()

    try:
        user = sess.query(User).filter(User.id == user_id).first()
        sess.close()
        return {'id': user.id, 'username': user.username, 'email': user.email, 'password': user.password,
                'role': user.role, 'date_creation': user.date_creation, 'authenticate': user.authenticate}
    except Exception as error:
        sess.close()
        return {'error': error}


def get_user_by_username(username: str):
    sess = session()

    try:
        user = sess.query(User).filter(User.username == username).first()
        sess.close()

        return {'id': user.id, 'username': user.username, 'email': user.email, 'password': user.password,
                'role': user.role, 'date_creation': user.date_creation, 'authenticate': user.authenticate}
    except Exception as error:
        sess.close()
        return {'error': error}


def create_user(data: dict):
    sess = session()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    user = User(username=username, email=email, password=hash_password(password))

    sess.add(user)
    sess.commit()

    get_user = get_user_by_username(username=username)
    create_auth(user_id=get_user.get('id'))

    sess.close()

    return get_user
