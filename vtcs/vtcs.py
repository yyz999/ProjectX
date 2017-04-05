import time
import threading
import RPi.GPIO as GPIO
import socket
import sys


class TractionControlSystem:
    # calibration_freq: number of times calibrating per second
    def __init__(self, calibration_freq, port_number):
        self.calibration_freq = 5
        self.port_number = port_number
        #self.direction=0 # [-127, +127]
        #self.magnitude=0 # [-127, +127]
        self.left_counter = 0
        self.right_counter = 0
        self.last_left_counter = 0
        self.last_right_counter = 0
        self.left_pwm_ratio = 0
        self.right_pwm_ratio = 0
        self.last_left_pwm_ratio = 0
        self.last_right_pwm_ratio = 0
        self.left_offset = 1
        self.right_offset = 1
        self.last_cmd_timestamp = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(15, GPIO.OUT)
        GPIO.setup(17, GPIO.OUT)
        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(6, GPIO.OUT)
        GPIO.setup(12, GPIO.OUT)
        GPIO.setup(13, GPIO.OUT)
        GPIO.add_event_detect(5, GPIO.RISING)
        GPIO.add_event_detect(22, GPIO.RISING)
        GPIO.add_event_callback(5, self.LeftCounterCallback)
        GPIO.add_event_callback(22, self.RightCounterCallback)
        self.left_channel = GPIO.PWM(18, 128)
        self.right_channel = GPIO.PWM(13, 128)
        self.left_channel.start(0)
        self.right_channel.start(0)
        self.calibration_enable = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('google.com', 0))
        host = s.getsockname()[0]
        server_address = (host, port_number)
        self.sock.bind(server_address)
        self.sock.listen(1)

    def __del__(self):
        self.calibration_enable = False
        GPIO.cleanup()
        #close socket
        self.sock.close()

    # Start to receive command
    def StartService(self):
        # Initialize Register configurationif(self.calibration_enable):
        while True:
            print('Wait for a connection')
            connection, client_address = self.sock.accept()
            self.TractionCalibrateCallback()
            try:
                while True:
                    data = connection.recv(32)
                    self.ProcessCommand(data)
            finally:
                # Clean up the connection
                print('Connection closed')
                self.Brake()
                print('Brake')
                self.calibration_enable = False
                print('Calibration callback stop')
                connection.close()
                print('connection close')

    def ProcessCommand(self, command):
        cmd = command.split(':')
        if len(cmd) != 3:
            # LOG error
            return
        if cmd[0] == 'P':
            pass
        elif cmd[0] == 'M':
            self.CalculateTraction(cmd[1], cmd[2])
            self.last_cmd_timestamp = time.time()
        else:
            #LOG error
            pass

    def CalculateTraction(self, magnitude, direction):
        dir = int(direction) / 127.0
        mag = int(magnitude) / 127.0
        ds = 0.5
        if dir < 0:
            ds = -0.5
        ms = 0.5
        if mag < 0:
            ms = -0.5
        if abs(dir) > abs(mag):
            dir = (abs(dir) * 2 - abs(mag)) * ds
            mag /= 2
        else:
            mag = (abs(mag) * 2 - abs(dir)) * ms
            dir /= 2
        self.left_pwm_ratio = mag + dir
        self.right_pwm_ratio = mag - dir

    def Brake(self):
        self.left_channel.ChangeDutyCycle(0)
        self.right_channel.ChangeDutyCycle(0)
        GPIO.output((6, 12, 15, 17), GPIO.LOW)

    def SetPWMsRegister(self):
        left = abs(self.left_pwm_ratio * self.left_offset)
        right = abs(self.right_pwm_ratio * self.right_offset)
        if left>1:
            right /=left
            left=1
        elif right>1:
            left /= right
            right=1
        print('pwm_ratio: %.4f %.4f'%(self.left_pwm_ratio, self.right_pwm_ratio))
        print('adjusted_pwm_ratio: %.4f %.4f'%(left, right))
        self.last_left_counter = self.left_counter
        self.last_right_counter = self.right_counter
        if left>80:
            left=80
        elif left<0:
            left=0
        if right>80:
            right=80
        elif right<0:
            right=0
        if (self.right_pwm_ratio > 0):
            GPIO.output(12, GPIO.HIGH)
            GPIO.output(6, GPIO.LOW)
            self.right_channel.ChangeDutyCycle(right * 80)
        else:
            GPIO.output(12, GPIO.LOW)
            GPIO.output(6, GPIO.HIGH)
            self.right_channel.ChangeDutyCycle(right * 80)
        if (self.left_pwm_ratio > 0):
            GPIO.output(17, GPIO.HIGH)
            GPIO.output(15, GPIO.LOW)
            self.left_channel.ChangeDutyCycle(left * 80)
        else:
            GPIO.output(17, GPIO.LOW)
            GPIO.output(15, GPIO.HIGH)
            self.left_channel.ChangeDutyCycle(left * 80)

    def LeftCounterCallback(self, channel):
        self.left_counter += 1

    def RightCounterCallback(self, channel):
        self.right_counter += 1

    def TractionCalibrateCallback(self):
        if (self.calibration_enable):
            threading.Timer(1.0 / self.calibration_freq,
                            self.TractionCalibrateCallback).start()
        if time.time() - self.last_cmd_timestamp > 0.2:
            self.left_pwm_ratio = 0
            self.right_pwm_ratio = 0
            self.Brake()
        elif self.left_pwm_ratio == 0 and self.right_pwm_ratio == 0:
            self.Brake()
        else:
            left = (self.left_counter - self.last_left_counter)
            right = (self.right_counter - self.last_right_counter)
            if left == 0 or right == 0 or self.last_right_pwm_ratio == 0 or self.last_left_pwm_ratio == 0:
                self.right_offset = 1
                self.left_offset = 1
            elif abs(self.last_left_pwm_ratio) >= abs(
                    self.last_right_pwm_ratio) and abs(self.left_pwm_ratio) >= abs(
                        self.right_pwm_ratio):
                self.right_offset *= abs(self.last_left_pwm_ratio / self.last_right_pwm_ratio * right / left)
                print('Offset: %f %f\n%d %d'%(self.left_offset, self.right_offset, left, right))
            elif abs(self.last_left_pwm_ratio) < abs(
                    self.last_right_pwm_ratio) and abs(self.left_pwm_ratio) < abs(
                        self.right_pwm_ratio):
                self.left_offset *= abs(self.last_right_pwm_ratio / self.last_left_pwm_ratio * left / right)
                print('Offset: %f %f\n%d %d'%(self.left_offset, self.right_offset, left, right))
            else:
                self.right_offset = 1
                self.left_offset = 1
            self.SetPWMsRegister()
        self.last_left_pwm_ratio = self.left_pwm_ratio
        self.last_right_pwm_ratio = self.right_pwm_ratio

#main
port = int(sys.argv[1])
vtcs = TractionControlSystem(4, port)
vtcs.StartService()
#end
