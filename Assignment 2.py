import os
import re


CWD = os.getcwd()
NASA_DIR = os.path.join(CWD, "NASA")

list_of_NASA_files = os.listdir(NASA_DIR)

list_of_combine_dict = []

for nasa_file in list_of_NASA_files:
    if not nasa_file.endswith(".dat"):
        print(f"Working file is {nasa_file}")

        file_type = re.sub("\d+.txt", "", nasa_file)



        nasa_file_path = os.path.join(NASA_DIR, nasa_file)
        with open(nasa_file_path, 'r') as ff:
            # Skip the first four lines
            for _ in range(4):
                next(ff)

            # Get date and time of data
            date_time = ff.readline()
            print(f"\tdate_time value is {date_time}")
            date_time = date_time.replace("\n", "").replace("00:00", "").split(":")[1].strip()
            print(f"\tdate_time value is {date_time}")


            # Create a dictionary to store data
            """
            key: column_name__indice_name
                Example: 113.8W_27__36.2W_51
            value: cell value rst equivalent column and indice(row)
            """
            fifth_line = ff.readline()
            sixth_line = ff.readline()
            fifth_line = re.sub('\n', '', fifth_line).split(' ')
            sixth_line = re.sub('\n', '', sixth_line).split(' ')
            while "" in fifth_line:
                fifth_line.remove("")
            while "" in sixth_line:
                sixth_line.remove("")
            # print(f"Fifth line : {fifth_line}\n"
            #       f"Sixth line : {sixth_line}")
            longitudes = []
            for elem in zip(fifth_line, sixth_line):
                longitudes.append(f"{elem[0]}_{elem[1]}")
            print(longitudes)


            while True:
                row = ff.readline()
                if row == "":
                    break
                latitude, row_data = row.replace("\n", "").split(":")
                latitude = latitude.replace("/", "_").replace(" ", "")
                row_data = row_data.split(" ")
                while "" in row_data:
                    row_data.remove("")

                for i in range(len(longitudes)):
                    nasa_file_dict = {}
                    nasa_file_dict["Type"] = file_type
                    nasa_file_dict["DateTime"] = date_time
                    nasa_file_dict["longitude"] = longitudes[i]
                    nasa_file_dict["latitude"] = latitude
                    try:
                        value = float(row_data[i])
                    except ValueError:
                        print(f"Error in row_data[i] is {row_data[i]}")
                        value = None
                    nasa_file_dict["Value"] = value

                    list_of_combine_dict.append(nasa_file_dict)

list_of_combine_dict
import pandas as pd
df = pd.DataFrame(list_of_combine_dict)
df





