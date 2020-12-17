from app import db
from app.models import Auto


# # создаем экземпляр класса User
new_auto = Auto(name='УАЗ Патриот', price=10, description='Внедорожник 4Х4', transmission='Механическая', img_url='auto5_1.jpg', dostup='Свободен')

# # добавляем изменения в базу данных (при этом база не сохраняется)
db.session.add(new_auto)

# # сохраняем изменения в базе
db.session.commit()

# auto_list = Auto.query.all()
# print(auto_list[0].name)
# print(auto_list[1].price)
