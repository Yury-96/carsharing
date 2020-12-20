from datetime import datetime
# from app import db
# from app.models import Auto
dt = datetime.now()
print(f"Дата: {dt.day}.{dt.month}.{dt.year}    Время: {dt.hour}:{dt.minute}:{dt.second}")
# # # создаем экземпляр класса User
# new_auto = Auto(name='УАЗ Патриот', price=10, description='Внедорожник 4Х4', transmission='Механическая', img_url='auto5_1.jpg', dostup='Свободен')
y = int(dt)
print(y)
# # # добавляем изменения в базу данных (при этом база не сохраняется)
# db.session.add(new_auto)

# # # сохраняем изменения в базе
# db.session.commit()


