from app import app, db
from app.models import Auto, Journal
from flask import render_template, request
from datetime import datetime
from os import listdir


@app.route('/index')
@app.route('/')
def index():
    # Получаем все записи из таблицы Auto
    auto_list = Auto.query.all()
    # Полученные наборы передаем в контекст
    context = {'auto_list': auto_list}
    return render_template('index.html', **context)



@app.route('/create_auto', methods=['POST', 'GET'])
def create_auto():
    context = None
    if request.method == 'POST':
        # Пришел запрос с методом POST (пользователь нажал на кнопку 'Добавить авто')
        # Получаем стоимость аренды в минуту - это значение поля input с атрибутом name="price"
        rent_price = request.form['price']
        # Запись числа будет считаться правильной и с точкой и с запятой (запятую заменяем точкой)
        k = rent_price.find(',')
        if k != -1:
            rent_price = rent_price[:k] + '.' + rent_price[k+1:]
        # Проверяем является ли значение поля "Стоимость" числом (случайный знак "-" не учитывается)
        # если не является, то возврат к форме добавления нового автомобиля
        try:
            rent_price = abs(float(rent_price))
        except:
            context = {'message': '- Стоимость аренды должна быть задана числом!'}
            return render_template('create_auto.html', **context)

        # Получаем имя файла картинки автомобиля - это значение поля input с атрибутом name="img_url"
        img_auto = request.form['img_url']
        # Проверяем есть ли данный файл среди доступных в папке auto
        # если нет, то возврат к форме добавления нового автомобиля
        if img_auto not in listdir('app/static/assets/images/auto'):
            context = {'message': '- Файл картинки должен быть из списка доступных!'}
            return render_template('create_auto.html', **context)

        # Получаем название автомобиля - это значение поля input с атрибутом name="name"
        name_auto = request.form['name']
        # Получаем описание автомобиля - это значение поля input с атрибутом name="description"
        description_auto = request.form['description']
        
        # Получаем тип корбки передач автомобиля - это значение поля input с атрибутом name="transmission"
        transmission_auto = request.form['transmission']
        # Добавляем автомобиль в базу данных Auto
        db.session.add(Auto(name=name_auto, price=rent_price, description=description_auto, transmission=transmission_auto, img_url=img_auto, dostup='Свободен'))
        # сохраняем изменения в базе
        db.session.commit()
        #Заполняем словарь контекста
        context = {
            'name_auto': name_auto,
            'auto_description': description_auto,
            'img_url': img_auto,
            'transmission': transmission_auto,
            'price': rent_price,
        }
        return render_template('add_auto.html', **context)
    elif request.method == 'GET':
        # Пришел запрос с методом GET - пользователь просто открыл в браузере страницу по адресу http://127.0.0.1:5000/create_auto
        # В этом случае ничего не делаем
        return render_template('create_auto.html')



@app.route('/correct_auto/<int:id_auto>', methods=['POST', 'GET'])
def correct_auto(id_auto):
    if request.method == 'POST':
        # Пришел запрос с методом POST (на странице auto_detail.html пользователь нажал на кнопку 'Изменить')
        # Получаем запись из таблицы Auto (по конкретному ID) для автомобиля, данные которого нужно изменить
        auto = Auto.query.get(id_auto)
        # Заполняем словарь контекста (для удобства эти данные будут подставлены в placeholder)
        context = {
            'id_auto': auto.id,
            'name_auto': auto.name,
            'price': auto.price,
            'in_rent_or_free': auto.dostup,
            'auto_transmission': auto.transmission,
            'auto_description': auto.description,
            'img_url': auto.img_url,
        }
    return render_template('correct_auto.html', **context)

   

