# Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import render_template, flash, request, redirect, session, url_for, Markup
from flask_app.__init__ import app
from flask_app.messages import ErrorMessages, InfoMessages
from flask_app.models.functions.event_category import read_event_category_category_name, create_event_category, update_event_category, delete_event_category, read_event_category, read_event_category_one
from flask_app.models.functions.reservations import read_reservation
from flask_app.views.staff.common.staff_common import is_staff_login
import re
from flask_app import db
from flask_app.models.mst_event_category import Mst_event_category

# エラーメッセージクラスのインスタンス作成
errorMessages = ErrorMessages()
# インフォメーションメッセージクラスのインスタンス作成
infoMessages = InfoMessages()


@app.route('/show_main_category', methods=["GET", "POST"])  # 첫 화면 페이지
@is_staff_login
def show_main_category():
    categories = read_event_category() # 데이터 베이스의 내용 전체를 불러옴. ( id순으로 정렬된 데이터 베이스의 내용 )
    # render함수로 html가르킴
    return render_template('staff/event_category/list.html', categories=categories) # 리스트.HTML은 메인 화면으로 데이터 베이스의 내용을 모두 전달 
# html 파일은 로그인이 되었을 때 표시
# render_template는 templates 폴더의 주소를 가준으로 html 파일을 불러옴

################################## 입력 폼 ##############################################################
@app.route('/show_main_category/<string:mode>/input', methods=['GET', 'POST']) ########################### 
# '/show_main_category/<string:mode>/input'는 list.html로 간다. show_main_category함수의 렌더 템플릿이 list.html이기 때문 
# <string:mode>는 url에서 얻은 정보를 문자열로 mode라는 변수에 저장한다. 즉, create, delete 등이  mode에 저장됨 
# mode는 url의 주소인 list.html로 들어가서, 버튼이 눌린 것에 따른 mode 값을 받아옴. 
# list.html 의 <a href="{{ url_for('show_input_form', mode='create') }}" class="btn btn-primary">イベントカテゴリ名新規登録</a> 
# 코드에서 신규 등록을 누르면, mode가 create가 설정된다. 
@is_staff_login ## <string:mode>은 사용자가 url을 통해, 입력한 값을 문자열 형태로 받아와서 mode라는 변수에 저장하는 것을 의미. 
def show_input_form(mode): # mode에 따른 입력폼 출력하는 함수 ##### 
    formdata = session.get('category_form', None) # session.get () <- 데이터 검색 , 그리고 검색한 데이터를 formdata에 저장 
    ## 즉 , category_form의 입력폼에서 작성된 데이터를 얻는다. 
    ## 만약, create 버튼을 누른다면, formdata = session.get('category_form', None) 에는 
    ## 데이터가 None으로 저장된다. 이유로는, list.html의 <a href="{{ url_for('show_input_form', mode='create') }}" class="btn btn-primary">イベントカテゴリ名新規登録</a>
    # 코드에서 name의 값에 저장된 값이 없기 때문에, get의 입장에서는 입력 받은 값이 없으면 ,None으로 저장한다. 

    
   
    event_category_name='' ## 이벤트 카테고리의 이름은 먼저 공백으로 정의 
    event_category_id=''  ##  ############################################################## 
    if formdata: # 입력폼에 데이터가 있다면, 즉, update , delete 일때 
        event_category_id = formdata['event_category_id'] ### 입력칸에서 입력된 id의 값을 읽는다. id는 숨겨진 값 
        event_category_name = formdata['event_category_name'] ## 입력칸에서 입력ㄷ된 이름을 읽는다. 
        session.pop('category_form', None) ### 입력폼의 세션을 닫는다. 
    
    else: # create일 때 즉, 'event_category_id'의 값이 없을 때 
        if mode=='create':
            event_category_id=''
            event_category_name=''
           # デバック処理通ってます。
            return render_template('staff/event_category/input.html', mode=mode, target_event_category=None)
        
        if mode=='update':
            # event_category_id=request.form.get('event_category_id') #id를 들고옴 . 키가 없을 수 도 있다. 
            vent_category_id=request.form['event_category_id'] # 위의 코드를 이렇게 바꾸어도 문제가 없다. 
            ## html의 입력폼에서 값을 받아온다. 
            target_event_category = read_event_category_one(event_category_id) # 입력된 값을 데이터 베이스에서 검색한다. 
            
            return render_template('staff/event_category/input.html', mode=mode, target_event_category=target_event_category)
        
        if mode=='delete':
            target_category_id=request.form.get('event_category_id')
            target_event_category = read_event_category_one(target_category_id)

            delete_event_category(target_event_category.event_category_id)

            flash('削除しました')
            return redirect(url_for('show_main_category'))
            

    return render_template('staff/event_category/confirm.html')
            
            


@app.route('/show_main_category/add', methods=['POST'])
@is_staff_login
def add_event_category(event_category_id=-1):
    mode = request.form.get("button") # name = " button"이 되어있는 버튼이 눌러졌을 때 작동 
    if mode=='create': # input.html에서 입력 폼에 name을 입력한 후에 처리 
        # html에서 데이터를 전송할 때, 각 입력 필드의 'name'속성 값은 키로, 
        # 사용자가 해당 필드에 입력하는 값은 키- 값 쌍으로 만들어짐. 
        # 이러한 값은 request.form에 딕셔너리로써 저장된다. 
        # 때문에, 만약 event_category_name 의 값을 가져오고 싶으면, 
        # request.form['event_category_name']으로 들고오면 된다. 
        create_event_category(request) 
        # 데이터 베이스에 데이터를 추가하는 함수로 이동 


        
        flash('新規イベントカテゴリ{}を追加しました'.format(request.form["event_category_name"]))
        return redirect(url_for('show_main_category'))
    elif mode=='update':
        event_category_id= request.form.get("event_category_id")
        update_event_category(event_category_id, request)
        flash('更新しました。')
        print("update_progress")
        return redirect(url_for('show_main_category'))
    elif mode=='delete':
        event_category_id= request.form.get("event_category_id")
        
        delete_event_category(event_category_id)
        flash('削除しました')
        print("delete_progress")
        return redirect(url_for('show_main_category'))
    else:
        print("why!")    
        

##################################### update ###################################

@app.route('/show_main_category/update/<int:event_category_id>', methods=['POST'])
@is_staff_login
def overwrite_event_category(event_category_id):
    old_event_category = read_event_category(event_category_id)
    update_event_category(event_category_id, request)
    flash('イベントカテゴリ{}を{}に更新しました'.format(old_event_category.event_category_name, request.form["event_category_name"]))
    return render_template(url_for('show_main_category'))





