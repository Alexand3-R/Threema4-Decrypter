#!/usr/bin/env python3
import subprocess
import binascii
import argparse
import sys
from Crypto.Cipher import AES

def header():
	return(str("-- Threema 4 Decryption Tool v1.0 --"))

def cli_options(args=sys.argv[1:]):
	p = argparse.ArgumentParser(description=header())
	p.add_argument("-k", "--keyfile", help="Decrypt AES cipher key files, such as key.dat.", required=True)
	p_mutex = p.add_mutually_exclusive_group(required=False)
	p_mutex.add_argument("-db", "--database", help="Decrypt SQLCipher encrypted databases. The decrypted database is stored as 'decrypted.db (requires sqlcipher v4 to be installed on Linux).'")
	p_mutex.add_argument("-f", "--datafile", help="Decrypt AES encrypted media files, such as MP4, JPEG, MP3. Uses the first 16 bytes as IV.")
	args = p.parse_args(args)
	return args

def read_key(key_file):
	#app_secret = [-107, 13, 38, 122, -120, -22, 119, 16, -100, 80, -25, 63, 71, -32, 105, 114, -38, -60, 57, 124, -103, -22, 126, 103, -81, -3, -35, 50, -38, 53, -9, 12]
	app_secret = bytearray.fromhex("950D267A88EA77109C50E73F47E06972DAC4397C99EA7E67AFFDDD32DA35F70C")
	#app_secret = bytearray.fromhex("7e604be4fb8ad789def2a28e558d4c963845703394c89956faf70d88a68ed200")
	localDataInputStream = open(key_file,"rb").read(33)
	f = bytearray(32)
	f = bytearray(localDataInputStream[1:33])
	k = 0
	# xor decoding loop
	while k < 32:
		arrayOfByte = f
		arrayOfByte[k] = (arrayOfByte[k] ^ app_secret[k])
		k += 1
	return(arrayOfByte)

def bytes_to_hex(key_file):
	key_string = str(binascii.hexlify(read_key(key_file))).replace("b","",1).replace("'","",2)
	return key_string

def sqlcipher_format(hex_key):
	formatted = "x\"" + bytes_to_hex(hex_key) + "\""
	return formatted

def decrypt_file(key_file, data):
	key = read_key(key_file)
	data_array = bytearray(open(data,"rb").read())
	iv = data_array[:16]
	cipher = AES.new(key, AES.MODE_CBC, iv)
	name = data.split("/")[-1]
	f = open(name[1:] + ".decrypted", "wb")
	f.write(cipher.decrypt(data_array[16:]))

def decrypt_database(key_file, database_name):
	hex_key_string = bytes_to_hex(key_file)
	sqlcipher_cmd = ("echo \""
					"PRAGMA cipher_default_kdf_iter = 1;"
					"PRAGMA key='x\\\"" + hex_key_string + "\\\"'; "
					"PRAGMA kdf_iter = 1;"
					"PRAGMA cipher_memory_security = OFF;"
					"select count(*) from sqlite_master;"
					"ATTACH DATABASE 'decrypted.db' AS plaintext KEY '';"
					"SELECT sqlcipher_export('plaintext');"
					"DETACH DATABASE plaintext;\""
					"| sqlcipher " + database_name)
	ps = subprocess.Popen(sqlcipher_cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

if __name__ == '__main__':
	args = cli_options()
	print("\n" + header() + "\n")
	if args.keyfile and not args.database and not args.datafile:
		print("Decryption Key: \n" + bytes_to_hex(args.keyfile))
		print("Decryption Key (formatted for sqlcipher): \n" + sqlcipher_format(args.keyfile))
	if args.database:
		print("Decrypting \'" + args.database + "\'\nwith decryption key: " + sqlcipher_format(args.keyfile))
		decrypt_database(args.keyfile, args.database)
	if args.datafile:
		print("Decrypting " + args.datafile + "\nwith decryption key: " + bytes_to_hex(args.keyfile))
		decrypt_file(args.keyfile, args.datafile)
	print ("\nTask completed!\n")



