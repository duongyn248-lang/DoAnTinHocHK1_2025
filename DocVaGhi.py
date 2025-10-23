import csv

def ghi_csv(input_file, output_file):
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)        
        fieldnames = reader.fieldnames 

        with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()               
            for row in reader:
                writer.writerow(row)           

    print(f" Đã ghi toàn bộ dữ liệu từ '{input_file}' sang '{output_file}'.")


if __name__ == "__main__":
    input_file = 'healthcare-dataset-stroke-data.csv'  
    output_file = 'ghi_csv.csv'                          
    ghi_csv(input_file, output_file)
