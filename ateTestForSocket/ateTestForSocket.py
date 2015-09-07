import sys
import string
from socket import *
import MySQLdb
def main():
	conn= MySQLdb.connect(
			host='localhost',
			port = 3306,
			user='root',
			passwd='root',
			db ='mysql')
	cur = conn.cursor()
	cur.execute("create table if not exists ate(id int, sendValue varchar(1024))")
	#get all message
	message = []
	count = cur.execute("select * from ate")
	print(count)

	if (count != 0):
		result = cur.fetchall()
		for i in result:
			print(i)
			print(i[0])
			print(i[1])
			message.append(i)


# server connect start here
	serverHost = '127.0.0.1'
	serverPort = 8899



	sockobj = socket(AF_INET, SOCK_STREAM)
	sockobj.connect((serverHost, serverPort))
	try:
		conn=MySQLdb.connect(host='localhost',user='root',passwd='root',db='test',port=3306)
		cur=conn.cursor()
		cur.execute('select * from user')
		cur.close()
		conn.close()
	except MySQLdb.Error,e:
		print ("Mysql Error %d: %s" % (e.args[0], e.args[1]))
	while(1):
		userInput = raw_input("Enter your input: ")
		if(userInput == 'q'):
			break
		elif(userInput == 'a'):
			userInput = raw_input("Enter id you want add:")
			iAdd = string.atoi(userInput)
			userInput = raw_input("Enter what you want to add:")
			insertArr = [iAdd, userInput]
			cur.execute("insert into ate values(%s, %s)", insertArr)
			message.append((iAdd,userInput))
		elif(userInput == 'p'):
			iToPrint = 0
			for i in message:
				print(iToPrint)
				print(i)
				iToPrint = iToPrint + 1
		elif(userInput == 'd'):
			userInput = raw_input("Enter which you want to delete:")
			iDelete = string.atoi(userInput)
			deleteArr = [message[iDelete][0]]
			cur.execute('delete from ate where id=%s', deleteArr)
			del message[iDelete]
		elif(userInput == 's'):
			userInput = raw_input("Enter which you want to send:")
			iSend = string.atoi(userInput)
			sockobj.send(message[iSend][1] + '\n')
			data = sockobj.recv(1024)
			print(data)

	cur.close()
	conn.commit()
	conn.close()
	sockobj.close()
main()
