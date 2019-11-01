#! /usr/bin/python3

import cgi
#, cgitb
import os
import json
import MySQLdb
import passwords

#cgitb.enable()
form = cgi.FieldStorage()

def front():
	print("Status: 200 OK")
	print("Content-Type: text/html")
	print()

	if info == "/":
		print("wtf")

	print("""<html>
			<head><title>Home</title></head>
			<body>
				<a href="form">Click here to post something</a><br>
				<p>{}</p>
				<a href="pickles">Click here to get all records</a><br>
			</body>
		</html>""".format(info))
	
	
	
def form():
	print("Status: 200 OK")
	print("Content-type: text/html")
	print()

	print("""<html>
			<form action="pickles" method="POST">
				First name:<br>
				<input type="text" name="first"><br>
				Last name:<br>
				<input type="text" name="last"><br>
				Number of pickles:<br>
				<input type="type" name="numpickles"><br>
				<input type="submit" value="submit">
			</form>
			<p>{}</p>""".format(info))

def foo():
	print("Status: 302 Redirect")
	print("Location: form")
	print()

def redir():
	print("Status: 302 Redirect")
	print("Location: front")
	print()

def jsontest():
	print("Status: 200 OK")
	print("Content-Type: application/json")
	print()

	x = [1, 2, 30, 20, {"foo": "bar"}]
	x_json = json.dumps(x, indent=2)
	print(x_json)

def pickles():
	print("Status: 200 OK")
	print("Content-Type: application/json")
	print()

	for a in os.environ:
		print('Var: ', a, 'Value: ', os.getenv(a))
	print("all done")
	
	if 'REQUEST_METHOD' in os.environ['REQUEST_METHOD']:
		method = os.environ['REQUEST_METHOD'].value
		print(method)

	conn = MySQLdb.connect(host = passwords.SQL_HOST,
				user = passwords.SQL_USER,
				passwd = passwords.SQL_PASSWD,
				db = "baseddata")
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM pickles;")
	results = cursor.fetchall()
	cursor.close()
	conn.close()
	row = []
	for rec in results:
		row.append({"id": rec[0], "first": rec[1], "last": rec[2], "pickles": rec[3],
			    "url": "http://ec2-54-88-136-27.compute-1.amazonaws.com/cgi-bin/restTest.cgi/pickles/"+str(rec[0])})
		results_json = json.dumps(row, indent=2)
	
	print(results_json)

def picklessingle():
	print("Status: 200 OK")
	print("Content-Type: text/html")
	print()
	
	conn = MySQLdb.connect(host = passwords.SQL_HOST,
                                user = passwords.SQL_USER,
                                passwd = passwords.SQL_PASSWD,
                                db = "baseddata")
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM pickles WHERE id=%s;", (info[len(info)-1],))
	results = cursor.fetchall()
	cursor.close()
	conn.close()
	row = []
	row.append({"id": results[0][0], "first": results[0][1], "last": results[0][2], "pickles": results[0][3],
                            "url": "http://ec2-54-88-136-27.compute-1.amazonaws.com/cgi-bin/restTest.cgi/pickles/"+str(results[0][0])})
	results_json = json.dumps(row, indent=2)
	print(results_json)
	

if 'PATH_INFO' in os.environ:
	info = os.environ['PATH_INFO']
else:
	info = "/"

if info == "/":
	front()

elif info == "/form":
	form()
elif info == "/foo":
	foo()
elif info == "/jsontest":
	jsontest()
elif info == "/pickles":
	pickles()
elif info == "/pickles/" + info[len(info)-1]:
	picklessingle()
else:
	print("Status: 404 Not Found")
	print()

	print("The CGI path '{}', underneath the 'pathinfo' tool, was not a valid URL.".format(info))
	
