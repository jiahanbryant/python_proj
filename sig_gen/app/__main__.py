import subprocess
import os

ID_file = "uniqueID.txt"
KEY_file = "verified-boot.key"
SIGNATURE_file = "signature.txt"
FILE_list = [ID_file, KEY_file]

def gen_sig(id):
    try:
        for file in FILE_list:
            if os.path.isfile(file):
                print(file + " file checked OK ...")
            else:
                print(file + " file doesn't exist, quitting...")
                exit()
        print("Processing with ID=" + id)
        command = subprocess.run('openssl dgst -sha256 -sign verified-boot.key uniqueId.txt | base64 -w0 > signature.txt', shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
        print(command.stdout)
        return True
    except:
        print("Error!")
        return False


def main() -> None:
    print("Welcome to signature generator.")
    while True:
        ID = input("Please input Unique ID here:\n").strip()
        if ID == "":
            print("Error, ID is empty!")
            continue
        else:
            with open(ID_file, 'w') as f:
                f.write(ID)
                f.close()
            while(gen_sig(ID)):
                print("Signature is successfully generated as below(also stored in signature.txt):\n")
                command = subprocess.run('cat signature.txt', shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
                print(command.stdout + "\n")
                exit()
            print("Failed generating signature.")
            break

if __name__ == "__main__":
    main()
    