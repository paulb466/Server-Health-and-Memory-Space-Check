from datetime import datetime
import time
import sys
import psutil
import os
import subprocess
import requests


# function to send Telegram msgs
def send_Tlg_msg(message):
	try:
		TOKEN = "************"		         
		chat_id = 00000000000
		telegram_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
		params = {
			'chat_id': chat_id,
			'text': message,
			'parse_mode': 'HTML',
		}
		response = requests.post(telegram_url, params=params)
	except Exception as e:
		logging.info("Possible internet communication error - Could not send Telegram message - Error is: "+str(e))




# Open a file in write mode

with open('/docker/webpage/webserver_serverhealth/Server_Health.txt', 'w') as file:

	sys.stdout = file

	current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	print("Data collected on: ",current_time,"\n\n")

	# CPU & RAM Info
	# cpu_usage = psutil.cpu_percent()
	print("----------------CPU, RAM, & SERVER INFO----------------")
	cpu_usage = psutil.cpu_percent(interval=2)
	print(f"Current CPU Usage: {cpu_usage}%")
	ram = psutil.virtual_memory()
	print(f"Current Ram Usage: {ram.percent}%")
	print()
	print("Dell PowerEdge iDRAC information")
	result = subprocess.run(['ipmi-sensors', '--record-ids=11,30,60,115'], stdout=subprocess.PIPE, text=True)
	file.write(result.stdout)

	print()

	#-----------------------------------------------------------------------------------------

	disk_list = ['/dev/sdb', '/dev/sdc', '/dev/sdd', '/dev/sde', '/dev/sdf', '/dev/sdg']

	#-----------------------------------------------------------------------------------------

	print("----------------HARD DRIVE FREE DISK SPACE----------------")
	# Free disk space
	disk_a = psutil.disk_usage("/mnt/movies")
	print(f"Free Space on /mnt/movies:           {disk_a.free / (1024 ** 3):,.0f} GB")
	disk_b = psutil.disk_usage("/mnt/tv_shows")
	print(f"Free Space on /mnt/tv_shows:         {disk_b.free / (1024 ** 3):,.0f} GB")
	disk_c = psutil.disk_usage("/mnt/various")
	print(f"Free Space on /mnt/various:          {disk_c.free / (1024 ** 3):,.0f} GB")
	disk_d = psutil.disk_usage("/mnt/snapraid_parity")
	print(f"Free Space on /mnt/snapraid_parity:  {disk_d.free / (1024 ** 3):,.0f} GB")
	disk_e = psutil.disk_usage("/mnt/qbit")
	print(f"Free Space on /mnt/qbit:             {disk_e.free / (1024 ** 3):,.0f} GB")
	disk_ab = psutil.disk_usage("/")
	print(f"Free Space on /:                     {disk_ab.free / (1024 ** 3):,.0f} GB")

	print()

	#-----------------------------------------------------------------------------------------


	# Smart Check
	# have to figure out how to run this once a day
	print("----------------HARD DRIVE SMART CHECKS----------------")
	print("This is only performed once a day, between 9-10:30 AM")
	current_time = datetime.now().strftime("%H:%M")
	if current_time >= "09:00" and current_time <= "10:30":

		with open('/docker/webpage/webserver_serverhealth/Computer_SmartCheck.txt', 'w') as file_2:

			full_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			print("Last Smart Check Performed: ",full_datetime,"\n")
			file_2.write(f"Last Smart Check Performed: {full_datetime}\n")

			for x in disk_list:
				try:
					result = subprocess.run(['smartctl', '-H', x], capture_output=True, text=True, check=True)
					result = result.stdout.split('\n')
					result2 = (result[-3])[-6:]
					print(f"{x} SMART check result: {result2}")
					file_2.write(f"\n {x} SMART check result: {result2}")
					if result2 != "PASSED":
						send_Tlg_msg(f"Hard drive {x} did not pass Smart Test")
				except:
					result = subprocess.run(['smartctl', '-H', x], capture_output=True)
					print(f"{x} SMART check result: {result}")
					file_2.write(f"\n {x} SMART check result: {result}")
		file_2.close()
	else:

		with open('/docker/webpage/webserver_serverhealth/Computer_SmartCheck.txt', "r") as file_3:
			for line in file_3:
				print(line.strip())  # strip() remo
		file_3.close()

	print()

	#-----------------------------------------------------------------------------------------

	# Hard drive temperature
	print("----------------HARD DRIVE TEMP'S----------------")
	def get_hard_drive_temperature(disk):
		try:
	        	result = subprocess.run(['smartctl', '-a', disk], capture_output=True, text=True, check=True)
		        temperature_line = [line for line in result.stdout.split('\n') if "Temperature_Celsius" in line]
		        temperature = temperature_line[0].split()[-1] if temperature_line else "N/A"
		        print(f"Hard Drive {disk} Temperature: {temperature}°C")
		except subprocess.CalledProcessError as e:
			print(f"Hard Drive {disk} Temperature: Cannot detect temperature")
			return f"Error getting hard drive temperature: {e}"

	for x in disk_list:
		get_hard_drive_temperature(x)

	print()

	#-----------------------------------------------------------------------------------------

	print("----------------HARD DRIVE GLOSSARY----------------")
	print("/dev/sdb - Linux boot drive")
	print("/dev/sdc - qbit drive")
	print("/dev/sdd - various drive")
	print("/dev/sde - tv_shows drive")
	print("/dev/sdf - movies drive")
	print("/dev/sdg - snapraid drive")

	sys.stdout = sys.__stdout__




# Send telegram msg with server health check
if current_time >= "08:55" and current_time <= "09:05":
	try:
		with open('/docker/webpage/webserver_serverhealth/Server_Health.txt', 'r') as file:
			contents = file.read()
			send_Tlg_msg("PowerEdge T420\nServer Health Check\n\n"+contents)
	except FileNotFoundError:
	    send_Tlg_msg(f"PowerEdge T420\nServer Health Check\n\n"+"The file '{file}' was not found.")
	except IOError:
	    send_Tlg_msg(f"PowerEdge T420\nServer Health Check\n\n"+"An error occurred while reading the file '{file}'.")