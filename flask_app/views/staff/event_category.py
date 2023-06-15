# Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import render_template, flash, request, redirect, session, url_for
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
    categories = read_event_category()
    # render함수로 html가르킴
    return render_template('staff/event_category/list.html', categories=categories)
# html 파일은 로그인이 되었을 때 표시
# render_template는 templates 폴더의 주소를 가준으로 html 파일을 불러옴

################################## add ##############################################################
@app.route('/show_main_category/<string:mode>/input', methods=['GET', 'POST'])
@is_staff_login
def show_input_form(mode):
    formdata = session.get('category_form', None) # session.get () <- 데이터 검색 , 그리고 검색한 데이터를 formdata에 저장 
    event_category_name=''
    event_category_id=''
    if formdata: # is None 
        event_category_id = formdata['event_category_id']
        event_category_name = formdata['event_category_name']
        session.pop('category_form', None)
    
    else:
        if mode=='create':
            event_category_id=''
            event_category_name=''
            print("hello") # デバック処理通ってます。
            return render_template('staff/event_category/input.html', mode=mode, tage)
        
        if mode=='update':
            event_category_id=request.form.get('event_category_id')
            target_event_category = read_event_category_one(event_category_id)
            
            return render_template('staff/event_category/input.html', mode=mode, target_event_category=target_event_category)
        
        if mode=='delete':
            print("hehe")
            delete_ev_category_name = request.form.get('event_category_id')
            dt = db.session.query(Mst_event_category).filter_by(event_category_name=delete_ev_category_name).first()
            if dt is None:  # 없다면 , 신규 등록
                flash("データがありません。")
                message = None
                return render_template('staff/event_category/list.html', message=message)
            else:
                message = request.form['event_category_name']+"が削除されました。"
                db.session.commit()
                return render_template('staff/event_category/list.html', message=message)
            

    return render_template('staff/event_category/confirm.html', message=message)
            
            


@app.route('/show_main_category/add', methods=['POST'])
@is_staff_login
def add_event_category(event_category_id=-1):
    mode = request.form.get("button")
    if mode=='create':
        
        create_event_category(request)
        
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





