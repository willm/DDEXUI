import sqlite3

from ddex.party import Party


class PartyRepository:
    def __init__(self):
        self.__with_cursor(lambda cursor, connection: cursor.execute("CREATE TABLE IF NOT EXISTS party(name text, partyId text, partyType integer)"))

    def __get_connection(self):
        return sqlite3.connect("ddexui.db")

    def get_party(self, party_type):
        connection = self.__get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT partyId, name, partyType FROM party WHERE partyType=?", (party_type,))
        party = cursor.fetchone()
        connection.close()
        if(party == None):
            return None
        return Party(party[0], party[1], party[2])

    def write_party(self, party):
        self.__with_cursor(lambda cursor, connection: self.__write_party(cursor, connection, party))

    def __write_party(self, cursor, connection, party):
        cursor.execute("INSERT INTO party(name, partyId, partyType) VALUES(?,?,?)", (party.name, party.party_id, party.party_type,))
        connection.commit()
        connection.close()

    def __with_cursor(self, action):
        connection = self.__get_connection()
        cur = connection.cursor()
        action(cur, connection)
        connection.close()
