from flask import Flask, render_template, url_for, request, escape, session, redirect
from os import urandom
from config.dbconnect import DatabaseConnection
from config.tok import Token


app = Flask(__name__)

database = DatabaseConnection()

# Hier wird die Verbindung mit der MySQL Datenbank hergestellt, ist die Verbindung nicht erfolgreich, wird das Programm beendet.
if not database.start_connection('127.0.0.1', 'julius', 'qaywsx', 'chatbot'):
    print('Es kann keine Verbindung mit der Datenbank hergestellt werden.')
    exit(-1)

# Um die Kommunikation sicherer zu machen, werden an alle Daten, die der User sendet ein Token herangehängt.
tok = Token(database)


# Wenn der User auf die Seite '/' kommt wird auf die Startseite unserer Seite weitergeleitet.
@app.route('/')
def catch_root():
    return redirect('/0')


# Das hier ist die Hauptseite
@app.route('/<int:site>', methods=['get', 'post'])
def root(site):
    # Versucht ein User auf unerlaubte Seiten zuzugreifen, wird dieser wieder auf die Startseite weitergeleitet.
    if "valid_request" not in session:
        site = 0
    
    # Die erste Seite hat die Nummer 1, dann geht es immer inkrement weiter.
    if site == 0:

        # Wenn die Person weiter klickt, wird eine Nachricht an den Server gesendet.
        if request.method == 'POST':
            instruction = escape(request.form["instruction"])   # Der Befehl, welcher übertragen wurde.
            token = escape(request.form["token"])               # Das Datentoken

            # Wenn das Token authentifiziert ist, kann der User weitermachen.
            if tok.check_token(token):
                if instruction == 'FIRST':
                    session["valid_request"] = True

                    return 'TRUE'
                else:
                    return 'FALSE'
            else:
                return 'FALSE'

        t = tok.create_token()

        # Hier wird die HTML-Seite an den Client geschickt.
        return render_template('index.html', stylesheet=url_for('static', filename='style.css'), scriptsheet=url_for('static', filename='scripts.js'),
                               token=t)

    # Auf der Zweiten Seite wird nach dem Namen gefragt.
    elif site == 1:
        if request.method == 'POST':
            if tok.check_token(escape(request.form["token"])):
                name = escape(request.form["inp"])  # Der Name, welchen der User eingetragen hat.

                if len(name) > 0:
                    # Ist der Name valide, wird er in eine Session-Variable geschrieben, um dann auf den anderen Seiten benutzt werden zu können.
                    session["name"] = name
                    return redirect('/2')   # Dann wird der User auf die 3. Seite weitergeleitet.
                else:
                    # Hat der User nichts eingegeben, wird eine entsprechende Fehlermeldung ausgegeben.
                    return render_template('1.html', stylesheet=url_for('static', filename='style.css'), scriptsheet=url_for('static', filename='scripts.js'),
                                           own_url='/1', token=tok.create_token(), out_text="Bitte gib deinen Namen ein.")
            else:
                return redirect("/0")

        # Hier wird die HTML-Seite an den Client geschickt.
        return render_template('1.html', stylesheet=url_for('static', filename='style.css'),
                               scriptsheet=url_for('static', filename='scripts.js'), own_url='/1', token=tok.create_token())

    # Auf der dritten Seite, wird nach dem Alter gefragt.
    elif site == 2:
        return render_template('1.html', stylesheet=url_for('static', filename='style.css'),
                               scriptsheet=url_for('static', filename='scripts.js'), own_url='/1', token=tok.create_token())

app.secret_key = urandom(90000)     # Die Daten, welche in der Session gespeichert werden, werden mit einem 90.000 Passwort geschützt.
app.run('127.0.0.1', 7007, True)    # Hier wird der Server gestartet.