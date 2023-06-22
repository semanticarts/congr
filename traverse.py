import os

def traverse_directory(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        print(f'Found directory: {dirpath}')
        for file_name in filenames:
            print(f'File: {os.path.join(dirpath, file_name)}')

traverse_directory('C:\\Users\\StevenChalem\\congr-test')  