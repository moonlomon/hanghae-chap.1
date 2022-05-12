# W1_mountain_review

## 항해99 첫 미니프로젝트 (참가자 : 김하연, 문성준, 유승연, 최병민)


## 프로젝트 정보

 - 혼자 등산을 하면서 나를 기분좋게 해주었던 산의 사진과 좋았던 코스를 소개하며 혼산러들의 정보를 공유하는 웹페이지입니다.

 - 개발기간 : 22.5.9-5.12
---
## Stack

 - frontend : HTML, CSS,

 - backend : python ,Flask

 - db : mongoDb

 - jQuery, jinja2, javascript
---
## 상세기능
### 메인페이지
1. 메인
 - 사진 및 리뷰등록
 - modal 기능 
 - 사진 클릭 시 상세페이지
 - 검색기능 가능
 - [전체목록 보기] button click 시 이벤트 발생 
2. modal 
 - 등록하기 button click시 이벤트 발생
 - 사진 클릭 시 상세페이지에 작성했던 정보 모달로 call

### 로그인,회원가입

 - 메인 페이지에서 로그인 페이지로 rendering 
 - JWT Token 이용 
 - 회원가입 button 클릭 시 회원가입 button으로 toggle 
 - Bulma 사용

### 등록페이지
1. 등록 종류
 - 사진등록, 산이름, 등산한 코스 이름, 지역명, 편의시설, 소감 및 기타정보
 - 사진 업로드 시 파일명 명시
 - 개선점 : 어떤 사진을 올렸는지 확인하기 위해 파일명을 명시하였지만 사진파일을 미리보기를 추가하여 사용자의 실수를 줄일 수 있을거 같다.
2. 예외처리
 - 사진 또는 산이름을 미작성시 경고알람
 - 개선점 : 산이름, 코스 이름, 지역명, 소감을 작성시 욕설 또는 은어가 들어가는 경우를 예외처리 (자연어처리기능) 

### 게시물

 - 등록페이지로부터 받은 데이터를 메인페이지에 게시물로 나타냄
 - 게시물의 경우 사진만 보여지며 마우스가 사진으로 이동시 이벤트가 발생하여 산이름, 작성자, 편의시설이 보여짐
 - 사진 클릭시 사진, 산이름, 위치, 편의시설, 소감의 데이터가 모두 보여짐 (modal 기능 구현)
---
 
## API 구성

### 웹페이지의 메인페이지

*> - 메인페이지인 idex.html 파일과 등록된 게시글의 정보를 mongoDB에서 가저와 rendering 해준다.*

```python
@app.route('/')
def home():
    return render_template('index.html', msg=msg) 
```   

*> - 로그인 후 보여지는 페이지로 로그인한 상태와 안한 상태를 구분, DB에 저장되어있는 등록페이지의 DB, 검색기능을 사용했을 때 검색어와 상태를 rendering 해준다.*

```python
@app.route('/login/home')
def home_():
    if status is not None:
        return render_template('index.html', posts=posts, status=status, keyword=keyword, user_id=user_id)
    else:
        return render_template('index.html', posts=posts, status='no', keyword='', user_id=user_id)
```


### 로그인 페이지

*> 로그인페이지 rendering*

```python
@app.route('/login')
def home_login():
    return render_template('register.html', msg=msg)
```

*> 로그인페이지 로그인 쿠키가 만료/ 존재하지 않을때 처리*

```python
@app.route('/login/login')
def login():
    
    return render_template('register.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
```

*> 로그인시 pw를 해쉬함수를 사용하여 DB에 저장*

```python
@app.route('/sign_in', methods=['POST'])
def sign_in():
    
         return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})
```

*> 회원가입시 ID pw 확인*

```python
@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    
    return jsonify({'result': 'success'})
```

*> 회원가입시 ID 중복확인*

```python
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    # 아이디 중복확인
    
    return jsonify({'result': 'success', 'exists': exists})
```

*> 회원가입시 ID 중복확인*

```python
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    # 아이디 중복확인
    
    return jsonify({'result': 'success', 'exists': exists})
```


### 등록 페이지

*> 등록페이지 rendering*

```python
@app.route('/register')
def register_page():
    return render_template("write.html")
```

*> 등록페이지에 들어오는 상세데이터 DB에 저장*

```python
@app.route('/register/save', methods=['POST'])
def register():
    
        return jsonify({"result": "success", 'msg': '포스팅 성공'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("/"))
```