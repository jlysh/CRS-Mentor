import csv
import json
import logging
import os
import re

import ijson

# Constants
YEAR_THRESHOLD = 2015  # Year threshold for filtering data
MAX_FILE_SIZE_MB = 14  # Maximum file size in MB
MIN_WORDS_IN_TITLE = 7  # Minimum number of words in the title

'''
Filter out data before {YEAR_THRESHOLD} - 1, keep only data from {YEAR_THRESHOLD} onwards
Filter out records with titles containing numbers
Filter out titles with non-printable characters
Filter out records with titles containing fewer than {MIN_WORDS_IN_TITLE} words
Filter out records without a year
Filter out records without an abstract
Keep approximately {MAX_FILE_SIZE_MB}MB of data
'''


# Read a chunk of source data and fix JSON issues
def readChunk(path, out_path, chunk_size=1024 * 1024 * 100):
    # Calculate total file size
    file_size = os.path.getsize(path)
    total_chunks = max(1, file_size // chunk_size)

    chunk_count = 0
    with open(path, 'r', encoding='utf-8') as fp:
        while True:
            # Read the data of a chunk
            chunk = fp.read(chunk_size)
            if not chunk:
                break

            # Replace the NumberInt format
            pattern = re.compile(r"NumberInt\((\d+)\)")
            fixed_chunk = re.sub(pattern, r'\1', chunk)

            with open(out_path, 'a', encoding='utf-8') as fo:
                fo.write(fixed_chunk)

            chunk_count += 1

            # Print a progress log
            if total_chunks > 1 and chunk_count % (total_chunks // 10) == 0:
                logging.info(f"Processed {chunk_count / total_chunks * 100:.2f}% of the JSON file")

    return chunk_count


def is_valid(record):
    # Check if the title contains only digits
    if record['title'].isdigit():
        return False

    # Filter out titles with fewer than {MIN_WORDS_IN_TITLE} words
    if len(record['title'].split()) <= MIN_WORDS_IN_TITLE:
        return False

    # Filter out titles, authors, and abstracts with non-printable characters
    if not record['title'].isprintable() or not ','.join(
            [author.get('name', '') for author in record['authors']]).isprintable() or not record[
        'abstract'].isprintable():
        return False
    return True

def extract_and_save_to_csv(file_path, output_csv_path):
    fieldnames = ['Id', 'Title', 'Authors', 'Year', 'Abstract']
    current_records = 0

    # Open CSV file for writing
    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  # Write header

        # Use ijson to parse JSON file item by item
        with open(file_path, 'r', encoding='utf-8') as file:
            # Use ijson's `items` method to parse JSON file item by item
            objects = ijson.items(file, 'item')
            try:
                for record in objects:
                    current_records += 1
                    try:
                        # Check if all fields are not empty or empty strings/lists
                        if not (record.get('abstract') and
                                record.get('authors') and
                                record.get('year') and
                                record.get('title') and
                                record.get('id')):
                            continue

                        # Check if authors is an empty list
                        if not record['authors']:
                            continue

                        # Check if the title is valid
                        if not is_valid(record):
                            continue

                        # Check if the year is after {YEAR_THRESHOLD}
                        if int(record['year']) < YEAR_THRESHOLD:
                            continue

                        # Extract required fields
                        extracted_record = {
                            'Id': record.get('id'),
                            'Title': record.get('title'),
                            'Authors': ','.join([author.get('name', '') for author in record['authors']]),
                            'Year': record.get('year'),
                            'Abstract': record.get('abstract')
                        }

                        # Write to CSV file
                        writer.writerow(extracted_record)

                        # Stop when approximately {MAX_FILE_SIZE_MB}MB of data has been collected
                        if csvfile.tell() > 1024 * 1024 * MAX_FILE_SIZE_MB:
                            break

                        # Print a progress log
                        if current_records % 1000 == 0:
                            logging.info(f"Data that has been written to {current_records}".format(
                                current_records=current_records))
                    except Exception as e:
                        logging.error(f"Error processing record: {e}")
                        continue
            except ijson.common.IncompleteJSONError as e:
                logging.error(f"Incomplete JSON error: {e}")
            except json.JSONDecodeError as e:
                logging.error(f"JSON decode error: {e}")
            except Exception as e:
                logging.error(f"Unexpected error: {e}")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Process the source data and save it as a JSON intermediate file
source_file_path = './DBLP-Paper/dblp_v14.json'
file_path = './DBLP-Paper/dblp_v14.json.json'
logging.info("Processing readChunk method...")
readChunk(source_file_path, file_path, chunk_size=1024 * 1024 * 100)

# Process the extracted data and save it as a final CSV file
dblp_csv_path = './DBLP-Paper/dbpl_data_mini.csv'
logging.info("Processing extract_and_save_to_csv method...")
extract_and_save_to_csv(file_path, dblp_csv_path)
logging.info("Data exported to CSV file.")
