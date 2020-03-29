#!/usr/bin/env python3
import requests
import base64
import hashlib
import sys
import binascii 
import argparse

user_agent = 'Threema/4.3A'
url = 'https://apip.threema.ch/identity/'

def header():
	return(str("-- Threema Public Key Dump Tool v1.0 --"))

def cli_options(args=sys.argv[1:]):
	p = argparse.ArgumentParser(description=header())
	p.add_argument("-id", "--threema_id", help="Enter 8 character Threema ID.", required=True)
	p.add_argument("-o", "--output", help="Set output file name to save raw public key to a file.", required=False)
	args = p.parse_args(args)
	return args

def retrieve_pubkey(threema_id):
	global base64_key
	response = requests.get(url + threema_id, headers={'User-Agent': user_agent})
	response.raise_for_status()
	jsonResponse = response.json()
	base64_key = jsonResponse["publicKey"]

def print_base64_key():
	print("Base64 key retrieved from API: " + base64_key)

def decode_key():
	global key_byte_array
	key_byte_array = base64.b64decode(base64_key)

def print_hex_key():
	print("Public key in hexadecimal Format: " + str(binascii.hexlify(key_byte_array)) + "\n")

def print_sha_key():
	global sha_string
	sha_value = hashlib.sha256(key_byte_array)
	sha_string = sha_value.hexdigest()
	print("SHA256 of public Key: " + sha_value.hexdigest())

def print_threema_fingerprint():
	print("Threema ID fingerprint: " + sha_string[:32] + "\n")

def save_public_key(file_name):
	file = open(file_name,"wb")
	file.write(key_byte_array)
	file.close()
	print("Public key saved as: \"" + file_name + "\"")


if __name__ == '__main__':
	args = cli_options()
	print("\n" + header() + "\n")
	if args.threema_id:
		retrieve_pubkey(args.threema_id)
		print_base64_key()
		decode_key()
		print_hex_key()
		print_sha_key()
		print_threema_fingerprint()
	if args.output:
		save_public_key(args.output)
