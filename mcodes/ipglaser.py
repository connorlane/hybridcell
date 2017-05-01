#!/usr/bin env python

import serial
import string
import time

class IPGLaser():
    def __init__(self, port):
	self.BAUD_RATE = 57600
	self.DATA_BITS = serial.EIGHTBITS
	self.STOP_BITS = serial.STOPBITS_ONE
	self.PARITY = serial.PARITY_NONE
	self.END_OF_COMMAND_CHARACTER = '\r'

        self.s = serial.Serial(port = port, baudrate = self.BAUD_RATE, parity = self.PARITY, stopbits = self.STOP_BITS, bytesize = self.DATA_BITS, timeout = 0.2)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.s.close()

    def _SendCommand(self, commandString, parameter=''):
        self.s.reset_input_buffer()
	toSend = commandString + ' ' + str(parameter) + self.END_OF_COMMAND_CHARACTER
	print toSend
        self.s.write(toSend)
    
        line = ""
        while True:
            c = self.s.read(1)
            if c:
                line += c
                if c == self.END_OF_COMMAND_CHARACTER:
                    break
            else:
                break

        return line.rstrip(self.END_OF_COMMAND_CHARACTER).upper()

    def SetAimingBeam(self, value):
        if value.upper() == "ON":
            response = self._SendCommand("ABN")
            if response != "ABN":
                return false
        elif value.upper() == "OFF":
            response = self._SendCommand("ABF")
            if response != "ABF":
                return false
        else:
            raise ValueError("Invalid argument")

        return True

    def SetDiodeCurrent(self, percent):
        assert(percent >= 0.0 and percent <= 100.0)

        command = "SDC"
        response = self._SendCommand(command, percent)
        responseSplit = response.split(':')
        if responseSplit[0] != command or responseSplit[1] != percent:
            return False
        return True

    def StartEmission(self):
        command = "EMON"
        response = self._SendCommand(command)
        if response != command:
            return False
        return True

    def StopEmission(self):
        command = "EMOFF"
        response = self._SendCommand(command)
        if response != command:
            return False
        return True

