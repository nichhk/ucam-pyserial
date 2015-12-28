import serial, commands
import time
import re
from binascii import hexlify
from struct import pack, unpack

class UCam(object):
	"""
	An interface to communicate with a uCam-II camera
	over a UART serial connection.
	"""
	
	def __init__(self):
		self.ser = serial.Serial('/dev/ttyAMA0', baudrate=921600, 
				timeout=.01)
		self.synced = False
		print 'initialized'

	def sync(self):
		num_tries = 100
		while num_tries > 0:
			if self._sync():
				return True
			num_tries -= 1
		return False
	
	def _write(self, string):
		return self.ser.write(bytearray(string.decode('hex')))
	
	def _matches(self, pattern, packet):
		packet_str = hexlify(packet)
		return re.match(pattern, packet_str) is not None

	def _sync(self):
		time.sleep(.05)
		self._write(commands.sync())
		read = self.ser.read(6)
		if self._matches(commands.ack('0d', '..'), read):
			if self._matches(commands.sync(), self.ser.read(6)):
				self._write(commands.ack('0d', '00'))
				return True
		return False
	
	def _initial(self):
		init_cmd = commands.initial('07', '07', '07')
		print 'init cmd ', init_cmd
		self._write(init_cmd)
		read = self._wait_for_bytes(6)
		print 'ack ', read
		assert self._matches(commands.ack('01', '..'), read)
	
	def _wait_for_bytes(self, i):
		bytearr = bytearray(i)
		cur = 0
		while cur < i:
			read = self.ser.read(1)
			if len(read) == 1:
				bytearr[cur] = read[0]
				cur += 1
		return bytearr

	def _set_pkg_size(self):
		self._write(commands.set_pkg_size('00', '02'))
		assert self._matches(commands.ack('06', '..'), 
				self._wait_for_bytes(6))

	def _snapshot(self):
		self._write(commands.snapshot('00', '00', '00'))
		assert self._matches(commands.ack('05', '..'), 
				self._wait_for_bytes(6))
	
	def _get_picture(self):
		"""
		Sends the GET PICTURE command and receives the
		corresponding DATA command.
		Returns the number of packets to be read.
		"""
		self._write(commands.get_picture('01'))
		assert self._matches(commands.ack('04', '..'),
				self._wait_for_bytes(6))
		# receive DATA
		data = self._wait_for_bytes(6)
	        assert self._matches(commands.data('01', '..', '..', '..'), 
				data)
		print hexlify(data)
		img_size = unpack('<I', 
				hexlify(data[-3:]).decode('hex') + '\x00')[0]
		print 'image size is ', img_size
		num_pkgs = img_size / (512 - 6)
		print 'num packages ', num_pkgs
		self._write(commands.ack('00', '00'))
		return img_size

	def _write_picture(self, img_size, name='pic.jpeg'):
		num_pkgs = img_size / (512 - 6)
		with open(name, 'wb+') as f:
			for i in range(1, num_pkgs + 1):
				print 'getting package ', i
				read = self._wait_for_bytes(512)
				f.write(read[4:-2])
				hex_idx = hexlify(pack('H', i))			
				print 'hex_idx ', hex_idx
				self._write(commands.ack('00', '00',
					hex_idx[:2], hex_idx[-2:]))
			f.write(self._wait_for_bytes(
				img_size - num_pkgs * (512 - 6)+ 2))
			f.close()
		# ACK end of data transfer
		self._write(commands.ack('f0', 'f0'))

	def take_picture(self, name='pic.jpeg'):
		# initialize for JPEG, VGA
		self._initial()

		# set package size to 512 bytes
		self._set_pkg_size()
		
		# compressed snapshot pic
		self._snapshot()

		# get picture (snapshot)
		num_pkgs = self._get_picture()

		# receive img data pkgs
		self._write_picture(num_pkgs, name)
	
	def reset(self):
		self._write(commands.reset())
