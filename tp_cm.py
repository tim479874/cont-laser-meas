import serial
import time
import csv




def connect_serial(com_port,timeout):
	global ser
	ser=serial.Serial(com_port,baudrate=38400, timeout=timeout)


def make_measurements(csv_name,time_meas):
	ser.write("${}\r\n".format('GO').encode())
	ser.flushInput()
	ser.flushOutput()
	
	with open(csv_name,"a", newline='') as f:
		writer = csv.writer(f,delimiter=",")
		writer.writerow(['date','time','HD','AZ','INC','SD'])
	
	
		t_end = time.time() + time_meas
		while time.time() < t_end:
			reads = ser.readline()
			decreds = reads.decode("utf-8")
			writer.writerow([time.strftime('%d/%m/%y'),time.strftime('%H:%M:%S'),decreds[10:14],decreds[17:23],decreds[26:30],decreds[33:37]])
			f.flush()
			
	ser.write("${}\r\n".format('ST').encode())
	
def main():
		
	while True:
	
		cmd= input("Command: (type '?' for help)")
		
		if cmd == "p":
			com_port=input("Port at which the TruePulse is connected:")
			print("TruePulse connected at:", com_port)
			timeout=int(input("Timeout:"))
			print("Timeout set at:" , timeout , "seconds")
			continue
			
		if cmd == "s":
			time_meas=int(input("Time of measurement:"))
			print("Time of measurement:", time_meas , "seconds")
			continue

		if cmd == "c":
			try:
				connect_serial(com_port,timeout)
				if ser.isOpen() == True:
					print("Connection established")
			except NameError:
				print("No port definied")
			except:
				print("Could not connect to TruePulse: wrong port?")
			continue
			
		if cmd == "d":
			try:
				ser.write("${}\r\n".format('TM,1').encode())
				ser.write("${}\r\n".format('AU,0').encode())
				ser.write("${}\r\n".format('DU,0').encode())
				ser.write("${}\r\n".format('MM,2').encode())
			except:
				print("No device connected")
			continue
			
		if cmd == "t":
			csv_name=input("Name of the csv file (with .csv ending):")
			print("Measurement will be saved as:", csv_name)		
			continue
			
		if cmd == "m":
			try:
				make_measurements(csv_name,time_meas)
			except:
				print("Time or output not defined")
			continue
			

		
		if cmd == "e":
			try:
				ser.flushInput()
				ser.flushOutput()
				ser.close()
			except:
				print("No device connected")
			continue
			
		if cmd == "?":
			print("""
			s: settings (length of measuremnt)
			p: serial port settings (port, timeout)
			c: connect to Truepulse
			d: load default Truepulse settings [Continoues target mode, slope distance, angles in degrees, distance in meters]
			t: name for text file
			m: take measurements
			e: close serial port
			q: quit
			""")			
			continue
			
		if cmd == "q":
			break
			
main()