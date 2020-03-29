# Threema4-Decrypter
This is a tool for decrypting Threema 4 databases and files, written in Python 3. It **only works if the Master Key passphrase has not been set**.

It was developed for a digital forensics university research project and is inspired by a tool  developed by [@wilzbach](https://github.com/wilzbach/threema-decrypt), which was written for an earlier version of Threema. 

An automated artifacts collection tool that utilizes the decryption tool has been added, together with a test kit containing Threema files and folders of the Android 'userdata' and 'sdcard' partitions. A script to dump the public key of a user using Threema's server has also been made available.

## Requirements
Python 3 (≥ 3.5)

SQLite 2 or higher (≥ 2.8)

SQLCipher 4 (≥ 4.0)

## Setup
```pip3 install pycryptodome```

## Usage
```
threema_decrypter.py [-h] -k KEYFILE [-db DATABASE | -f DATAFILE]
artefacts_collector.py [-h] -d USERDATA -s SDCARD
threema_public_key_dumper.py [-h] -id THREEMA_ID [-o OUTPUT]
```
### Examples
```
alex@PC:~/Desktop/CCF/Test-Kit$ python3 threema_decrypter.py -k key.dat -db threema4.db
alex@PC:~/Desktop/CCF/Test-Kit$ python3 artefacts-collector.py  -d data/ch.threema.app -s media/0/Android/data/ch.threema.app
alex@PC:~/Desktop/CCF/Test-Kit$ python3 threema_public_key_dumper.py -id EDB5TMPB -o pubkey
```

## Authors
Alexander-OS3

Hoang-OS3

## TO-DO
Implement support for passing the Master Key passphrase to the decryption script.
