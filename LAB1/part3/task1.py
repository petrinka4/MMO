class String:
    vowels = "аеёиоуыэюяaeiou"

    def __init__(self, text=""):
        self.text = str(text)

    def __str__(self):
        return self.text

    def __len__(self):
        return len(self.text)

    def __add__(self, other):
        return String(self.text + str(other))

    def reverse(self):
        return String(self.text[::-1])

    def count_words(self):
        return len(self.text.split())

    def count_vowels(self):
        return sum(1 for ch in self.text.lower() if ch in self.vowels)

    def is_palindrome(self):
        s = "".join(ch.lower() for ch in self.text if ch.isalnum())
        return len(s) > 0 and s == s[::-1]

    def capitalize_words(self):
        words = [word.capitalize() for word in self.text.split()]
        return String(" ".join(words))

    def remove_spaces(self):
        return String("".join(self.text.split()))

    def replace_word(self, old, new):
        return String(self.text.replace(old, new))

    def char_frequency(self):
        freq = {}
        for ch in self.text.lower():
            if ch.isalpha():
                freq[ch] = freq.get(ch, 0) + 1
        return freq

    def longest_word(self):
        words = self.text.split()
        if not words:
            return ""
        return max(words, key=len)


s = String(input("Введите строку: "))

print("Строка:", s)
print("Длина строки:", len(s))
print("Строка наоборот:", s.reverse())
print("Количество слов:", s.count_words())
print("Количество гласных:", s.count_vowels())
print("Является палиндромом:", s.is_palindrome())
print("Каждое слово с заглавной буквы:", s.capitalize_words())
print("Без пробелов:", s.remove_spaces())
print("Самое длинное слово:", s.longest_word())
print("Частота букв:", s.char_frequency())

old = input("Какое слово заменить: ")
new = input("На какое слово заменить: ")
print("После замены:", s.replace_word(old, new))
print("Сложение строк:", s + "!!!")

p = String("А роза упала на лапу Азора")
print()
print("Строка:", p)
print("Является палиндромом:", p.is_palindrome())
