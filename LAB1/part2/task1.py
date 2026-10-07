def is_prime(n):
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("аргумент должен быть целым числом")
    if n < 0 or n > 1000:
        raise ValueError("число должно быть в диапазоне от 0 до 1000")
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def read_number(text):
    try:
        return int(text)
    except ValueError:
        raise ValueError("нужно ввести целое число")


def main():
    primes = [x for x in range(101) if is_prime(x)]
    print("Простые числа от 0 до 100:", primes)
    print()
    while True:
        s = input("Введите число от 0 до 1000 (q - выход): ").strip()
        if s.lower() == "q":
            print("Выход из программы")
            break
        try:
            num = read_number(s)
            result = is_prime(num)
            print(f"is_prime({num}) = {result}")
        except (ValueError, TypeError) as e:
            print("Ошибка:", e)
        finally:
            print("-" * 40)


main()
