text = ' An apple a day keeps the doctor away'

counts = {}
for ch in text:
    counts[ch] = counts.get(ch, 0) + 1

print("Строка:", repr(text))
print("Словарь:")
print(counts)
print()
for key, value in counts.items():
    print(f"'{key}' - {value}")
