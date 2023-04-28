import serial
import threading
import datetime


class GPS:
    is_service_started = False
    gpgga_string = "$GPGGA,"
    port = "/dev/ttyS0"
    connected_to_satelite = False
    file_name = datetime.datetime.strfStrig("%d-%m-%y-%H-%M-%S")
    is_recording_gps = False
    is_worker_running = False
    def __init__(self,port,file_name):
        self.port = port
        self.file_name = file_name
        self.start_service()

    
    def start_service(self):
        try:
            self.serial_port = serial.Serial(self.port , baudrate=9600 , timeout=1)
            self.is_service_started = True
        except PermissionError:
            self.is_service_started = False
            print('Unable to access serial Port due to Permissio Error -----> \n')

    def test_gps_sensor(self):
        received_data = self.serial_port.readline().decode('utf-8')

        if received_data:
            print('gps_sensor is working -----> \n')
        else:
            print('no data received ,check gps is connected --------> \n')

    def get_cordinates(self):
        data = self.serial_port.readline().decode('utf-8')

        if data:
            GPGGA_data_available = data.find(self.gpgga_string)

            if (GPGGA_data_available > -1):
                raw_data =  data.split(",")
                if int(raw_data[7]) <= 3:
                    print('not enough statelites in view')
                    self.connected_to_satelite = False
                    return
            
                if raw_data[2] and raw_data[4]:
                    # extract the latitude and longitude information
                    lat = float(raw_data[2][:2]) + float(raw_data[2][2:]) / 60
                    lon = float(raw_data[4][:3]) + float(raw_data[4][3:]) / 60
                    
                    # check if latitude is South and flip the sign if it is
                    if raw_data[3] == "S":
                        lat = -lat
                    
                    # check if longitude is West and flip the sign if it is
                    if raw_data[5] == "W":
                        lon = -lon

                    return { 'longitude' : round(lon, 6) , "latitude" : round(lat,6)}

                else:
                    print('unable to parse data ----> \n')


    def gps_recording_worker(self):
        self.is_worker_running = True
        if not self.is_service_started:
            print('service not running ----> \n')
            self.is_worker_running = False
            return 
        elif not self.connected_to_satelite:
            print('not connected to satelite ----> \n')
            self.is_worker_running = False
            return
        
        else:
            while self.is_recording_gps:
                cordinates = self.get_cordinates()
                print(cordinates)

    def start_worker(self):
        self.t1 = threading.Thread(target=self.gps_recording_worker)
        self.t1.start()

    def stop_worker(self):
        if not self.is_worker_running:
            print('no working is running')
            return
        
        else:
            self.is_recording_gps = False
            print("worker is now resting")