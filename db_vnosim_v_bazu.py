# import os
# # определение текущей рабочей директории
# path = os.getcwd()
# # чтение записей
# with os.scandir('app/static/assets/images/auto') as listOfEntries:  
#     for entry in listOfEntries:
#         # печать всех записей, являющихся файлами
#         if entry.is_file():
#             print(entry.name)


# print(os.listdir('app/static/assets/images/auto'))
# if 'auto6_0.jpg'  not in os.listdir('app/static/assets/images/auto'):
#     print(' HE Входит в список')




#from datetime import datetime
# from app import db
# from app.models import Auto
#dt = datetime.now()
#print(f"Дата: {dt.day}.{dt.month}.{dt.year}    Время: {dt.hour}:{dt.minute}:{dt.second}")
# # # создаем экземпляр класса User
# new_auto = Auto(name='УАЗ Патриот', price=10, description='Внедорожник 4Х4', transmission='Механическая', img_url='auto5_1.jpg', dostup='Свободен')
#y = int(dt)
#print(y)
# # # добавляем изменения в базу данных (при этом база не сохраняется)
# db.session.add(new_auto)

# # # сохраняем изменения в базе
# db.session.commit()

x = input('Задайте число = ')
#x.strip()
k = x.find(',')
if k != -1:
    x = x[:k]+'.'+x[k+1:]
try:
    x = abs(float(x))
    print(x,  ' - это действительно число!')
except:
    print(x, '- это не число!')



