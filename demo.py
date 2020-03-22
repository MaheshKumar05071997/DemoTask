import datetime
from zipfile import ZipFile

import namegenerator
import os
import pandas as pd
import wget


class DemoTask():

    # function that returns weekdays date.
    def weekdays_date(self):
        today_date = datetime.datetime.today()
        for x in range(6):
            all = today_date - datetime.timedelta(days=x)
            if all.weekday() < 5:
                desired = all.date().day
                # print(desired)
        return desired

    # returns path where file is to be saved
    def save_path(self):
        x_save_path = (os.path.normpath(os.getcwd() + os.sep + os.pardir))
        y_save_path = (os.path.normpath(x_save_path + os.sep + os.pardir))
        os.chdir(y_save_path)
        # os.chdir('NSE_Downloads')
        current_save_path = os.getcwd()
        print('in save_path:', current_save_path)
        return current_save_path

    # function to dynamically change the file names and download it from NSE website
    def rename_files_for_download(self):
        original = "https://archives.nseindia.com/content/historical/EQUITIES/2020/FEB/cm27FEB2020bhav.csv.zip"

        print(f"Original file is: {original}")
        a = (self.weekdays_date())
        self.save_path()
        try:
            os.mkdir('NSE_Downloads')  # makes a separate folder "NSE_Downloads" and saves the downloaded files
        except FileExistsError:
            print('File exists already')
        os.chdir('NSE_Downloads')
        current = os.getcwd()
        # print(a)
        predefined = ["FEB", "MAR"]  # I'm defining the months only to download for Feb & March
        for i in range(a):
            for x in predefined:
                # print(i+1)
                modified_file = f"https://archives.nseindia.com/content/historical/EQUITIES/2020/{x}/cm{str(i).zfill(2)}{x}2020bhav.csv.zip"
                print(
                    f"Modified file {i + 1} is: {modified_file}")  # New file generated dynamically based on original file pattern
                try:
                    wget.download(modified_file, current)
                except ConnectionResetError:
                    print('Error Handled!')
                except TimeoutError:
                    print("Oops this was a weekend, we don't have file for this date")
            # time.sleep(4)
        for i in os.listdir(current):  # Unzip the downloaded files
            with ZipFile(i, 'r') as zip:
                zip.printdir()
                print('Extracting files now..')
                zip.extractall('temp')
                print('Done!')
        print("Finished in rename_files_for_download")
        print('Path after extraction:', os.getcwd())
        uff = os.chdir('temp')
        print('Temp Directory ?', uff)
        temp_dir = os.getcwd()
        print(temp_dir)
        col_list = 'SYMBOL', 'SERIES', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'LAST', 'PREVCLOSE', 'TOTTRDQTY', 'TOTTRDVAL', 'TIMESTAMP'
        for i in os.listdir(temp_dir):  # Parses the unzipped files and saves the files in .CSV format
            print("Currently opening: ", i, "file")
            a = (pd.read_csv(i, usecols=col_list))
            df = pd.DataFrame(a)
            print('Saving file:')
            df.to_csv(namegenerator.gen() + '.csv')
            # print(i)
        print("Files Parsed Successfully")


if __name__ == "__main__":
    dt = DemoTask()
    dt.rename_files_for_download()
    print("Main finished!")
