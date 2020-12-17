from app import app, db
from app.models import Auto#, Journal
from flask import render_template, request
from datetime import datetime


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
        # Получаем название товара - это значение поля input с атрибутом name="name"
        name_auto = request.form['name']

        # Получаем стоимость аренды в минуту - это значение поля input с атрибутом name="price"
        rent_price = request.form['price']

        # Получаем описание автомобиля - это значение поля input с атрибутом name="description"
        description_auto = request.form['description']

        # Получаем описание автомобиля - это значение поля input с атрибутом name="img_url"
        img_auto = request.form['img_url']

        # Получаем тип корбки передач автомобиля - это значение поля input с атрибутом name="transmission"
        transmission_auto = request.form['transmission']

        # Добавляем автомобиль в базу данных Auto
        db.session.add(Auto(name=name_auto, price=rent_price, description=description_auto, transmission=transmission_auto, img_url=img_auto, dostup='Свободен'))

        # сохраняем изменения в базе
        db.session.commit()

        #Заполняем словарь контекста
        context = {
            #'method': 'POST',
            'name': name_auto,
            # 'price': rent_price,
            # 'description': description_auto,
            # 'transmission': transmission_auto,
            'img_url':img_auto
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
    #journal = Journal.query.get(auto_info.auto.id)

    context = None

    if request.method == 'POST':

        new_name = request.form['name']
        new_price = request.form['price']
        new_description = request.form['description']
        new_transmission = request.form['transmission']
        #dostup = request.form['in_rent_or_free']
        new_img_url = request.form['new_img_url']

        if new_name:
            auto.name = request.form['name']
        
        if new_price:
            auto.price = request.form['price']

        if new_description:
            auto.description = request.form['description']

        if new_transmission:
            auto.transmission = request.form['transmission'] 

        if new_img_url:
            auto.img_url = request.form['new_img_url']

        if request.form['in_rent_or_free']:
            auto.dostup = request.form['in_rent_or_free']
            
        db.session.commit()

     
    if auto.dostup == 'Свободен':
        button_name = 'Арендовать'
    else:
        button_name = 'Освободить' 
    
    img_url = auto.img_url[:6]
    k = int(auto.img_url[6])
   
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
    }   
       
    return render_template('auto_detail.html', **context)

@app.route('/auto_rental/<int:id_auto>', methods=['POST', 'GET'])
def auto_rental(id_auto):

    auto = Auto.query.get(id_auto)
    #journal = Journal.query.get(auto_info.auto.id)
    img_url = auto.img_url[:6]
    k = int(auto.img_url[6])

    context = None

    if request.method == 'POST':
        
        if auto.dostup == 'Свободен':
            auto.dostup = 'Занят'
            button_name = 'Освободить'
        else:
            auto.dostup = 'Свободен'
            button_name = 'Арендовать' 
    #age_seconds = (datetime.now() - product.created).seconds
    #age = divmod(age_seconds, 60)
    #img_url = auto.img_url[:6]
    #k = int(auto.img_url[6])
        db.session.commit()


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
    }   
       
    return render_template('auto_detail.html', **context)



@app.route('/del_auto/<int:id_auto>', methods=['POST', 'GET'])
def del_auto(id_auto):
    
    auto = Auto.query.get(id_auto)

    context = {'name_auto_del': auto.name}
             
    db.session.delete(auto)
    db.session.commit()

    return render_template('del_auto.html', **context)




@app.route('/rental_log')
def rental_log():
    return render_template('rental_log.html')



