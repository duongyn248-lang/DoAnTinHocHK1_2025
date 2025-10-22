import csv

def copy_csv(input_file, output_file):
    
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)  

        with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)

            for row in reader:
                writer.writerow(row)

    print(f" Đã sao chép toàn bộ dữ liệu từ '{input_file}' sang '{output_file}'.")


if __name__ == "__main__":
    input_file = 'healthcare-dataset-stroke-data.csv'  
    output_file = 'stroke_copy.csv'                      

    copy_csv(input_file, output_file)

