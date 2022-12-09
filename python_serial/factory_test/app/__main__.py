from time import sleep
import serial
import serial.tools.list_ports
import PySimpleGUI as sg
import os
#import sys

# Setup serial
def serial_setup(COM, boundrate):
    global ser
    global Serial_Ready
    ser = None
    try:
        ser = serial.Serial(COM, boundrate, timeout=0.1)
        Serial_Ready = True
        return True
        
    except OSError:
        print("ERROR in configuring serial.")
        Serial_Ready = True
        return False

# Formatted serial reads
def fread_serial():
    global lines
    lines = []
    line = 0
    lines = ser.readlines()
    if lines != []:
        for line in range(0, len(lines) - 1): # SET loop from 1 to ignore the sent content
            if line == 0:
                print("[Sent_cmd]: " + "{}".format(lines[line].decode("utf-8", "replace").rstrip()))
            else:
                print("{}".format(lines[line].decode("utf-8", "replace").rstrip()))
        return True
    else:
        print("Device may not turn on.")
        return False

def execute_CMD(command):
    try:
        ser.readall() # A trick to clear serial buffer
        ser.write(f'{command}\n'.encode())
        if fread_serial() == True:
            for i in range(0, 150):  # longest wait for command to finish == 30s
                ser.write(f'\n'.encode())
                lines = ser.readlines()
                if b'~#' in lines[len(lines) - 1]:
                    break
                else:
                    sleep(0.2)
                    window.refresh()
        else:
            print("Serial reads nothing.")

    except serial.SerialTimeoutException:
        print("Error: serial write timeout!")
        pass