@app.route('/auto_detail/<int:id_auto>', methods=['POST', 'GET'])
def auto_detail(id_auto):
    # Получаем из таблицы Auto запись по автомобилю (по конкретному ID)
    auto = Auto.query.get(id_auto)
    context = None
    if request.method == 'POST':
        # Пришел запрос с методом POST (на странице correct_auto.html пользователь нажал на кнопку 'Изменить')
        # Получаем и вносим в базу название автомобиля - это значение поля input с атрибутом name="name"
        auto.name = request.form['name']
        # Получаем и вносим в базу описание автомобиля - это значение поля input с атрибутом name="description"
        auto.description = request.form['description']
        # Получаем и вносим в базу тип корбки передач автомобиля - это значение поля input с атрибутом name="transmission"
        auto.transmission = request.form['transmission']
        # Получаем стоимость аренды в минуту - это значение поля input с атрибутом name="price"
        rent_price = request.form['price']
        k = rent_price.find(',')
        # Запись числа будет считаться правильной и с точкой и с запятой (запятую заменяем точкой)
        if k != -1:
            rent_price = rent_price[:k] + '.' + rent_price[k+1:]
        # Проверяем является ли значение поля "Стоимость" числом (случайный знак "-" не учитывается)
        try:
            rent_price = abs(float(rent_price))
            # Если значение поля "Стоимость" число, то вносим это изменение в базу данных
            auto.price = rent_price
        except:
            # если не является, то заполняем контекст и возвращаемся на форму корректировки данных автомобиля на страницу correct_auto.html
            context = {
                'id_auto': auto.id,
                'name_auto': auto.name,
                'in_rent_or_free': auto.dostup,
                'auto_transmission': auto.transmission,
                'auto_description': auto.description,
                'price': auto.price,
                'img_url': auto.img_url,
                'message': '- Стоимость аренды должна быть задана числом!'}
            return render_template('correct_auto.html', **context)
        # Проверяем, является ли значение поля input с атрибутом name="new_img_url" именем файла, находящегося в папке auto (картинки автомобилей)
        # если не является, то заполняем контекст и возвращаемся на форму корректировки данных автомобиля на страницу correct_auto.html
        if request.form['new_img_url'] not in listdir('app/static/assets/images/auto'):
            context = {
                'id_auto': auto.id,
                'name_auto': auto.name,
                'in_rent_or_free': auto.dostup,
                'auto_transmission': auto.transmission,
                'auto_description': auto.description,
                'price': auto.price,
                'img_url': auto.img_url,
                'message': '- Файл картинки должен быть из списка доступных!'
            }
            return render_template('correct_auto.html', **context)
        # Меняем в базе данных картинку данного автомобиля на новую
        auto.img_url = request.form['new_img_url']
        # сохраняем изменения в базе
        db.session.commit()
     
    # Связываем доступность автомобиля с соответствующим названием кнопки (Арендовать / Свободен)
    if auto.dostup == 'Свободен':
        button_name = 'Арендовать'
    else:
        button_name = 'Освободить' 
    # Получаем неизменяемую часть имени файла данного автомобиля (например, auto2_)
    img_url = auto.img_url[:6]
    # Получаем изменяемую часть имени файла данного автомобиля в виде целого числа
    k = int(auto.img_url[6])
    # Получаем все записи из таблицы Journal по данному автомобилю
    journal = Journal.query.filter_by(auto_info=id_auto).all()
    # Заполняем словарь контекста для отображения на странице auto_detail.html
    context = {
        'id_auto': auto.id,
        'name_auto': auto.name,
        'price': auto.price,
        'in_rent_or_free': auto.dostup,
        'yes_or_not': auto.transmission,
        'auto_description': auto.description,
        'img_url_1': auto.img_url,
        'img_url_2': img_url + str((k+1)//5 + (k+1)%5) + '.jpg',
        'img_url_3': img_url + str((k+2)//5 + (k+2)%5) + '.jpg',
        'img_url_4': img_url + str((k+3)//5 + (k+3)%5) + '.jpg',
        'button_name': button_name,
        'journal_list': journal
    }   
    return render_template('auto_detail.html', **context)



@app.route('/auto_rental/<int:id_auto>', methods=['POST', 'GET'])
def auto_rental(id_auto):
    # Получаем из таблицы Auto запись по автомобилю (по конкретному ID)
    auto = Auto.query.get(id_auto)
    # Получаем неизменяемую часть имени файла данного автомобиля (например, auto2_)
    img_url = auto.img_url[:6]
    # Получаем изменяемую часть имени файла данного автомобиля в виде целого числа
    k = int(auto.img_url[6])
    # В dt помещаем текущую дату и время
    dt = datetime.now()
    if request.method == 'POST':
        # Пришел запрос с методом POST (на странице auto_detail.html пользователь нажал на кнопку 'Арендовать / Освободить')
        # Получаем все записи из таблицы Journal по данному автомобилю (по конкретному ID)
        journal = Journal.query.filter_by(auto_info=id_auto).all()
        # Устанавливаем доступность автомобиля в соответствие с тем, на какую кнопку (Арендовать / Свободен) нажал пользователь
        if auto.dostup == 'Свободен':
            auto.dostup = 'Занят'
            button_name = 'Освободить'
            if not journal:
                # Если записей в журнале по данному автомобилю не было, то добавляем строку в таблицу Journal
                db.session.add(Journal(auto_info=id_auto, time_begin=dt, time_end=None, cost=0, quantity=1, time_total=0, cost_total=0))
            else:
                # Добавляем строку в таблицу Journal с учётом данных последней записи по данному автомобилю
                db.session.add(Journal(auto_info=id_auto, time_begin=dt, time_end=None, cost=0, quantity=journal[-1].quantity+1, time_total=journal[-1].time_total, cost_total=journal[-1].cost_total))
        else:
            # Меняем доступность автомобиля на "Свободен" и название кнопки на "Арендовать"
            auto.dostup = 'Свободен'
            button_name = 'Арендовать' 
            # В последнюю запись по данному автомобилю в таблице Journal вносим данные: время окончания аренды, общее время аренды, стоимость последней аренды и общая стоимость аренды 
            journal[-1].time_end = dt
            journal[-1].time_total +=(dt - journal[-1].time_begin).seconds //60
            journal[-1].cost = ((dt - journal[-1].time_begin).seconds //60) * auto.price
            if journal[-1].cost == 0:
                journal[-1].cost = auto.price
            journal[-1].cost_total +=journal[-1].cost
    # сохраняем изменения в базе
    db.session.commit()
    # Получаем все записи из таблицы Journal по данному автомобилю (по конкретному ID)
    journal = Journal.query.filter_by(auto_info=id_auto).all()
    # Заполняем словарь контекста для отображения на странице auto_detail.html
    context = {
        'id_auto': auto.id,
        'name_auto': auto.name,
        'price': auto.price,
        'in_rent_or_free': auto.dostup,
        'yes_or_not': auto.transmission,
        'auto_description': auto.description,
        'img_url_1': auto.img_url,
        'img_url_2': img_url + str((k+1)//5 + (k+1)%5) + '.jpg',
        'img_url_3': img_url + str((k+2)//5 + (k+2)%5) + '.jpg',
        'img_url_4': img_url + str((k+3)//5 + (k+3)%5) + '.jpg',
        'button_name': button_name,
        'journal_list': journal
    }   
    return render_template('auto_detail.html', **context)



@app.route('/del_auto/<int:id_auto>', methods=['POST', 'GET'])
def del_auto(id_auto):
    # Получаем из таблицы Auto запись по автомобилю (по конкретному ID)
    auto = Auto.query.get(id_auto)
    # Получаем все записи из таблицы Journal по данному автомобилю (по конкретному ID)
    journal = Journal.query.filter_by(auto_info=id_auto).all()
    context = {
        'name_auto': auto.name,
        'auto_description': auto.description,
        'img_url': auto.img_url,
        'transmission': auto.transmission,
        'price': auto.price,
    }
    # Удаляем все записи из таблиц Auto и Journal по данному автомобилю (по конкретному ID)
    for row in journal:
        db.session.delete(row)         
    db.session.delete(auto)
    # сохраняем изменения в базе
    db.session.commit()
    return render_template('delete_auto.html', **context)



@app.route('/rental_log')
def rental_log():
    # Создаём список журнала аренды
    journal_total = []
    # Получаем все записи из таблицы Auto
    auto_list = Auto.query.all()
    # По каждому автомобилю, который хотя бы один раз был арендован, добавляем в список журнала аренды последнюю запись из таблицы Journal
    for auto in auto_list:
        journal_auto = []
        if Journal.query.filter_by(auto_info=auto.id).first():
            journal_line = Journal.query.filter_by(auto_info=auto.id)[-1]
            journal_auto.append(auto.img_url)
            journal_auto.append(auto.name)
            journal_auto.append(journal_line.quantity)
            journal_auto.append(journal_line.time_total)
            journal_auto.append(journal_line.cost_total)
            journal_total.append(journal_auto)
    context = {'journal_total': journal_total}
    return render_template('rental_log.html', **context)



