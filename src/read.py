
def is_csv_file(file_path):
    return file_path.endswith('.csv')

def read_csv_file(file_path):
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                row = line.strip().split(',')
                data.append(row)
        return data
    except Exception as e:
        print(f"Error: {e}")
        return None
