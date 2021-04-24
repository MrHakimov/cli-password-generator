## Примеры запуска:
* Генерация пароля из 8 символов с обязательным наличием символа в верхнем регистре:
```shell
python3 main.py --generate 8 8 --upper
```

* Получения отчета (разбивка паролей на соответствующие и несоответствующие) для паролей из файла `passwords.txt`. Критерий разбивки: если пароль состоит из 8-16 символов, содержит хотя бы одну заглавную букву, хотя бы один специальный символ и хотя бы одно число, то он будет считаться соответствующим.
```shell
python3 main.py --report passwords.txt 8 16 --upper --specials --digits
```

* Проверка корректности пароля по заданным критериям:
```shell
python3 main.py --check AlishEr 3 7 --upper
```

### Notes
* Примеры паролей содержатся в файле `passwords.txt`.
* Пароли обрабатываются пакетами из 1000 паролей за раз.
