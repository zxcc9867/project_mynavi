import re
from flask import render_template, flash, request, redirect, session, url_for, Markup
from flask_app.__init__ import app
from flask_app.__init__ import db
from flask_app.messages import ErrorMessages, InfoMessages
from flask_app.models.functions.customer import delete_customer, read_customer, read_customer_one, update_customer, read_customer_customer_account
from flask_app.models.functions.event_category import create_event_category, read_event_category, read_event_category_one, read_event_category_category_name
from flask_app.models.functions.event import create_event, read_event, read_event_one, read_event_event_category, update_event, delete_event, read_event_with_date
from flask_app.models.functions.reservations import read_reservation_customer_id
from flask_app.models.functions.ticket import read_ticket_one
from flask_app.views.staff.common.staff_common import is_staff_login
from flask_app.views.customer.common.customer_common import is_customer_login
from flask_app.messages import ErrorMessages, InfoMessages
from hashlib import sha256


@app.route("/mypage", methods=['GET','POST'])
@is_customer_login
def show_mypage():
    current_customer_id = session['logged_in_customer_id']
    """
    session 상에 로그인되어 있는 고객 아이디를 읽어 온다. 
    """
    current_customer = read_customer_one(current_customer_id)
    """
    현재 로그인 된 고객의 정보를 커스터머 테이블에서 들고온다. 
    mst_customer의 형식 
    어카운트 명, 패스워드 , 이름, 우편 번호, 주소, 휴대폰 번호 
    """
    current_ticket_reservations = read_reservation_customer_id(current_customer_id)
    """
    read_reservation_customer_id를 통해, tbl_reservation 테이블에서 저장되어 있는 고객 id와 
    현재 로그인한 고객의 id와 비교해서 일치하는 것을 출력한다. 
    출력결과 -> 예약된 티켓 정보:[<Tbl_reservation reservation_id:106 ticket_id:306 customer_id:1>]
    """
    current_reserved_events = []
    for current_ticket_reservation in current_ticket_reservations:
        current_ticket_id = current_ticket_reservation.ticket_id
        """
        current_ticket_id = current_ticket_reservation.ticket_id 코드는 
        위의 과정에서 현재 로그인한 사람과 예약 내역이 일치한 것을 확인했으므로, 
        예약 테이블에서 예약된 사람과 티켓 id , 예약 id 같은 것을 불러온다. 
        """
        current_event_id = read_ticket_one(current_ticket_id).event_id
        """
        현재 로그인 한 사람으로 예약된 티켓 id를 들고와서, 티켓 테이블의 모든 행을 출력한다. 
        그리고 출력된 행 중에서 event_id의 속성 값을 현재 이벤트 id로 저장한다.
        """
        current_reserved_event= read_event_one(current_event_id)
        
        """
        한 개의 이벤트를 출력한다. -> 현재 티켓에 해당되는 이벤트 id를 들고가서, 
        해당되는 이벤트의 내용을 출력한다.  
        
        """
        """
        print(f"현재 예약된 이벤트 :{current_reserved_event}")
        출력 결과 -> 현재 예약된 이벤트 :<Mst_event event_id:2 event_category_id:1 event_name:bts live event_date:20230630 event_place:seoul event_overview:bts>
        """
        current_reservation_id = current_ticket_reservation.reservation_id
        """
        Tbl_reservation 테이블의 reservation_id:106 값을 들고옴.  
        """
        print(f"현재 예약된 이벤트 id : {current_reservation_id}")
        current_reservation_info = (current_reserved_event, current_reservation_id)
        """
        현재 예약된 이벤트의 정보와 id를 넣는다. 
        """
        current_reserved_events.append(current_reservation_info)
        print(f"예약된 정보 {current_reserved_events}")
        """
        현재 예약된 정보 출력 :

        [(<Mst_event event_id:2 event_category_id:1 event_name:bts live event_date:20230630 event_place:seoul event_overview:bts>, 107)]
        """
        # print(current_reservation_id)
        # print(current_reservation_info)
    return render_template('/customer/mypage/mypage_top.html', current_customer=current_customer, current_reserved_events=current_reserved_events)
    """
    현재의 로그인 한 사람의 정보와 로그인한 사람이 예약한 이벤트의 정보를 전달한다. 
    """

