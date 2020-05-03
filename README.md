# PythonProject

# 1.1. Шифрование
```./encryptor.py encode --cipher {caesar|vigenere|vernammod|vernam} --key {<number>|<word>} [--input-file input.txt] [--output-file output.txt] --language {rus|eng|vern}```
  
# 1.2. Дешифрование
```./encryptor.py decode --cipher {caesar|vigenere|vernammod|vernam} --key {<number>|<word>} [--input-file input.txt] [--output-file output.txt] --language {rus|eng|vern}```
  
# 1.3. Построение модели
```./encryptor.py train --text-file {input.txt} --model-file {model} --language {rus|eng}```
  
# 1.4. Взлом
```./encryptor.py hack [--input-file input.txt] [--output-file output.txt] --model-file {model} --language {rus|eng}```
