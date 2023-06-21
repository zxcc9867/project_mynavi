from flask import render_template, flash, request, redirect, session, url_for, Markup
from flask_app.__init__ import app
from flask_app.models.mst_customer import Mst_customer
from flask_app.models.functions.customer import read_customer_customer_account
from flask_app.__init__ import db
import hashlib  # この行を追加
from flask_app.views.customer.common.customer_common import is_customer_login


@app.route('/show_login', methods=['GET'])
def show_login():
    return render_template('/customer/customer_login/customer_login.html')

@app.route('/show_login/customer_login', methods=['GET','POST'])
def customer_login():
    customer_account = request.form.get('customer_account')
    customer_account_search = Mst_customer.query.with_entities(Mst_customer.customer_account).filter_by(customer_account=customer_account).all()  # 入力されたアカウント名とデータべースのアカウント名が一致するアカウント名を抽出
    # customer_password = request.form.get('customer_password')  # この行を削除
    customer_password = hashlib.sha256(request.form.get('customer_password').encode()).hexdigest()  # この行を追加
    customer_password_tuple = Mst_customer.query.with_entities(Mst_customer.customer_password).filter_by(customer_account=customer_account).all()
    if not customer_password_tuple:
        flash('アカウント名が違います')
        return render_template('/customer/customer_login/customer_login.html')
    else:
        print(customer_password_tuple[0])
        customer_password_database = ''.join(customer_password_tuple[0])
        print(customer_password_database)
        if customer_account_search:
            if customer_password_database == customer_password:
                customer_array = read_customer_customer_account(request.form.get('customer_account'))
                customer = customer_array[0]
                session['logged_in_customer'] = True
                session['logged_in_customer_account'] = customer.customer_account
                session['logged_in_customer_id'] = customer.customer_id
                session['logged_in_customer_name'] = customer.customer_name
                flash('ログインしました')
                return redirect(url_for('show_customer_event_list'))
            else:
                flash('パスワードが違います')
                return render_template('/customer/customer_login/customer_login.html')
        else:
            flash('アカウント名が違います')
            return render_template('/customer/customer_login/customer_login.html')
    
@app.route('/customer_logout')
@is_customer_login
def customer_logout():
    session.pop('logged_in_customer', None)
    flash('ログアウトしました')
    return redirect(url_for('show_customer_event_list'))

@app.route('/show_sighup', methods=['GET'])
def show_signup():
    return render_template('/customer/customer_signup/input.html')

@app.route('/show_signup/confirm', methods=['POST'])
def show_signup_confirm():
    customer_account = request.form.get('customer_account')
    customer_password = request.form.get('customer_password')
    customer_name = request.form.get('customer_name')
    customer_zipcode = request.form.get('customer_zipcode')
    customer_address = request.form.get('customer_address')
    customer_phone = request.form.get('customer_phone')
    # customer_payment = request.form.get('customer_payment')

    return render_template('/customer/customer_signup/confirm.html', customer_account=customer_account, customer_password=customer_password, customer_name=customer_name, customer_zipcode=customer_zipcode, customer_address=customer_address, customer_phone=customer_phone)




@app.route('/show_signup/signup', methods=['POST'])
def signup():
    customer_password_hash = hashlib.sha256(request.form.get('customer_password').encode()).hexdigest()
    mst_customer = Mst_customer(
        customer_account = request.form.get('customer_account'),
        # customer_password = request.form.get('customer_password'), # この行を削除
        customer_password = customer_password_hash,  #この行を追加
        customer_name = request.form.get('customer_name'),
        customer_zipcode = request.form.get('customer_zipcode'),
        customer_address = request.form.get('customer_address'),
        customer_phone = request.form.get('customer_phone'),
        # customer_payment = request.form.get('customer_payment')
    )
    db.session.add(mst_customer)
    db.session.commit()
    flash('新規登録に成功しました')
    return redirect(url_for('show_login'))

# @app.route('/show_customer_edit', methods=['GET'])
# def show_customer_edit():