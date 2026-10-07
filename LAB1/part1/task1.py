import math

n = 500
total = 0
sign = 1

for i in range(n):
    total += sign / (2 * i + 1)
    sign = -sign

pi_value = 4 * total

print("Количество членов ряда:", n)
print("Число Пи по формуле Грегори:", pi_value)
print("Значение math.pi:", math.pi)
print("Погрешность:", abs(math.pi - pi_value))
