import json

def the_status(number):
    if number % 2 == 0:
        return 'Taken'
    else:
        return 'Available'

def return_dic(numbers):
    return json.dumps({i:the_status(i) for i in numbers})

print(return_dic(list(range(1, 55))))
