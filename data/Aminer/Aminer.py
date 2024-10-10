import csv
import logging

# Input and output file names
input_file = './AMiner-Paper/AMiner-Paper.txt'
output_file = 'aminer_data.csv'
output_file_mini = 'aminer_data_mini.csv'
# Limit the size of the output file
MAX_FILE_SIZE_MB = 15


# Clean the source dataset
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
                                     record.get('Affiliations', ''), record.get('Year', ''), record.get('Venue', ''),
                                     record.get('Abstract', '')])
                    record_count += 1
                    if record_count % 1000 == 0:
                        logging.info(f'{record_count} records have been written to {output_file}')
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

        # Write the last record
        if record and 'Abstract' in record:
            writer.writerow([record.get('Index', ''), record.get('Title', ''), record.get('Authors', ''),
                             record.get('Affiliations', ''), record.get('Year', ''), record.get('Venue', ''),
                             record.get('Abstract', '')])
            record_count += 1
            if record_count % 1000 == 0:
                logging.info(f'{record_count} records have been written to {output_file}')
            if outfile.tell() > 1024 * 1024 * MAX_FILE_SIZE_MB:
                logging.info(f"File size limit reached at {record_count} records.")

    logging.info(f'All records have been written to {output_file}, total {record_count} records')


# The dataset is cleaned twice to extract the condensed data
def extract_data_with_abstract(input_file, output_file_mini):
    # Extract records with abstract
    abstract_records = []
    logging.info(f'Extracting records with abstract...')
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            if 'Abstract' in row and row['Abstract'] != 'First Page of the Article':
                abstract_records.append(row)

    # Write to a CSV file
    with open(output_file_mini, 'w', newline='', encoding='utf-8') as outfile:
        fieldnames = ['Index', 'Title', 'Authors', 'Affiliations', 'Year', 'Venue', 'Abstract']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        record_count = 0

        for record in abstract_records:
            writer.writerow(record)
            record_count += 1
            if record_count % 1000 == 0:
                logging.info(f'{record_count} records have been written to {output_file_mini}')
            if outfile.tell() > 1024 * 1024 * MAX_FILE_SIZE_MB:
                logging.info(f"File size limit reached at {record_count} records.")
                break

    logging.info(f'All records have been written to {output_file_mini}, total {record_count} records')


# Call the function
# extract_data(input_file, output_file)
extract_data_with_abstract(output_file, output_file_mini)
