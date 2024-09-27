import csv

# 输入和输出文件名
input_file = './data/AMiner-Paper/AMiner-Paper.txt'
output_file = 'aminer_data.csv'
max_records = 14000  # 限制保存的记录数

# 打开输入文件和输出CSV文件
with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:

    # 创建CSV写入器
    writer = csv.writer(outfile)
    # 写入标题行
    writer.writerow(['Index', 'Title', 'Authors', 'Affiliations', 'Year', 'Venue', 'Abstract'])

    # 临时存储当前记录的字段
    record = {}
    record_count = 0  # 记录计数器

    # 逐行读取文件
    for line in infile:
        line = line.strip()

        # 根据行的前缀判断字段
        if line.startswith('#index'):
            # if record_count >= max_records:  # 检查是否达到最大记录数
            #     break  # 如果达到，则跳出循环

            if record:  # 如果已有记录，则写入前一个记录
                if 'Abstract' in record:  # 只有当记录包含摘要时才写入
                    writer.writerow([record.get('Index', ''), record.get('Title', ''), record.get('Authors', ''),
                                     record.get('Affiliations', ''), record.get('Year', ''), record.get('Venue', ''), record.get('Abstract', '')])
                    record_count += 1  # 增加记录计数
                else:
                    continue
            record = {}  # 重置记录

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

    # 写入最后一个记录（如果有，并且未达到最大记录数）
    if record and record_count < max_records:
        writer.writerow([record.get('Index', ''), record.get('Title', ''), record.get('Authors', ''),
                         record.get('Affiliations', ''), record.get('Year', ''), record.get('Venue', ''), record.get('Abstract', '')])
        record_count += 1

print(f'{record_count} records have been written to {output_file}')



