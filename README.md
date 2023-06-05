## 2023年新人研修向けムジクロチケット実行手順

### １.データベース作成 
<VSCodeのターミナルで実行>
```c
mysql -u root -p
```
password：mysql
```c
create database mujiqlo_ticket;
```

### 2.パッケージのインストール　※Flask研修で実施済み
以下を**全文**コピーしてターミナルに貼り付け、実行。
```c
pip install click==8.0.4\
    Flask==1.1.2\
    Flask-Script==2.0.6\
    Flask-SQLAlchemy==2.5.1\
    greenlet==1.1.2\
    itsdangerous==2.0.1\
    Jinja2==3.0.3\
    MarkupSafe==2.1.1\
    PyMySQL==1.0.2\
    setuptools==54.2.0\
    SQLAlchemy==1.4.32\
    Werkzeug==2.0.3\
    cryptography==39.0.2
```
パッケージのインストール状況は以下のコマンドで確認
```c
pip list
```

### 3.テーブル作成 
<VSCodeのターミナルで実行>

・mujiqloディレクトリに移動して実行
```c
python manage.py init_db
```

### 4.ムジクロチケットの実行 
<VSCodeのターミナルで実行>

```c
python server.py
```

・chromeで http://127.0.0.1:5000/ にアクセスする
・'staff001','password'でログインする


***

<memo>
開発に使った環境
Python 3.9.4

Package          Version
--------------   -------
- click            8.0.4
- Flask            1.1.2
- Flask-SQLAlchemy 2.5.1
- greenlet         1.1.2
- itsdangerous     2.0.1
- Jinja2           3.0.3
- MarkupSafe       2.1.0
- pip              21.0.1
- PyMySQL          1.0.2
- setuptools       54.2.0
- SQLAlchemy       1.4.32
- Werkzeug         2.0.3



