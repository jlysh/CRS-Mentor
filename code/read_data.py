import pandas as pd


def parse_aminer_paper(file_path):
    indices, titles, authors, affiliations, years, venues, references, abstracts = ([] for _ in range(8))

    index, title, author, affiliation, year, venue, reference, abstract = [None] * 8

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#index'):
                index = line[7:].strip()
            elif line.startswith('#*'):
                title = line[3:].strip()
            elif line.startswith('#@'):
                author = line[3:].strip()
            elif line.startswith('#o'):
                affiliation = line[3:].strip()
            elif line.startswith('#t'):
                year = line[3:].strip()
            elif line.startswith('#c'):
                venue = line[3:].strip()
            elif line.startswith('#%'):
                if reference is None:
                    reference = []
                reference.append(line[3:].strip())
            elif line.startswith('#!'):
                abstract = line[3:].strip()
            elif abstract == None or abstract == 'First Page of the Article': # 摘要为空不读取
                continue
            elif line.strip() == '':
                indices.append(index)
                titles.append(title)
                authors.append(author)
                affiliations.append(affiliation)
                years.append(year)
                venues.append(venue)
                references.append(';'.join(reference) if reference else '')
                abstracts.append(abstract)

                index, title, author, affiliation, year, venue, reference, abstract = [None] * 8

    data = {
        'Index': indices,
        'Title': titles,
        'Authors': authors,
        'Affiliations': affiliations,
        'Year': years,
        'Venue': venues,
        'References': references,
        'Abstract': abstracts
    }

    df = pd.DataFrame(data)
    return df

def read_csv(file_path):
    df = pd.read_csv(file_path)
    return df

# # 使用示例
# file_path = 'data/min_aminer.txt'
# df = parse_aminer_paper(file_path)
# df.to_csv('data/min_aminer_papers.csv', index=False)  # 保存为CSV文件
# # 查看数据集前5行
# print(df.head())




if __name__ == '__main__':
    file_path = 'data/min_aminer_papers.csv'
    df = read_csv(file_path)
    for i in df['Abstract']:
        print(i,'\n\n')