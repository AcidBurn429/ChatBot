from mysql.connector import connect
from mysql.connector.errors import InterfaceError


# Diese Klasse ermöglicht das Verbinden mit einer Datenbank
class DatabaseConnection:
    # Im Konstruktor werden die Klassenvariablen initialisiert.
    def __init__(self):
        self.mysql = None
        self.cursor = None

    # Mit der Funktion "start_connection" wird eine Verbindung zu einem MySQL-Server gestartet
    def start_connection(self, hostname, username, password, db):
        try:
            self.mysql = connect(host=hostname, user=username, passwd=password, database=db)
            self.mysql.autocommit = True    # Diese Zeile ermöglicht das automatische Neuladen nach einer Änderung

            return True
        except InterfaceError:
            return False

    # Ist es notwendig, dass man sich mit der Datenbank neu verbinden muss, stellt diese Funktion dies zur
    # Verfügung
    def refresh(self):
        self.mysql.reconnect()

    # Um SQL-Abfragen zu machen, wird diese Funktion benutzt.
    def execute(self, statement, variables, ret= False):
        cursor = self.mysql.cursor(prepared=True)
        cursor.execute(statement, variables)
        if ret:
            return cursor

    # Um die MySQL-Verbindung zu beenden wird diese Funktion benutzt.
    def close_connection(self):
        self.mysql.close()
