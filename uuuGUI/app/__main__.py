import subprocess
import os, sys
import platform
import PySimpleGUI as sg
import time
import shutil
import serial.tools.list_ports

# command list
checkForUsb = "check_usb_device"
loadImage = "boot_image"
# From StackOverFlow, mainly for Windows
# https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile
def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    global base_path
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Setup serial
def serial_setup(COM, boundrate):
    global ser
    ser = None
    try:
        ser = serial.Serial(COM, boundrate, timeout=0.1)
        return True
        
    except OSError:
        print("ERROR in configuring serial.")
        return False
    except AttributeError:
        print("ERROR in selecting COM port, try another one.")
        return False

def cmdCheck(cmd):
    uuu_WIN = resource_path(r"tools\win\uuu.exe")
    uuu_MAC = resource_path("tools/mac/uuu")
    uuu_LINUX = resource_path("tools/linux/uuu")
    autoScript_WIN = resource_path(r"tools\images\uuu.auto")
    autoScript_Linux_Mac = resource_path("tools/images/uuu.auto")

    try:
        if running_OS == "Windows":
            # To hide windows console poping
            # https://stackoverflow.com/questions/1765078/how-to-avoid-console-window-with-pyw-file-containing-os-system-call
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            if cmd == "check_usb_device":
                print("Checking for USB devices...")
                command = subprocess.run([uuu_WIN, "-lsusb"], stdout=subprocess.PIPE, universal_newlines=True, startupinfo=startupinfo)
            elif cmd == "boot_image":
                print("loading images...")
                command = subprocess.run([uuu_WIN, autoScript_WIN], stdout=subprocess.PIPE, universal_newlines=True, startupinfo=startupinfo)
            print(command.stdout)
            os.chdir(base_path)
            return command.stdout
        elif running_OS == "macOS" or running_OS=="Darwin":
            if cmd == "check_usb_device":
                print("Checking for USB devices...")
                command = subprocess.run([uuu_MAC, "-lsusb"], stdout=subprocess.PIPE, universal_newlines=True)
            elif cmd == "boot_image":
                print("loading images...")
                command = subprocess.run(["sudo", uuu_LINUX, autoScript_Linux_Mac], stdout=subprocess.PIPE, universal_newlines=True)
            return command.stdout
        elif running_OS == "Linux":
            if cmd == "check_usb_device":
                print("Checking for USB devices...")
                command = subprocess.run([uuu_LINUX, "-lsusb"], stdout=subprocess.PIPE, universal_newlines=True)
            elif cmd == "boot_image":
                print("loading images...")
                command = subprocess.run(["sudo", uuu_LINUX, autoScript_Linux_Mac], stdout=subprocess.PIPE, universal_newlines=True)
            return command.stdout
        else:
            print("Error: Not supported OS")
            return False
        
    except subprocess.SubprocessError:
        print("Error in running uuu tool.")
        return False

def replaceFile(FilePath):
    try:
        if running_OS == "Windows":
            shutil.copy2(FilePath + "/imx-boot.bin", resource_path(r"tools\images"))
            shutil.copy2(FilePath + "/fitImage", resource_path(r"tools\images"))
            print("Done replacing files.")
            return
        elif running_OS == "macOS" or running_OS=="Darwin" or running_OS == "Linux":
            shutil.copy2(FilePath + "/imx-boot.bin", resource_path("tools/images"))
            shutil.copy2(FilePath + "/fitImage", resource_path("tools/images"))
            print("Done replacing files.")
            return
        else:
            print("Not supported OS.")
            return False

    except FileNotFoundError:
        print("Warning: using internal files.")
        window['-IMAGEPATH-'].update(f"Using internal files", text_color="Brown")
        window.Refresh()
        return

# To extract device info from output of usb_check
# currently only support one usb device at a time
def retrieveDEVICE(): 
    suportList = ["MX8MM", "MX8MN"]
    usbDevice = cmdCheck(checkForUsb)
    if usbDevice != "False":
        for device in suportList:
            if device in usbDevice:
                print(device + " is found.")
                window['-DEVICE-'].update(f"Device Connected", text_color="Green")
                return True
            
            else:
                print("Error: no usb device found.")
                window['-DEVICE-'].update(f"Device Not Connected", text_color="Red")
                return False

# To load u-boot and fit to ram of soc via USB
def recover():
    try:
        cmdCheck(loadImage)
        if serial_setup(COM, 115200):
            while True:
                boot_timeout = time.time() + 60

                y = ser.readline()
                print("{}".format(y.decode("utf-8", "replace").rstrip()))

                if b'test=>' in y:
                    print('\nboot [OK]')
                    ser.write("flash boot".encode() + b'\n')
                    pass
                elif b'flash boot [OK]' in y:
                    print("now verifying...")
                    ser.write("verify".encode() + b'\n')
                    pass
                elif b'verify [OK]' in y:
                    print("Recovery Done successfully.")
                    global recovery
                    recovery = True
                    return
                elif time.time() > boot_timeout:
                    print("Error: boot timeout")
                    recovery = False
                    return
        else:
            print("check serial configuraton.")
            recovery = False
            return
    except:
        print("Error: failed to boot image.")

def main() -> None:

    # Window Layout
    layout = [  [sg.Text('Device'), sg.Text('Device Not Connected', key='-DEVICE-', text_color='Red', size=(46,1)), sg.Button('Check', size=(6,1))],
                [sg.Input(sg.user_settings_get_entry('-filename-', ''), key='-IMAGEPATH-', size=(60,1)), sg.FolderBrowse('Browse', size=(6,1))],
                [sg.Text('Select Serial'), sg.Combo([comport.device for comport in serial.tools.list_ports.comports()], default_value="Select Com Port", size=(10, 1), key='-COM-')],
                [sg.Button('Recover')],
                [sg.Output(size=(80,20), key='-OUTPUT-', expand_x=True, expand_y=True)],
                [sg.Exit()]
    ]

    # Create the Window
    global window
    version = open(resource_path("version"), 'r+').read()
    window = sg.Window(f'Stream1955 Recovery Tool (ver. {version})', layout, icon="icon/48x48.ico", resizable=True, element_justification='centre', finalize=True)
    print("Use of instruction:\n1, Connect USB from PC to Device, check for device;\n2, [Opt.]Select files for loading;\n3, Select serial port;\n4, Press recover.")

    global running_OS
    global COM
    running_OS = platform.system()  

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == "Check":
            retrieveDEVICE()
        elif event == "Recover":
            if not retrieveDEVICE():
                print("Connect device first!")
                continue
            if values['-COM-'] != "Select Com Port":
                COM = values['-COM-']
                print("Using " + COM)

                global FilePath
                FilePath = values['-IMAGEPATH-']
                print(f"Will copy files under path: {FilePath} over to internal")
                replaceFile(FilePath)
                window.perform_long_operation(recover, '-RECOVER DONE-')
            else:
                print("Please select correct com port.")

        elif event == '-RECOVER DONE-' and recovery:
            print("Recovery [OK].")
            # Not in USB mode after recovery
            window['-DEVICE-'].update(f"Device Not Connected", text_color="Red")

if __name__ == "__main__":
    main()

