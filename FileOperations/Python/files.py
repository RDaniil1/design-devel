import win32api
import shutil

import os
from pathlib import Path
from pprint import pprint

import json

from bs4 import BeautifulSoup

from zipfile import ZipFile
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def get_filesystem_info():
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    
    for drive in drives:
        disk_info = shutil.disk_usage(drive)
            
        volume_info = win32api.GetVolumeInformation(drive)
 
        print(f'Drive name: {drive}', \
            f'Volume label: {volume_info[0]}', \
            f'Volume type: {volume_info[4]}', \
            f'Disk usage: {disk_info.used}', \
            f'Free: {disk_info.free}', \
            f'Total: {disk_info.total}', sep='\n')
        print()
        
def opertate_files():
    string = input('Type string for file input: ')
    file_path = Path(__file__).parent  / 'file.txt'
    with open(file_path, 'w') as file:
        file.writelines([string])
    
    file_content = []
    with open(file_path) as file:
        file_content = file.readlines()
    pprint(file_content)
    
    os.remove(file_path)
    
def operate_json():
    amount = int(input('Type amount of keys/values: '))
    keys = input('Type keys: ').split()
    values = input('Type values: ').split()
    
    if len(keys) != amount or len(values) != amount:
        print('Incorrect amount of keys/values')
        return
    
    data = dict(zip(keys, values))
    data = json.dumps(data)

    json_path = Path(__file__).parent / 'file.json'
    with open(json_path, 'w') as json_file:
        json_file.write(data)
    
    with open(json_path) as json_file:
        data = json_file.read()

    print(data)

def operate_xml():
    xml_filename = 'file.xml'
    xml_path = Path(__file__).parent / xml_filename
    if not xml_path.exists():
        print(f'File {xml_filename} not exists')
        return
    
    data = ''
    with open(xml_path) as xml_file:
        data = xml_file.read()
    
    bs_data = BeautifulSoup(data, 'xml')
    
    tag = bs_data.find('to')
    tag['atr'] = 'info'
    
    print(bs_data)
    
    with open(xml_path, 'w') as xml_file:
        xml_file.write(bs_data.prettify())

    os.remove(xml_path)
    
def operate_zip():
    Tk().withdraw()
    filename = askopenfilename()
    
    zip_filename = 'files.zip'
    zip_curr_direct = Path(__file__).parent
    zip_full_path = zip_curr_direct / zip_filename 
    with ZipFile(zip_full_path, 'w') as zip_file:
        zip_file.write(filename)
        
    with ZipFile(zip_full_path) as zip_file:
        zip_file.extractall(zip_curr_direct)
        
    os.remove(zip_full_path)
    os.remove(filename)
    
if __name__ == '__main__':
    get_filesystem_info()
    opertate_files()
    operate_json()
    operate_xml()
    operate_zip()

