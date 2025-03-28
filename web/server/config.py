
import mysql.connector
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

    def sendData(self,name,address,full_place,hand_palce,occupied):
        query = "INSERT INTO parking (agency,address,full_place,hand_place,occupied) VALUES(%s,%s,%s,%s,%s)"
        values = (name,address,full_place,hand_palce,occupied)
        self.cursor.execute(query,values)
        self.connect.commit()
        print(f'{self.cursor.rowcount} enregistrement insére')