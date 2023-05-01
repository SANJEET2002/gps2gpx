import serial
import threading
import datetime
import time
import gpxpy.gpx


class Gps2Gpx:
    is_service_started = False
    gpgga_string = "$GPGGA,"
    port = "/dev/ttyS0"
    connected_to_satelite = False
    is_recording_gps = False
    is_worker_running = False
    baudrate = 9600
    def __init__(self,port,baudrate,folder):
        self.port = port
        self.folder = folder
        self.baudrate = baudrate
        self.start_service()

    
    def start_service(self):
        try:
            self.serial_port = serial.Serial(self.port , baudrate=self.baudrate , timeout=1)
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

        data = None

        while True:
            data = self.serial_port.readline().decode('utf-8')

            if data.find(self.gpgga_string) > -1:
                break;

        if data:
            GPGGA_data_available = data.find(self.gpgga_string)

            if (GPGGA_data_available > -1):
                raw_data =  data.split(",")
                if int(raw_data[7]) <= 3:
                    print('not enough statelites in view')
                    self.connected_to_satelite = False
            
                elif raw_data[2] and raw_data[4]:
                    # extract the latitude and longitude information
                    lat = float(raw_data[2][:2]) + float(raw_data[2][2:]) / 60
                    lon = float(raw_data[4][:3]) + float(raw_data[4][3:]) / 60
                    
                    # check if latitude is South and flip the sign if it is
                    if raw_data[3] == "S":
                        lat = -lat
                    
                    # check if longitude is West and flip the sign if it is
                    if raw_data[5] == "W":
                        lon = -lon

                    self.connected_to_satelite = True

                    return { 'longitude' : round(lon, 6) , "latitude" : round(lat,6)}

                else:
                    print('unable to parse data ----> \n')

            else:
                print('no valid string')

    def gps_recording_worker(self):
        self.is_worker_running = True
        self.is_recording_gps = True
        startTime = datetime.datetime.now().strftime("%d-%m-%y-%H-%M-%S")

        gpx = gpxpy.gpx.GPX()
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)

        if not self.is_service_started:
            print('service not running ----> \n')
            self.is_worker_running = False
            return 
        
        else:
            while True:
                if self.is_recording_gps:
                    cordinates = self.get_cordinates()
                    print(cordinates)
                    if cordinates:
                        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(cordinates['latitude'], cordinates["longitude"], time=datetime.datetime.now()))
                else:
                    try:
                        with open(f"{self.folder}/{startTime}.gpx", "w") as f:
                            f.write(gpx.to_xml())
                            print("saved cordinates into gpx file \n")
                        break
                    except Exception as e:
                        print(e)


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




if __name__ == "__main__":
    converter = Gps2Gpx(port='/dev/ttyS0',baudrate=9600,folder="./")
    converter.start_worker()
    time.sleep(10)
    converter.stop_worker()
