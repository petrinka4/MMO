vowels = "аеёиоуыэюяaeiou"
not_letters = "ъь"

text = input("Введите текст: ")

vowel_count = 0
consonant_count = 0
vowel_list = []

for ch in text:
    low = ch.lower()
    if not ch.isalpha() or low in not_letters:
        continue
    if low in vowels:
        vowel_count += 1
        vowel_list.append(ch)
    else:
        consonant_count += 1

print("Количество гласных:", vowel_count)
print("Количество согласных:", consonant_count)

if vowel_count == consonant_count:
    print("Количество гласных и согласных совпадает")
    print("Гласные буквы в тексте:", " ".join(vowel_list))
