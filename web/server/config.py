
import mysql.connector
import datetime
class DB:
    def __init__(self):
        # self.db_name = db_name
        self.connect = mysql.connector.connect(
            host =  'localhost',
            user = 'root',
            password = 'ahmed@2002',
            database = 'my_syotame_app'
        )
        if self.connect.is_connected(): print('La connexion est réunie')
        self.cursor = self.connect.cursor()

    def sendData(self, name, address, full_place, hand_palce, occupied):
        # Utilisation de datetime pour obtenir la date actuelle dans le bon format
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Format correct : 'YYYY-MM-DD HH:MM:SS'

        # Préparation de la requête SQL
        query = """
            INSERT INTO parking (agency, address, full_place, hand_place, occupied, created_at, updated_at) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        # Les valeurs à insérer, y compris les dates au format correct
        values = (name, address, full_place, hand_palce, occupied, current_time, current_time)

        # Exécution de la requête
        self.cursor.execute(query, values)
        self.connect.commit()
        print(f'{self.cursor.rowcount} enregistrement(s) inséré(s)')
