class apiMessage:
	def __init__(self, ip, port, msg):
		self.ip=ip
		self.port=port
		self.msg=msg

	def processMessage(self):
		print 'PROCESSING MESSAGE'
		print 'FROM: ', self.ip, "\nPORT: ", self.port
		print 'MESSAGE: ', self.msg, "\n"
		pieces = self.msg.split(',')
		cmd = pieces[0]
		if cmd == 'mouse_l': 
			print "Left mouse down\n"
		elif cmd == 'mouse_lu':
			print "Left mouse up\n"
		elif cmd == 'mouse_m':
			print "Mouse wheel down\n"
		elif cmd == 'mouse_mu':
			print "Mouse wheel up\n"
		elif cmd == 'mouse_r':
			print "Right mouse down\n"
		elif cmd == 'mouse_ru':
			print "Right mouse up\n"
