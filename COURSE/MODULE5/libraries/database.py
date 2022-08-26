import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
from libraries.countries import ApiFetcher


class Databases(object): 
    
    
    @classmethod
    def dbCreate(cls):
        cnx = mysql.connector.connect(user='root', password='', host='localhost', database='mydb')
        mycursor=cnx.cursor()
        mycursor.execute("DROP DATABASE mydb")
        mycursor.execute("CREATE DATABASE mydb")
        mycursor.execute("USE mydb")
        reqC = "CREATE TABLE client(idClient INT PRIMARY KEY NOT NULL AUTO_INCREMENT, name VARCHAR(100), phone VARCHAR(25), email VARCHAR(50), address VARCHAR(100), latlng VARCHAR(50) NULL, age INT)"
        mycursor.execute(reqC)
        reqI = "CREATE TABLE income(idIcme INT PRIMARY KEY NOT NULL AUTO_INCREMENT, devise VARCHAR(50), salary INT, salaryInXOF INT)"
        mycursor.execute(reqI)
        reqk = "CREATE TABLE country(idCountry INT PRIMARY KEY NOT NULL AUTO_INCREMENT, country VARCHAR(100), flag VARCHAR(100))"
        mycursor.execute(reqk)
        
        dataframe = ApiFetcher.main()
        val1 = []
        for i in range(len(dataframe)): 
            val1.append((dataframe['name'][i], dataframe['phone'][i], dataframe['email'][i], dataframe['address'][i], str(dataframe['latlng'][i]), str(dataframe['age'][i])))
        req1 = "INSERT INTO client (name, phone, email, address, latlng, age) VALUES (%s, %s, %s, %s, %s, %s)"
        mycursor.executemany(req1, val1) 
        
        val2 = []
        for i in range(len(dataframe)):
            val2.append((dataframe['devise'][i], str(dataframe['salary'][i]), str(dataframe['salaryInXOF'][i])))
        req2 = "INSERT INTO income (devise, salary, salaryInXOF) VALUES (%s, %s, %s)"
        mycursor.executemany(req2, val2) 
        
        val3 = []
        for i in range(len(dataframe)):
            val3.append((dataframe['country'][i], dataframe['flag'][i]))
        req3 = "INSERT INTO country (country, flag) VALUES (%s, %s)"
        mycursor.executemany(req3, val3)



    @classmethod
    def main(cls):
        conn = Databases.dbCreate()
        return conn
