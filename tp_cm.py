import serial
import time
import csv
import os




def connect_serial(com_port,timeout):
	global ser
	ser=serial.Serial(com_port,baudrate=38400, timeout=timeout)


def make_measurements(csv_name,time_meas):
	ser.write("${}\r\n".format('GO').encode())
	ser.flushInput()
	ser.flushOutput()	
	with open(csv_name,"w", newline='') as f:
		writer = csv.writer(f,delimiter=",")
		writer.writerow(['date','time','HD','AZ','INC','SD'])	
		t_end = time.time() + time_meas
		while time.time() < t_end:
			reads = ser.readline()
			decreds = reads.decode("utf-8")
			if decreds == "$OK\r\n":
				pass
			else:
				writer.writerow([time.strftime('%d/%m/%y'),time.strftime('%H:%M:%S'),decreds.split(',')[2],decreds.split(',')[4],decreds.split(',')[6],decreds.split(',')[8]])
			f.flush()
			print("Time left:", int(round(t_end-time.time(),0)), "seconds", end='\r')
			
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
			filename=input("Name of the csv file (with .csv ending):")
			csv_name=os.path.join(os.getcwd(),filename)
			print("Measurement will be saved as:", csv_name)		
			continue
			
		if cmd == "m":
			try:
				if os.path.exists(csv_name) == True:
					print("File already exists")
				else:
					make_measurements(csv_name,time_meas)
					print("Measurement saved at:", csv_name)				
			except NameError:
				print("Time or output not defined; Device connected?")
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