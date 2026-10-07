line = input("Введите целые числа через пробел: ")
numbers = tuple(int(x) for x in line.split())

print("Кортеж:", numbers)

evens = [x for x in numbers if x % 2 == 0]

if not numbers:
    print("Кортеж пустой")
elif evens:
    print("Наименьший четный элемент:", min(evens))
else:
    print("Четных элементов нет, первый элемент:", numbers[0])
