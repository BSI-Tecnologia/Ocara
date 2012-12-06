#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
	Script de correção da tabela schedule_of_borrow
"""

import psycopg2
from string import *
from datetime import *
import os

print "### rotina de atualizações para as novas funcionalidades e e correções do Ocara iniciada."

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
    dbCursor.execute("SELECT * FROM schedule_of_borrow")
    result_list = dbCursor.fetchall()
    try:
        for result in result_list:
            dbCursor.execute("INSERT INTO schedule_of_borrow_bkp VALUES (%s, %s, %s, %s, %s, %s, %s)", (result[0],result[1],result[2],result[3],result[4],result[5],result[6]))
    except Exception, error1:
        print "### Erro ao inserir os dados antigos de empréstimos na tabela de backup > ", error1
    dbCursor.execute("DELETE FROM schedule_of_borrow")
    dbCursor.execute("ALTER TABLE schedule_of_borrow DROP COLUMN name_heritage;")
    dbCursor.execute("ALTER TABLE schedule_of_borrow ADD COLUMN heritage_id integer;")
except Exception, error2:
    print "### Erro ao criar a tabela de backup dos empréstimos > ", error2

sql_txt = open( '/tmp/sql.txt')
sql_cmds = sql_txt.readlines()
for cmd in sql_cmds :
    try:
        dbCursor.execute(cmd)
        print ">>> OK >>> %s" % (cmd,)
    except Exception, error:
        print ">>> ERRO >>> %s >>> %s" % (cmd, error,)
sql_txt.close()


conn.commit()
conn.close()

print "### rotina de atualizações para as novas funcionalidades e e correções do Ocara executada."