@app.route("/mypage/customer_info/<string:mode>", methods=['GET', 'POST'])
@is_customer_login
def show_customer_info_form(mode:str):
    """
    会員情報のフォーム
    modeによって表示する内容を若干変更する。
    残りの実装内容：無し
    """
    current_customer_id = session['logged_in_customer_id']
    info_messages = InfoMessages()
    error_messages = ErrorMessages()
    customer = read_customer_one(current_customer_id)
    """
    현재 로그인 한 사용자의 id를 가지고 customer에 불러온다. -> 현재 사용자의 id, 어카운트, 패스워드 등등 
    """
    if mode == 'update':
        return render_template('/customer/mypage/customer_edit_form.html', customer=customer, mode=mode)
    if mode == 'delete':
        """
        予約履歴の確認
        """


        reserved_event = read_reservation_customer_id(current_customer_id)
        if reserved_event:
            flash(error_messages.w17())
            return redirect(url_for('show_mypage'))
        return render_template('/customer/mypage/customer_delete_form.html', customer=customer, mode=mode)


@app.route("/mypage/<string:mode>/confirm", methods=['POST'])
@is_customer_login
def show_customer_info_form_confirm(mode:str):
    """
    キャンセルボタンが押された場合は問答無用でshow_mypageに遷移する
    会員情報の確認画面を表示する。
    modeによって表示する内容を変える。
    残りの実装内容：
    ・UPD: 無
    ・DEL: 無
    """

    """
    회원 정보 변경에서 입력한 데이터를 가지고 일로옴. 
    """

    if request.form.get("button") == "cancel":
        """
        <button type="submit" class="btn btn-secondary" name="button" value="cancel">キャンセル</button>
        위의 html에서 눌러진 버튼의 value가 cancel일 때, 이 if문이 실행됨. 
        """
        return redirect(url_for('show_mypage'))
        """
        캔슬 버튼이 눌러졌으면, 마이페이지 화면으로 돌아감. 
        """
    
    if mode == 'update':
        """
        만약, mode가 업데이트라면, 회원의 정보를 변경한다. 
        """
        current_customer_id = request.form.get('customer_id')
        """
        회원 정보 변경 입력폼에 입력한 값을 들고오지만, customer_id는 
        현재의 로그인한 고객의 id가 자동으로 들어가있는 것으로, 유저가 입력한 것은 아님. 
        """
        current_customer = read_customer_one(current_customer_id)
        """
        현재의 고객 아이디를 읽어서, 현재 로그인한 고객의 모든 정보를 들고온다. 
        """
        """
        バリデーションチェックするための関数が欲しい→実装した
        """
        error_messages = customer_info_validate(request)
        if error_messages:
            for error_message in error_messages:
                flash(error_message)
            return redirect(url_for('show_customer_info_form', mode="update"))
        else:
            session["customer_info"] = request.form
            print(session["customer_info"])
            return render_template('/customer/mypage/customer_edit_form_confirm.html', mode=mode, req=session["customer_info"]) 
    if mode == 'delete':
        current_customer_id = session.get('logged_in_customer_id')
        current_customer = read_customer_one(current_customer_id)
        return render_template('/customer/mypage/customer_delete_form_confirm.html', customer=current_customer, mode=mode)

