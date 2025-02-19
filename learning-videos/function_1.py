def calculate_statistics(numbers, operation='mean'):
    if not numbers:
        return "Error: The list is empty"
    
    if operation == 'mean':
        return sum(numbers) / len(numbers)
    
    elif operation == 'median':
        sorted_numbers = sorted(numbers)
        n = len(sorted_numbers)
        midpoint = n // 2
        if n % 2 == 0:
            return (sorted_numbers[midpoint - 1] + sorted_numbers[midpoint]) / 2
        else:
            return sorted_numbers[midpoint]
    elif operation == 'mode':
        frequency = {}
        for number in numbers:
            frequency[number] = frequency.get(number, 0) + 1
        most_frequency = max(frequency.values())
        modes = [k for k, v in frequency.items() if v == most_frequency]
        return modes
    else:
        return "Error: Unsupported operation"
        
data = [1, 1, 8, 1, 5, 3, 5]

print("Mean:" , calculate_statistics(data))
print("Median:" , calculate_statistics(data, operation='median'))
print("Mode:" , calculate_statistics(data, operation='mode'))
