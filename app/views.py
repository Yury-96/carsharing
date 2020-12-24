from app import app, db
from app.models import Auto, Journal
from flask import render_template, request
from datetime import datetime
import os


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
        k = rent_price.find(',')
        if k != -1:
            rent_price = rent_price[:k] + '.' + rent_price[k+1:]
        try:
            rent_price = abs(float(rent_price))
        except:
            context = {'message': '- Стоимость аренды должна быть задана числом!'}
            return render_template('create_auto.html', **context)

        # Получаем имя файла картинки автомобиля - это значение поля input с атрибутом name="img_url"
        img_auto = request.form['img_url']
        # Проверяем есть ли данный файл среди доступных в папке auto
        if img_auto not in os.listdir('app/static/assets/images/auto'):
            context = {'message': '- Файл картинки должен быть из списка доступных!'}
            return render_template('create_auto.html', **context)

        # Получаем название товара - это значение поля input с атрибутом name="name"
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
        auto = Auto.query.get(id_auto)
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
    auto = Auto.query.get(id_auto)
    context = None
    if request.method == 'POST':
        
        auto.description = request.form['description']
        auto.transmission = request.form['transmission']
        auto.name = request.form['name']
        
        rent_price = request.form['price']
        k = rent_price.find(',')
        if k != -1:
            rent_price = rent_price[:k] + '.' + rent_price[k+1:]
        try:
            rent_price = abs(float(rent_price))
            auto.price = rent_price
        except:
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

        if request.form['new_img_url'] not in os.listdir('app/static/assets/images/auto'):
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
        auto.img_url = request.form['new_img_url']
        
        db.session.commit()
     
    if auto.dostup == 'Свободен':
        button_name = 'Арендовать'
    else:
        button_name = 'Освободить' 
    img_url = auto.img_url[:6]
    k = int(auto.img_url[6])
    journal = Journal.query.filter_by(auto_info=id_auto).all()
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
    auto = Auto.query.get(id_auto)
    img_url = auto.img_url[:6]
    k = int(auto.img_url[6])
    dt = datetime.now()
    if request.method == 'POST':
        journal = Journal.query.filter_by(auto_info=id_auto).all()
        if auto.dostup == 'Свободен':
            auto.dostup = 'Занят'
            button_name = 'Освободить'
            if not journal:
                db.session.add(Journal(auto_info=id_auto, time_begin=dt, time_end=None, cost=0, quantity=1, time_total=0, cost_total=0))
            else:
                db.session.add(Journal(auto_info=id_auto, time_begin=dt, time_end=None, cost=0, quantity=journal[-1].quantity+1, time_total=journal[-1].time_total, cost_total=journal[-1].cost_total))
        else:
            auto.dostup = 'Свободен'
            button_name = 'Арендовать' 
            journal[-1].time_end = dt
            journal[-1].time_total +=(dt - journal[-1].time_begin).seconds //60
            journal[-1].cost = ((dt - journal[-1].time_begin).seconds //60) * auto.price
            if journal[-1].cost == 0:
                journal[-1].cost = auto.price
            journal[-1].cost_total +=journal[-1].cost
    db.session.commit()
    journal = Journal.query.filter_by(auto_info=id_auto).all()
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
    auto = Auto.query.get(id_auto)
    journal = Journal.query.filter_by(auto_info=id_auto).all()
    context = {
        'name_auto': auto.name,
        'auto_description': auto.description,
        'img_url': auto.img_url,
        'transmission': auto.transmission,
        'price': auto.price,
    }
    for row in journal:
        db.session.delete(row)         
    db.session.delete(auto)
    db.session.commit()
    return render_template('delete_auto.html', **context)



@app.route('/rental_log')
def rental_log():
    journal_total = []
    auto_list = Auto.query.all()
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



