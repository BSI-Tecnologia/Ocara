#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
	Script de correção da tabela schedule_of_borrow
"""

import psycopg2
from string import *
from datetime import *
import os

print "### rotina de correção da tabela de empréstimo iniciada."

try:
	conn = psycopg2.connect("\
	    dbname='ocara'\
	    user='ocara'\
	    host='localhost'\
	    password='liberdade'\
    ");
except:
	print "### Erro ao conectar ao banco de dados"
	exit()

conn.set_isolation_level(0)
dbCursor = conn.cursor()

try:
    dbCursor.execute("CREATE TABLE schedule_of_borrow_bkp (LIKE schedule_of_borrow)")
except Exception, error:
    print "### Erro ao criar a tabela de backup dos empréstimos > ", error
    exit()

dbCursor.execute("SELECT * FROM schedule_of_borrow")
result_list = dbCursor.fetchall()

try:
    for result in result_list:
        dbCursor.execute("INSERT INTO schedule_of_borrow_bkp VALUES (%s, %s, %s, %s, %s, %s, %s)", (result[0],result[1],result[2],result[3],
            result[4],result[5],result[6]))
except Exception, error:
    print "### Erro ao inserir os dados antigos de empréstimos na tabela de backup > ", error
    exit()

dbCursor.execute("DELETE FROM schedule_of_borrow")

dbCursor.execute("ALTER TABLE schedule_of_borrow DROP COLUMN name_heritage;")

dbCursor.execute("ALTER TABLE schedule_of_borrow ADD COLUMN heritage_id integer;")

conn.commit()
conn.close()

print "### rotina de correção da tabela de empréstimo executada com sucesso."