def main() -> None:

    # Globals
    ver = "1.5.2"
    bs = 115200
    port = ''
    Serial_Ready = True
    imagename = "swuimage" # file put to USB has to be named as this 
    com_file_path = os.path.join(os.getcwd(), "com.txt")
    cmdlist_file_path = os.path.join(os.getcwd(), "cmdlist.txt")

    # setup serial
    if os.path.exists(com_file_path):
        with open(com_file_path, 'r') as f:
                port = f.readline()
                f.close()
        if serial_setup(port, bs) == False:
            print("Error: change to proper COM port.")
            Serial_Ready = False
        else:
            Serial_Ready = True
            ser.readall()
            ser.write(b'root\n') #Send root to login as root
            s = ser.read(100)
            if b'root: not found' in s:
                print("Already logged in.")
            elif s == b'':
                print("Device is probably not on!")
                Serial_Ready = False
            else:
                print("Serial setup complete!")
    else:
        Serial_Ready = False
        pass

    # Window layout
    sg.theme('Light Blue 2')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  
                [sg.Text('Serial Port'), 
                sg.Combo([comport.device for comport in serial.tools.list_ports.comports()], default_value=port, size=(8, 1), enable_events=True, key='-COMBO-'), 
                sg.Button('OK', size=(6, 1)), sg.Button("Refresh", size=(6, 1))],

                [sg.Text("Commands", auto_size_text=True), sg.InputText(key='-CMD-', do_not_clear=False, size=(50, 1)), sg.Button('Send', bind_return_key=True, size=(6, 1))],
                [sg.Button('Enter u-boot', size=(12, 1)), sg.Button('Start Recovery', size=(12, 1)), sg.Button('Factory-Test', size=(12, 1))], 


                [sg.Text(text="STATUS", auto_size_text=True), sg.Text(key='-STA-', text="SUCCESS", justification="left", text_color='Green')],
                [sg.ProgressBar(100, orientation='h', size=(58, 10), key='-PROG-', expand_x=True)],
                [sg.Text("Log output")],
                [sg.Output(size=(80, 15), key='-OUT-', expand_x=True, expand_y=True)],
                [sg.Button('Exit', size=(6, 1)), sg.Button('Clear', size=(6, 1)), sg.Text("Version: " + ver, text_color="Black")]
            ]

    # Create the Window
    global window
    window = sg.Window('Factory-Test', layout, resizable=True, element_justification="center", finalize=True)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'): # if user closes window or clicks exit button
            break

        if event == 'OK':
            port = values['-COMBO-']
            with open(com_file_path, 'w') as f:
                f.write(port)
                f.close()
            print("Changed to port " + port + ", and saved")
            if serial_setup(port, bs) == True:
                print("Change port success.")
                Serial_Ready = True
            else:
                print("Port is not correct, try another one.")
                window['-STA-'].update(f"Error", text_color="Red")
                Serial_Ready = False
                continue
        
        if event == "Refresh":
            window['-COMBO-'].update(value='', values=[comport.device for comport in serial.tools.list_ports.comports()])

        if event == 'Send':
            if Serial_Ready == False:
                print("Check serial setup or power.")
                window['-STA-'].update(f"Error", text_color="Red")
                continue
            cmd = values['-CMD-']
            if cmd == '':
                print("Error, Can't send empty command.")
                window['-STA-'].update(f"Error", text_color="Red")
            else:
                window['-STA-'].update(f"Using commands", text_color="Black")
                ser.readall() # A trick to clear serial buffer
                ser.write(f'{cmd}\n'.encode())
                fread_serial()
        
        if event == 'Enter u-boot':
            if Serial_Ready == False:
                print("Check serial setup or power.")
                window['-STA-'].update(f"Error", text_color="Red")
                continue
            window['-STA-'].update(f"Entering u-boot", text_color="Black")
            print("Now trying to enter u-boot...")
            ser.write(f'uboot\r\n'.encode()) # Literally send anything to stop auto boot
            if fread_serial():
                if b'=>' in lines[len(lines) - 1]:
                    print("Now in uboot console.")
                    window['-STA-'].update(f"SUCCESS", text_color="Green")
                else:
                    print("Enter uboot failed.")
                    window['-STA-'].update(f"Error", text_color="Red")
                    continue

        if event == 'Start Recovery':
            if Serial_Ready == False:
                print("Check serial setup or power.")
                window['-STA-'].update(f"Error", text_color="Red")
                continue
            print("Now start recovery...")
            window['-PROG-'].update(15)
            ser.write("usb reset\n".encode()) # USB command
            window['-STA-'].update(f"Starting USB subsystem", text_color="Black")
            fread_serial()
            if b'Storage Device(s) found' not in lines[len(lines)-3]: # The last 3rd output telling the USB drive found
                print("Please insert USB drive and try again.")
                window['-STA-'].update(f"Error", text_color="Red")
                window['-PROG-'].update(0)
                continue
            window['-STA-'].update(f"Erasing existing partitions")
            ser.write("nand erase.part swufit\n".encode()) ################### 
            ser.write("nand erase.part fit\n".encode()) ## Erase partitions ##
            ser.write("nand erase.part data\n".encode()) #####################
            fread_serial()

            window['-STA-'].update(f"Loading file from USB")
            window['-PROG-'].update(50)
            # Loading file to ram
            ser.write("fatls usb 0:1\n".encode()) # List files from usb drive
            ser.write("fatload usb 0 $loadaddr ".encode() + imagename.encode() + '\n'.encode())
            fread_serial()
            window['-STA-'].update(f"Writing image to nand flash")
            window['-PROG-'].update(70)
            ser.write("nand write $loadaddr swufit $filesize\n".encode()) # Write to NAND flash
            fread_serial()
            window['-PROG-'].update(100)
            window['-STA-'].update(f"SUCCESS", text_color="Green")

        if event == 'Factory-Test':
            if Serial_Ready == False:
                print("Check serial setup or power.")
                window['-STA-'].update(f"Error", text_color="Red")
                continue
            print("Now start factory test...")
            window['-STA-'].update(f"Running test", text_color="Black")
            if os.path.exists(cmdlist_file_path):
                cmdlist = []
                count = 0 
                percent = 0
                step = 0
                try:
                    with open(cmdlist_file_path, 'r') as f:
                        cmdlist = f.readlines()
                        step = 100/len(cmdlist)
                    f.close()
                except ZeroDivisionError:
                    print("cmdlist.txt is empty, fill with commands first.")
                    window['-STA-'].update(f"Error", text_color="Red")
                    continue

                print('Command list:')   
                for cmd in cmdlist:
                    count += 1
                    percent += step
                    print(f'{count}: {cmd}'.rstrip())
                    execute_CMD(cmd)
                    window['-PROG-'].update(percent)    
                window['-STA-'].update(f"SUCCESS", text_color="Green")

            else:
                print("ERROR: command list is not available, will create file now but you need to fill with commands.")
                window['-STA-'].update(f"Error", text_color="Red")
                with open(cmdlist_file_path, 'w') as f:
                    f.close()
                continue

        if event == 'Clear':
            window['-OUT-'].update('') # Clear log window

    window.close()

if __name__ == "__main__":
    main()
