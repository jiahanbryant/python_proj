import subprocess
import os
import datetime
import platform

ID_file = "uniqueID.txt"
KEY_file = "verified-boot.key"
SIGNATURE_file = "signature.txt"
LOG_dir = "log"
LOGfile_pre = "/test_log_"
FILE_list = [ID_file, KEY_file]

def logging(message):
    print(message)

    if not os.path.isdir(LOG_dir):
        try:
            os.mkdir(LOG_dir)
        except FileExistsError:
            print("Folder exists already.")
            pass

    with open(log_file, 'a+') as f:
        f.write(message + '\n')
        f.close

def gen_sig(id):
    try:
        for file in FILE_list:
            if os.path.isfile(file):
                logging(file + " file checked OK ...")
            else:
                logging(file + " file doesn't exist, quitting...")
                exit()
        logging("Processing with ID=" + "\"" + id + "\"")
        command = subprocess.run('openssl dgst -sha256 -sign verified-boot.key uniqueId.txt | base64 -w0 > signature.txt', shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
        logging(command.stdout)
        return True
    except:
        logging("Error!")
        return False


def main() -> None:
    global date
    global log_file
    global my_os
    my_os = platform.system()

    while True:
        date  = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        log_file = LOG_dir + LOGfile_pre + date
        logging("Welcome, dear " + my_os + " user, " + "please input your Unique ID here:")
        ID = input().strip()

        if ID == "":
            logging("Error, ID is empty!")
            continue
        else:
            with open(ID_file, 'w') as f:
                f.write(ID)
                f.close()
            while(gen_sig(ID)):
                logging("Signature is successfully generated as below(also stored in signature.txt):\n")
                if my_os == "Windows":
                    command = subprocess.run('type signature.txt', shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
                else:
                    command = subprocess.run('cat signature.txt', shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
                logging(command.stdout + "\n")
                exit()
            logging("Failed generating signature.")
            break

if __name__ == "__main__":
    main()
    