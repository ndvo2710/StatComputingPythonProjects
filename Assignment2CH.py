import os
import re

CWD = os.getcwd()
NASA_DIR = os.path.join(CWD, 'NASA')

list_of_NASA_files = os.listdir(NASA_DIR)

for nasa_files in list_of_NASA_files:
    if not nasa_files.endswith(".dat"):
        nasa_files_dir = os.path.join(NASA_DIR, nasa_files)
        with open(nasa_files_dir, 'r') as ff:
            for _ in range(4):
                next(ff)

            data_time = ff.readline()
            data_time = data_time.replace('\n', '').replace("00:00", "").split(":")[1].strip()

            fifth_line = ff.readline()
            sixth_line = ff.readline()
            fifth_line, sixth_line = re.sub('\n', '', fifth_line, sixth_line).split(' ')