@app.route("/mypage/<string:mode>/overwrite", methods=['POST'])
@is_customer_login
def customer_info_overwrite(mode:str):
    """
    キャンセルボタンが押された場合は問答無用でshow_mypageに遷移する
    渡されたmodeに応じて以下のように処理する。
    update:会員IDを受け取った情報で置き換える。パスワードだけは特殊な処理が必要。
    delete:会員IDを取得。取得した会員ID情報を基に、DBから会員情報を取得。取得した会員情報を削除する。

    残りの実装内容:
    UPD: マージ処理
    DEL: 済
    """
    infoMessage = InfoMessages()
    if request.form.get("button") == "cancel":
        return redirect(url_for('show_mypage'))
    
    current_customer_id = session['logged_in_customer_id']
    current_customer = read_customer_one(current_customer_id)

    if mode=='update':
        """
        今から実装する
        会員情報の上書き
        セッション情報の変更
        """
        current_customer.customer_account = request.form.get('customer_account')
        current_customer.customer_password =  sha256(request.form.get('customer_password').encode()).hexdigest()
        current_customer.customer_name = request.form.get('customer_name')
        current_customer.customer_zipcode = request.form.get('customer_zipcode')
        current_customer.customer_address = request.form.get('customer_address')
        current_customer.customer_phone = request.form.get('customer_phone')

        db.session.merge(current_customer)
        db.session.commit()

        current_customer = read_customer_one(current_customer_id)
        print(current_customer)
        session['logged_in_customer'] = True
        session['logged_in_customer_account'] = current_customer.customer_account
        session['logged_in_customer_id'] = current_customer.customer_id
        session['logged_in_customer_name'] = current_customer.customer_name
        flash(infoMessage.i02('会員情報'))
        return redirect(url_for('show_mypage'))
    if mode=='delete': 
        for key in list(session.keys()):
            session.pop(key, None)
        flash(infoMessage.i04())
        delete_customer(current_customer_id)
        return redirect(url_for('show_customer_event_list'))
    return ('未実装です')


def customer_info_validate(request) -> list:
    """
    フォームに入力された情報が適切か否かを判定する
    現状空判定のみ。
    """
    print(request.form)
    errorMessages = ErrorMessages()
    account_id = request.form.get('customer_id')
    account = request.form.get('customer_account')
    password = request.form.get('customer_password')
    pass_confirm = request.form.get('customer_password_confirm')
    name = request.form.get('customer_name')
    zipcode = request.form.get('customer_zipcode')
    address = request.form.get('customer_address')
    phone_number = request.form.get('customer_phone')
    messages = []
    """
    アカウント名のバリデーションチェック。
    空でない
    メールアドレス形式ではない
    重複していない
    もし重複している場合は現在のそれとアカウント名と等しい
    """
    current_customer = read_customer_one(account_id)

    if account == '':
        messages.append(errorMessages.w02('アカウント名'))
        """
        아무것도 입력 안했을 때, 필수항목이라는 에러가 출력된다. 
        """
    elif not re.fullmatch("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", account):
        messages.append(errorMessages.w18('アカウント名', 'メールアドレス'))
    else:
        found_customers = read_customer_customer_account(account)
        for found_customer in found_customers:
            if found_customer.customer_id == current_customer.customer_id:
                continue
            else:
                messages.append(errorMessages.w03('アカウント名'))
                """
                'この' + arg1 + 'は既に使われています。' 이 '어카운트명'은 이미 사용되고 있습니다. 
                """
                

    """
    パスワードのバリデーションチェック。
    空でない...?本当に…?
    英数字8文字以上20文字以下
    """
    if password == '':
        messages.append(errorMessages.w02('パスワード'))
    elif not re.fullmatch("^[a-zA-Z0-9]{8,20}", password):
        messages.append(errorMessages.w18('パスワード', '半角英数字8文字以上20文字以下'))

    """
    確認用パスワードのバリデーションチェック
    空でない
    パスワードと一致しない
    """

    if pass_confirm == '':
        messages.append(errorMessages.w02('パスワード(確認用)'))
    elif pass_confirm != password:
        messages.append(errorMessages.w05())

    """
    会員名のバリデーションチェック
    空でない
    """
    if name == '':
        messages.append(errorMessages.w02('会員名'))

    """
    郵便番号のバリデーションチェック
    空でない
    半角数字数字7桁
    """
    if zipcode == '':
        messages.append(errorMessages.w02('郵便番号'))
    elif not re.fullmatch("^[0-9]{7,7}", zipcode):
        messages.append(errorMessages.w18('郵便番号', '半角数字7桁'))

    """
    住所のバリデーションチェック
    空でない
    """
    if address == '':
        messages.append(errorMessages.w02('住所'))

    """
    電話番号のバリデーションチェック
    空でない
    半角数字10桁以上11桁以下
    """
    if phone_number == '':
        messages.append(errorMessages.w02('電話番号'))
    elif not re.fullmatch("^[0-9]{10,11}", phone_number):
        messages.append(errorMessages.w18('電話番号', '半角数字10桁か11桁'))

    return messages