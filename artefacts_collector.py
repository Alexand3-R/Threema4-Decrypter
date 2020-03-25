#!/usr/bin/env python3
import os
import sys
import time
import argparse
import shutil
from threema_decrypter import \
read_key, bytes_to_hex, sqlcipher_format, decrypt_file, decrypt_database

def header():
	return(str("\n-- Threema 4 Artefacts Collector v1.0 --"))

def cli_options(args=sys.argv[1:]):
	p = argparse.ArgumentParser(description=header())
	p.add_argument("-d", "--userdata", help="Set path to Threema app folder. E.g. /mountpoint/data/ch.threema.app", required=True)
	p.add_argument("-s", "--sdcard", help="Set path to Threema app folder. E.g. /mountpoint/media/0/Android/data/ch.threema.app", required=True)
	args = p.parse_args(args)
	return args

def assign_file_locations(threema_data, threema_sd):
	# Set Global Variables
	global device_id, app_preferences, keyfile, database, file_dirs
	# Device ID File
	device_id = threema_data + "/files/device_id"
	# Threema Preferences Location
	app_preferences = threema_data + "/shared_prefs/ch.threema.app_preferences.xml"
	# Decryption Key Location
	keyfile = threema_data + "/files/key.dat"
	# Database File Location
	database = threema_data + "/databases/threema4.db"
	# Hidden Media Files
	all_media = threema_sd + "/files/data"
	avatars = threema_sd + "/files/data/.avatar"
	group_avatars = threema_sd + "/files/data/.grp-avatar"
	wallpapers = threema_sd + "/files/data/.wallpaper"
	blob = threema_sd + "/files/data/.blob"
	file_dirs = [all_media, avatars, group_avatars, wallpapers, blob]

def retrieve_hidden_media():
	print("\nRetrieving hidden media ...")
	count = 0
	for dir in file_dirs:
		file_list = os.listdir(dir)
		dir_name = dir.split("/")[-1]
		if dir_name.startswith("."):
			dir_name = dir_name[1:]
		os.makedirs("retrieved_files/media/" + dir_name) 
		for file in file_list:
			if os.path.isfile(dir + "/" + file):
				count = count + 1
				decrypt_file(keyfile, (dir + "/" + file))
				decrypted_name = file[1:] + ".decrypted"
				shutil.move(decrypted_name, "retrieved_files/media/" + dir_name)
	print ("Result: " + str(count) + " files.\n")
			
def retrieve_database():
	print("Retrieving database ...")
	decrypt_database(keyfile, database)
	time.sleep(1)
	shutil.move("decrypted.db","retrieved_files/")

def retrieve_settings_data():
	print("Retrieving Device ID and App Preferences ...")
	os.makedirs("retrieved_files/data")
	shutil.copyfile(device_id,"retrieved_files/data/device_id.txt")
	shutil.copyfile(app_preferences,"retrieved_files/data/app_preferences.txt")

if __name__ == '__main__':
	args = cli_options()
	if args.userdata and args.sdcard:
		print(header())
		assign_file_locations(args.userdata, args.sdcard)
		retrieve_hidden_media()
		retrieve_database()
		retrieve_settings_data()
		print ("\nTask completed!\n")
		
