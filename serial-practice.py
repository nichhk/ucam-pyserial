import serial

ser = serial.Serial('/dev/ttyAMA0', timeout=.01)
hello_str = bytearray('deadbeef')
print 'about to write'
wrote = ser.write(hello_str)

print 'wrote ', wrote
print 'string length: ', len(hello_str)
print 'incoming ', ser.inWaiting()
read = ser.read(wrote)
print read
ser.close()
