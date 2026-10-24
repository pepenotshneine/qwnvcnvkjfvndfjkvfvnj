import sqlite3
# Підключаємо вбудованого помічника для роботи з базою даних (щоб зберігати наші посилання)
import requests
# Підключаємо помічника, який вміє відправляти запити в інтернет і завантажувати сайтиПідключаємо помічника, який вміє відправляти запити в інтернет і завантажувати сайти
from bs4 import BeautifulSoup

db = sqlite3.connect("db.db")
db.execute("CREATE TABLE IF NOT EXISTS p (u TEXT)")

while True:
    c = input("\n1-Пошук 2-Додати 3-Список 4-Очистити 0-Вихід: ")
    # Цей рядок запускає нескінченний цикл, який постійно показує меню на екрані та чекає, поки ви введете потрібну цифру для вибору дії.

    if c == "0":
        break
    elif c == "1":
        w = input("Слово: ").lower()
        res = []
        for (u,) in db.execute("SELECT u FROM p"):
            try:
                txt = BeautifulSoup(requests.get(u, timeout=2).text, "html.parser").get_text().lower()
                n = txt.count(w)
                if n > 0: res.append((u, n))
# Цей код створює просту програму з меню, яка зберігає посилання на сайти в базі даних, шукає в них потрібне слово та виводить результати у списку від найрелевантніших
            except:
                pass  #якщо сайт зламався або не відкривається, програма пропускає його і не вимикається через помилку
        res.sort(key=lambda x: x[1], reverse=True)   # сортує знайдені сайти так, щоб нагорі опинилися ті, де ваше слово зустрічається найчастіше
    elif c == "2":
        db.execute("INSERT INTO p VALUES (?)", (input("URL: "),))
        db.commit()
    elif c == "3":
        for (u,) in db.execute("SELECT u FROM p"): print(u) # виводить на екран кожен знайдений сайт разом із кількістю згадок на ньому
    elif c == "4":
        db.execute("DELETE FROM p")
        db.commit()
        print("Очищено!")