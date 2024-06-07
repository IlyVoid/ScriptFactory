from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import os
import random
import sys
from termcolor import colored
from tqdm import tqdm

# Encrypt function with progress bar
def encrypt(key, filename):
    chunksize = 64 * 1024
    outFile = os.path.join(os.path.dirname(filename), "(encrypted)" + os.path.basename(filename))
    fileSize = os.path.getsize(filename)
    IV = b''

    for _ in range(16):
        IV += bytes([random.randint(0, 0xFF)])

    encryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(filename, "rb") as infile:
        with open(outFile, "wb") as outfile:
            outfile.write(str(fileSize).encode().zfill(16))
            outfile.write(IV)
            with tqdm(total=fileSize, unit='B', unit_scale=True, desc='Encrypting') as pbar:
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break

                    elif len(chunk) % 16 != 0:
                        chunk += b' ' * (16 - (len(chunk) % 16))

                    outfile.write(encryptor.encrypt(chunk))
                    pbar.update(len(chunk))

# Decrypt function with progress bar
def decrypt(key, filename):
    encrypted_prefix = "(encrypted)"
    outFile = os.path.join(os.path.dirname(filename), os.path.basename(filename[len(encrypted_prefix):]))
    chunksize = 64 * 1024
    with open(filename, "rb") as infile:
        fileSize = int(infile.read(16))
        IV = infile.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(outFile, "wb") as outfile:
            with tqdm(total=fileSize, unit='B', unit_scale=True, desc='Decrypting') as pbar:
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break

                    outfile.write(decryptor.decrypt(chunk))
                    pbar.update(len(chunk))

            outfile.truncate(fileSize)

def allfiles():
    allFiles = []
    for root, subfiles, files in os.walk(os.getcwd()):
        for names in files:
            allFiles.append(os.path.join(root, names))

    return allFiles

def print_error(message):
    print(colored("Error: " + message, "red"))

def print_success(message):
    print(colored(message, "green"))

def print_warning(message):
    print(colored("Warning: " + message, "yellow"))

choice = input(colored("Do you want to (E)ncrypt or (D)ecrypt? ", "blue"))
password = input(colored("Enter the passphrase: ", "blue"))

encFiles = allfiles()

if choice == "E":
    for Tfiles in encFiles:
        if os.path.basename(Tfiles).startswith("(encrypted)"):
            print_warning("%s is already encrypted" % str(Tfiles))
            continue

        elif Tfiles == os.path.join(os.getcwd(), sys.argv[0]):
            continue
        else:
            encrypt(SHA256.new(password.encode()).digest(), Tfiles)
            print_success("Done encrypting %s" % str(Tfiles))
            os.remove(Tfiles)

elif choice == "D":
    filename = input(colored("Enter the filename to decrypt: ", "blue"))
    if not os.path.exists(filename):
        print_error("This file does not exist")
        sys.exit(0)
    elif not filename.startswith("(encrypted)"):
        print_error("%s is not encrypted" % filename)
        sys.exit()
    else:
        decrypt(SHA256.new(password.encode()).digest(), filename)
        print_success("Successfully decrypted %s" % filename)
        os.remove(filename)

else:
    print_error("Please choose a valid option.")
    sys.exit()

