# Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import render_template, flash, request, redirect, session, url_for
from flask_app.__init__ import app
from flask_app.messages import ErrorMessages, InfoMessages
from flask_app.models.functions.event_category import read_event_category_category_name, create_event_category,update_event_category,delete_event_category,read_event_category
from flask_app.models.functions.reservations import read_reservation
from flask_app.views.staff.common.staff_common import is_staff_login
import re
from flask_app import db
from flask_app.models.mst_event_category import Mst_event_category 

# エラーメッセージクラスのインスタンス作成
errorMessages = ErrorMessages()
# インフォメーションメッセージクラスのインスタンス作成
infoMessages = InfoMessages()


@app.route('/staff_event_category',methods=["GET"]) # 첫 화면 페이지 
@is_staff_login
def staff_event_category():
    
    return render_template('staff/event_category/list.html',) #render함수로 html가르킴
# html 파일은 로그인이 되었을 때 표시 
# render_template는 templates 폴더의 주소를 가준으로 html 파일을 불러옴 
 
@app.route('/create', methods=['GET','POST'])
def create():

    create_ev_category_name = request.form['event_category_name']
    create_ev_category_id = request.form['event_category_id']
    dt = db.session.query(Mst_event_category).filter_by(event_category_id=create_ev_category_id).first()

     # 없다면 , 신규 등록 
    if dt is True:
            flash("既にイベントが登録されています。")
            # return redirect(url_for('/staff/event_category/list.html'))
    else : 
        
        dt = Mst_event_category(
                    event_category_name=create_ev_category_name, 
                    event_category_id = create_ev_category_id
        )           
    db.session.merge(dt)
    db.session.commit()
    message = request.form['ev_category_name']+"が登録されました。"
    return render_template('staff/event_category/confirm.html',message=message)
    
    
##################################### update ###################################
@app.route('/update', methods=['GET','POST'])
def update():
    update_ev_category_name = request.form['event_category_name']
    update_ev_category_id = request.form['event_category_id']
    dt = db.session.query(Mst_event_category).filter_by(event_category_name=update_ev_category_name).first()
    if dt is None: # 없다면 , 신규 등록 
        
        dt.event_category_name=update_ev_category_name 
        
       
    else: 
        flash("登録されていないイベントです。")
        # return redirect(url_for('/staff/event_category/list.html'))
    dt = Mst_event_category(
                    event_category_name=dt.event_category_name, 
                    event_category_id = dt.event_category_id
        )   
    db.session.merge(dt)
    db.session.commit() 
    message = request.form['event_category_name']+"が更新されました。"
    return render_template('staff/event_category/confirm.html',message=message)
    

##################################delete 삭제 ################################################################

@app.route('/delete',methods=['GET','POST'])
def delete():
    delete_ev_category_name = request.form['event_category_name']
    delete_ev_category_id = request.form['event_category_id']
    dt = db.session.query(Mst_event_category).filter_by(event_category_name=delete_ev_category_name).first()
    db.session.commit()
    if dt is None: # 없다면 , 신규 등록 
        flash("データがありません。")
        # redirect(url_for('/staff/event_category/list.html'))
        # redirect는 새로운 페이지로 이동하라는 지시만 내림 
        # render template는 주어진 데이터와 템플릿을 사용하여, 
        # 페이지의 내용을 생성 
        # 그래서 리다이렉트를 사용하여, 정의된 함수로 이동한다. 
       
    else: 
        dt = db.session.query(Mst_event_category).filter_by(event_category_name=delete_ev_category_name).delete()
        message = request.form['event_category_name']+"が削除されました。"
        return render_template('staff/event_category/confirm.html',message=message)

@app.route('/result',methods=['GET','POST'])

def result():
    # result_db = db.session.query(Holiday).order_by(Holiday.holi_date.desc()).all()
    
    result_db = db.session.query(Mst_event_category).order_by(Mst_event_category.event_category_name.desc()).all()
    return render_template('staff/event_category/confirm.html',message=result_db) # 데이터 베이스의 결과를 모두 전송 

# イベントカテゴリ管理　list
@app.route("/staff_event_category", methods=["GET", "POST"])
@is_staff_login
def staff_manage_category():
    mst_category = read_event_category()

    if not mst_category:
        flash(errorMessages.w01('イベントカテゴリ情報'))

    # mst_customerに直接値を追加できないので、新しい配列を作る
    # mst_category_dict = []
    # for category in mst_category:
    #     param = {'isDeletable': True,
    #              'category_id': category.category_id,
    #              'category_name': category.category_name,
    #              }

    return render_template("staff/event_category/list.html", mst_category=mst_category)

