import os
import subprocess
import configparser

class CsvImporter:
    def __init__(self, config_path):
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

    def import_csv_files(self):
        db_user = self.config.get('Database', 'db_user')
        db_pass = self.config.get('Database', 'db_pass')
        db_name = self.config.get('Database', 'db_name')
        table_name = self.config.get('Database', 'table_name')

        folder_path = self.config.get('CSV', 'folder_path')
        mysql_path = self.config.get('CSV', 'mysql_path')

        # List all CSV files in the folder
        csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

        for csv_file in csv_files:
            full_path = os.path.join(folder_path, csv_file)
            print(f"Importing {full_path} into the database...")

            # Construct the MySQL command
            mysql_command = [
                mysql_path,
                '-u', db_user,
                '-p' + db_pass,
                '-e', f"LOAD DATA LOCAL INFILE '{full_path.replace('\\', '\\\\')}' INTO TABLE {db_name}.{table_name} FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\\n' IGNORE 1 LINES (CITY, STREET, BON_BUN, BU_BUN, DAN_GI_MYEONG, SQUARE_METER, CONTRACT_DATE, CONTRACT_DAY, AMOUNT, LAYER, CONSTRUCTION_DATE, ROAD_NAME, REASON_CANCELLATION_DATE, REGISTRATION_CREATION, TRANSACTION_TYPE, LOCATION_AGENCY);"
            ]

            # Execute the MySQL command using subprocess
            subprocess.run(mysql_command, shell=True)

        print("All files imported.")

if __name__ == "__main__":
    config_path = 'config.ini'
    csv_importer = CsvImporter(config_path)
    csv_importer.import_csv_files()
