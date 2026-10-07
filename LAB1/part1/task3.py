data = [1, 34, 'qwerty', 12, 13, 16, 'Love', 'Python']

words = []
numbers = []

for item in data:
    if isinstance(item, str):
        words.append(item)
    else:
        numbers.append(item)

total = sum(numbers)
product = 1
for num in numbers:
    product *= num

top3 = sorted(numbers, reverse=True)[:3]

print("Исходный список:", data)
print("Список слов:", words)
print("Список чисел:", numbers)
print("Сумма элементов:", total)
print("Произведение элементов:", product)
print("Три наибольших элемента:", top3)
