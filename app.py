number_of_seats = 79
available = [3, 5, 8]

for seat in range(number_of_seats):
    if seat not in available:
        taken = []
        taken.append(seat)
        print(taken)