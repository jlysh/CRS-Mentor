import csv
import random

# Input and output file names
input_file = './AMiner-Paper/AMiner-Paper.txt'
output_file = 'aminer_data.csv'
output_file_mini = 'aminer_data_mini.csv'
# Limit the number of records that can be saved
max_records = 13000

def extract_data(input_file, output_file):
    # Open the input file and output CSV file
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:

        # Create a CSV writer
        writer = csv.writer(outfile)
        # Write the header line
        writer.writerow(['Index', 'Title', 'Authors', 'Affiliations', 'Year', 'Venue', 'Abstract'])

        # Temporarily store the fields of the current record
        record = {}
        # Record counters
        record_count = 0

        # Read files line by line
        for line in infile:
            line = line.strip()

            # Determine the field based on the prefix of the row
            if line.startswith('#index'):
                if record and 'Abstract' in record:
                    writer.writerow([record.get('Index', ''), record.get('Title', ''), record.get('Authors', ''),
                                     record.get('Affiliations', ''), record.get('Year', ''), record.get('Venue', ''), record.get('Abstract', '')])
                    record_count += 1
                    if record_count % 1000 == 0:
                        print(f'{record_count} records have been written to {output_file}')
                record = {}
                record['Index'] = line.split()[-1]

            elif line.startswith('#*'):
                record['Title'] = ' '.join(line.split()[1:])

            elif line.startswith('#@'):
                record['Authors'] = ' '.join(line.split()[1:])

            elif line.startswith('#o'):
                record['Affiliations'] = ' '.join(line.split()[1:])

            elif line.startswith('#t'):
                record['Year'] = line.split()[-1]

            elif line.startswith('#c'):
                record['Venue'] = ' '.join(line.split()[1:])

            elif line.startswith('#!'):
                record['Abstract'] = ' '.join(line.split()[1:])

        # Write to the last record
        if record and 'Abstract' in record:
            writer.writerow([record.get('Index', ''), record.get('Title', ''), record.get('Authors', ''),
                             record.get('Affiliations', ''), record.get('Year', ''), record.get('Venue', ''), record.get('Abstract', '')])
            record_count += 1

    print(f'All records have been written to {output_file},total {record_count} records')

def extract_data_with_abstract(input_file, output_file_mini):
    # Randomly select max_records records with a summary from all records
    abstract_records = []
    print(f'Extracting {max_records} records with abstract...')
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            abstract_records.append(row)

    # Randomly select max_records records
    selected_records = random.sample(abstract_records, min(max_records, len(abstract_records)))

    # Write to a CSV file
    with open(output_file_mini, 'w', newline='', encoding='utf-8') as outfile:
        fieldnames = ['Index', 'Title', 'Authors', 'Affiliations', 'Year', 'Venue', 'Abstract']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for record_count,record in enumerate(selected_records):
            writer.writerow(record)
            if record_count % 1000 == 0:
                print(f'{record_count} records have been written to {output_file}')

    print(f'All records have been written to {output_file_mini},total {record_count} records')


# Call the function
extract_data(input_file, output_file)
extract_data_with_abstract(output_file, output_file_mini)
