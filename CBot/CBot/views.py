from flask import Flask, render_template, url_for, request, escape, session, redirect
from os import urandom
from config.dbconnect import DatabaseConnection
from config.tok import Token


app = Flask(__name__)

database = DatabaseConnection()

if not database.start_connection('127.0.0.1', 'julius', 'qaywsx', 'chatbot'):
    print('Es kann keine Verbindung mit der Datenbank hergestellt werden.')
    exit(-1)

tok = Token(database)


@app.route('/')
def catch_root():
    return redirect('/0')


@app.route('/<int:site>', methods=['get', 'post'])
def root(site):
    if "valid_request" not in session:
        site = 0
    
    if site == 0:
        if request.method == 'POST':
            instruction = escape(request.form["instruction"])
            token = escape(request.form["token"])

            if tok.check_token(token):
                if instruction == 'FIRST':
                    session["valid_request"] = True

                    return 'TRUE'
                else:
                    return 'FALSE'
            else:
                return 'FALSE'

        t = tok.create_token()
        print(t)
        return render_template('index.html', stylesheet=url_for('static', filename='style.css'), scriptsheet=url_for('static', filename='scripts.js'),
                               token=t)
    elif site == 1:
        if request.method == 'POST':
            if tok.check_token(escape(request.form["token"])):
                name = escape(request.form["inp"])

                if len(name) > 0:
                    session["name"] = name
                    return redirect('/2')
                else:
                    return render_template('1.html', stylesheet=url_for('static', filename='style.css'), scriptsheet=url_for('static', filename='scripts.js'),
                                           own_url='/1', token=tok.create_token(), out_text="Bitte gib deinen Namen ein.")
            else:
                return redirect("/0")

        return render_template('1.html', stylesheet=url_for('static', filename='style.css'),
                               scriptsheet=url_for('static', filename='scripts.js'), own_url='/1', token=tok.create_token())
    elif site == 2:
        return render_template('1.html', stylesheet=url_for('static', filename='style.css'),
                               scriptsheet=url_for('static', filename='scripts.js'), own_url='/1', token=tok.create_token())

app.secret_key = urandom(90000)     # Die Daten, welche in der Session gespeichert werden, werden mit einem 90.000 Passwort geschützt.
app.run('127.0.0.1', 7007, True)