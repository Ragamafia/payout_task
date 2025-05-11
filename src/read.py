
def is_csv_file(file):
    return file.endswith('.csv')

def read_csv_file(csv_file):
    data = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        for line in file:
            row = line.strip().split(',')
            data.append(row)

        return data

