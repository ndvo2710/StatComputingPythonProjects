import os
import re
import sys
import math

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

longitude_list = list(df.longitude.unique())
for i in range(len(longitude_list)):
    if 'W' in longitude_list[i]:
        longitude_list[i] = float(longitude_list[i].split('W')[0])

latitude_list = list(df.latitude.unique())
for i in range(len(latitude_list)):
    print(latitude_list[i])
    if 'N' in latitude_list[i]:
        N_lat = latitude_list[i].split('N')[0]
        N_lat = N_lat.replace(" ", "")
        N_lat = float(N_lat)
        print(f"N_lat is {N_lat} with type is {type(N_lat)}")
        latitude_list[i] = N_lat
    elif 'S' in latitude_list[i]:
        print(latitude_list[i].split('S')[0])
        latitude_list[i] = float(latitude_list[i].split('S')[0].replace(" ", ""))

latitude_list


def closest_number(numbers, target):
    smallest_difference = float(sys.maxsize)
    smallest_d_index = 0
    for i in range(len(numbers)):
        difference = abs(numbers[i] - float(target))
        if difference < smallest_difference:
            smallest_difference = difference
            smallest_d_index = i
    return numbers[smallest_d_index]


# Import elevation.dat data intp elevation_df
elevation_dir = os.path.join(NASA_DIR, "elevation.dat")
list_of_elevation_dicts = []
with open(elevation_dir, 'r') as elev_f:
    elev_long = elev_f.readline()
    elev_long
    elev_long = [float(elem) for elem in elev_long.replace("\n", "").replace("-", "").split(" ")]
    while True:
        row_e = elev_f.readline()
        if row_e == "":
            break
        row_e = row_e.replace("\n", "").replace("-", "").split(" ")
        row_e = [float(elem) for elem in row_e]
        lat = row_e[0]
        row_lat_data = row_e[1:]
        for i in range(len(elev_long)):
            elev_dict = {}
            elev_dict["lat"] = lat
            elev_dict["long"] = elev_long[i]
            elev_dict["elevation"] = row_lat_data[i]
            list_of_elevation_dicts.append(elev_dict)
list_of_elevation_dicts
elevation_df = pd.DataFrame(list_of_elevation_dicts)
elevation_df

# Update df by using elevation_df
def generate_elevation_for_df(row):
    global elevation_df
    if 'N' in row['latitude']:
        df_row_lat = row['latitude'].split('N')[0]
        df_row_lat = df_row_lat.replace(" ", "")
        df_row_lat = float(df_row_lat)
    elif 'S' in row['latitude']:
        df_row_lat = row['latitude'].split('S')[0]
        df_row_lat = df_row_lat.replace(" ", "")
        df_row_lat = float(df_row_lat)

    if 'W' in row['longitude']:
        df_row_long = row['longitude'].split('W')[0]
        df_row_long = df_row_long.replace(" ", "")
        df_row_long = float(df_row_long)

    lat_match = closest_number(elevation_df.lat, df_row_lat)
    long_match = closest_number(elevation_df.long, df_row_long)
    match_elev_df_obj = elevation_df.loc[(elevation_df.lat == lat_match) & (elevation_df.long == long_match), ['elevation']]
    return float(match_elev_df_obj.values[0][0])


df.apply(generate_elevation_for_df, axis=1)
df

