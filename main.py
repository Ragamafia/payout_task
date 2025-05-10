file_path = '/home/ragamafia/PycharmProjects/payout_task/data/data1.csv'

with open(file_path, 'r') as file:
    header = file.readline().strip().split(',')

    for line in file:
        values = line.strip().split(',')
        data = dict(zip(header, values))
        print(data)



        # print(f"id: {data['id']}, email: {data['email']}, name: {data['name']}, "
        #       f"department: {data['department']}, hours_worked: {data['hours_worked']}, "
        #       f"rate: {data['hourly_rate'] or data['rate'] or data['salary']}")