from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import certifi
ca = certifi.where()



app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/img"
basedir = os.path.abspath(os.path.dirname(__file__))

#mongoDB
##각자 DB 사용
client = MongoClient('mongodb+srv://test:sparta@cluster0.zosuv.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

SECRET_KEY = 'SPARTA'


@app.route('/')
def home():
    msg = request.args.get("msg")
    # posts = list(db.mountain_info.find({}, {'_id': False}))
    return render_template('index.html', msg=msg) #posts=posts)


@app.route('/login/home')
def home_():
    msg = request.args.get("msg")
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_id = payload["id"]
    posts = list(db.mountain_info.find({}, {'_id': False}))
    status = request.args.get("searched")
    keyword = request.args.get("keyword")

    if status is not None:
        return render_template('index.html', posts=posts, status=status, keyword=keyword, user_id=user_id)
    else:
        return render_template('index.html', posts=posts, status='no', keyword='', user_id=user_id)


@app.route('/login')
def home_login():
    msg = request.args.get("msg")
    return render_template('register.html', msg=msg)


@app.route('/login/login')
def login():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # user_info = db.users.find_one({"username": payload["id"]})
        return render_template('register.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


# @app.route('/login')
# def home_login():
#     msg = request.args.get("msg")
#     token_receive = request.cookies.get('mytoken')
#     print(payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256']))
#     try:
#         # user_info = db.users.find_one({"username": payload["id"]})
#         return render_template('register.html', msg=msg)
#     except jwt.ExpiredSignatureError:
#         return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
#     except jwt.exceptions.DecodeError:
#         return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.mountain_users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    #회원가입조건
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,                               # 아이디
        "password": password_hash,                                  # 비밀번호
        "profile_name": username_receive                       # 프로필 이름 기본값은 아이디

    }
    db.mountain_users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    # 아이디 중복확인
    username_receive = request.form['username_give']
    exists = bool(db.mountain_users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})

  
@app.route('/register')
def register_page():
    return render_template("write.html")


@app.route('/register/save', methods=['POST'])
def register():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_id = payload['id']
        print(user_id)
        mountain_receive = request.form["mountain_give"]
        route_receive = request.form["route_give"]
        location_receive = request.form["location_give"]
        facilities_receive = request.form["facilities_give"]
        facilities_receive = [int(val) for val in facilities_receive.split(',')]
        # 편의시설 css class 명#
        # 화장실 badge-primary
        # 대피소 badge-secondary
        # 대중교통 badge-success
        # 주차장 badge-danger
        # 하산 후 먹거리 badge-warning
        facilities = [
            [{"비교적 깨끗한 화장실": facilities_receive[0]}, "badge-primary"],
            [{"대피소": facilities_receive[1]}, "badge-secondary"],
            [{"이용 가능한 대중교통": facilities_receive[2]}, "badge-success"],
            [{"넓은 주차장": facilities_receive[3]}, "badge-danger"],
            [{"하산 후 먹거리": facilities_receive[4]}, "badge-warning"]
        ]
        description_receive = request.form["description_give"]

        doc = {
                "userID": user_id,
                "mountain": mountain_receive,
                "route": route_receive,
                "location": location_receive,
                "fa": facilities,
                "desc": description_receive
        }
        if 'file_give' in request.files:
            file = request.files["file_give"]
            filename = secure_filename(file.filename).split('.')[0]
            # print(filename)
            extension = secure_filename(file.filename).split('.')[-1]
            today = datetime.now()
            my_time = today.strftime('%Y%m%d%H%M%s')
            file_name = f'{filename}-{my_time}.{extension}'
            file_path = f"./static/img{file_name}.{extension}"
            file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], file_name))
            doc["pic"] = file_name
        else:
            doc["pic"] = ""

        db.mountain_info.insert_one(doc)
        # print(doc)
        return jsonify({"result": "success", 'msg': '포스팅 성공'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("/"))


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)