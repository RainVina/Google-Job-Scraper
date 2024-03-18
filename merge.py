import os
import csv

main_folder = "C:/Users/Ran/Downloads/Scraper for Google Jobs/raw_data"

output_csv = "combined_data.csv"

def merge_csvs_in_subfolders(main_folder, output_csv):
    with open(output_csv, "w", newline="", encoding="utf-8") as output_file:
        csv_writer = csv.writer(output_file)

        header_written = False

        for root, dirs, files in os.walk(main_folder):
            for file in files:
                if file.endswith(".csv"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", newline="", encoding="utf-8") as input_file:
                        csv_reader = csv.reader(input_file)
                        header = next(csv_reader)

                        if not header_written:
                            csv_writer.writerow(header)
                            header_written = True

                        for row in csv_reader:
                            csv_writer.writerow(row)

merge_csvs_in_subfolders(main_folder, output_csv)
