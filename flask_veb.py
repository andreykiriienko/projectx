from flask import Flask, render_template, redirect, request
from user import create_user, get_user_by_id, get_user_by_username, is_token_alive, if_token_is_expire
from misc import check_password

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('links.html')


@app.route('/user/create', methods=['GET', 'POST'])
def creation_user():
    message = 'User created successful'
    if request.method == 'GET':
        return render_template('creation_user.html')
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            create_user(data={'username': username, 'email': email, 'password': password})
            return render_template('creation_user.html', message=message)
        except Exception as e:
            return render_template('creation_user.html', message=e)


@app.route('/user/get/<int:id>', methods=['GET'])
def user_data(id_user):
    if request.method == 'GET':
        result = get_user_by_id(user_id=id_user)
        return result


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'GET':
        return render_template('login_user.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = get_user_by_username(username=username)
        get_username = user['username']
        get_password = user['password']
        hash_pass = check_password(get_password, password)
        if get_username == username and hash_pass == True:
            return render_template('my_acc.html')
    return redirect('/login')


@app.route('/account/<int:id>', methods=['GET'])
def account(id):
    if request.method == 'GET':
        alive = is_token_alive(user_id=id)
        if alive:
            return render_template('my_acc.html')
        else:
            expire = if_token_is_expire(id)
            if expire:
                return render_template('my_acc.html')
    return render_template('login_user.html')


@app.route('/logout')
def delete_user():
    return render_template('delete_user.html')


@app.errorhandler(404)
def page_not_found_404(error):
    return render_template('page404.html'), 404


@app.errorhandler(500)
def page_not_found_500(error):
    return render_template('page500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
