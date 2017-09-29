# Imports
import os
import time
import logging


# Setups
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


# Variables
base_dir = '/sys/bus/w1/devices/'


# Settings
sleep_time = 300
log_weather = 'Y'
temp_format = 'F'
logs_folder = 'logs/'
th_high = 80
th_low = 70
device_list = {'28-0516a1a7d7ff':'Sensor 1',
     	       '28-0416b059cfff':'Sensor 2'}


# Functions
def space():
    space = '\n' + 32 * '-' + '\n'
    print(space)


def device_check():
    for device_id, device_name in device_list.items():

        temp_data_file = logs_folder + device_id
        device_id_loc = base_dir + device_id + '/w1_slave'

        def read_temp_raw():
            f = open(device_id_loc, 'r')
            lines = f.readlines()
            f.close()
            return lines
        
        def read_temp():
            lines = read_temp_raw()

            while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                lines = read_temp_raw()
            
            equals_pos = lines[1].find('t=')

            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                temp_f = temp_c * 9.0 / 5.0 + 32.0
                return temp_c, temp_f
        
        def temp_action():
            att = "None"
            if ctemp_f <= int(th_low):
                att = "None"
                return att
            elif ctemp_f >= int(th_high):
                att = "Fan ON"
                return att

        def write_to_log():
            log_data = [device_name, device_id, ctemp_f, ctemp_c, current_time, actiontt]

            print("Logging : {} \n".format(log_data))

            if os.path.exists(temp_data_file) == False:
                open(temp_data_file, 'a').close()
                print("The file {} has been Created ...".format(temp_data_file))

            with open(temp_data_file, mode='+a', encoding='utf-8') as log_open:
                final_write_data = str(log_data) + '\n'
                log_open.write(final_write_data)
                log_open.close()
        
        current_time = time.ctime()
        current_temp = read_temp()
        ctemp_f = int(current_temp[1])
        ctemp_c = int(current_temp[0])
        actiontt = temp_action()

        print('Checking {}'.format(device_name))
        print('Sensor file location: {}'.format(device_id_loc))
        print('Action : {}'.format(actiontt))



        if temp_format.upper() == 'F':
            print("Current temp on {} is : {}F at {}".format(device_name, ctemp_f, current_time, actiontt))
        else:
            print("Current temp on {} is : {}C at {}".format(device_name, ctemp_c, current_time, actiontt))
     
        if log_weather.upper() == 'Y':
            write_to_log()


# App Call
while True:
    space()
    device_check()
    time.sleep(sleep_time)
