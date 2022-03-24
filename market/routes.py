from unicodedata import category
from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import AddForm, RegisterForm, LoginForm, PurchaseForm, SellForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template("home.html")

@app.route('/market', methods=['GET', 'POST'])
@login_required             #yêu cầu user phải đăng nhập mới được vô trang market ==> file init phải có thêm dòng 13,14
def market_page():
    purchaseForm = PurchaseForm()
    sellForm = SellForm()
    addForm = AddForm()
    
    if request.method == 'POST':
        # Add Item
        item_to_add = Item.query.filter_by(item_name=addForm.name.data).first()
        if item_to_add:
            flash('This item already existed !!', category='danger')
        else:
            add_item = Item(item_name=addForm.name.data,
                            item_barcode=addForm.barcode.data,
                            item_price=addForm.price.data,
                            item_description=addForm.description.data)
            db.session.add(add_item)
            db.session.commit()
            flash(f'{addForm.name.data} is added to the market !!' , category='success')

        # Purchase function
        purchased_item = request.form.get('purchased_item')      #này chỉ lấy tên của item được bấm mua (đọc cục cmt dưới)
        item_obj = Item.query.filter_by(item_name=purchased_item).first()   #dùng tên lấy ra item obj trong db
        if item_obj:
            if current_user.can_purchase(item_obj):
                item_obj.buy(current_user)
                flash(f"Congratulations! You purchased {item_obj.item_name} for {item_obj.item_price}$", category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {item_obj.item_name}!", category='danger')

        # Sell function
        sold_item = request.form.get('sold_item') 
        item_obj2 = Item.query.filter_by(item_name=sold_item).first()   #dùng tên lấy ra item obj trong db
        if item_obj2:
            if current_user.can_sell(item_obj2):
                item_obj2.sell(current_user)
                flash(f"Congratulations! You sold {item_obj2.item_name} for {item_obj2.item_price}$", category='success')
        return redirect(url_for('market_page'))
            # item_obj.item_owner = current_user.id
            # current_user.user_budget -= item_obj.item_price
            # db.session.commit() 
            # flash('Purchase Success!!', category='success')
    # if purchaseForm.validate_on_submit():
        # print(purchaseForm.__dict__)    khi bấm submit thì flask sẽ trả về một đối tượng submit
        # print(purchaseForm['submit'])   
        # in phần value của đối tượng submit ra ta sẽ có 1 thẻ html <input id="submit" name="submit" type="submit" value="Purchase">
        # Để biết được user đã purchase item nào, ta sẽ thay đổi phần value trả về của đối tượng submit thẻ html trêN
        # thành {{ item.item_name }} trong file modals
        #print(request.form.get('purchased_item'))   #để lấy được value của obj submit khi trả về, sẽ sd lib request của flask
        #  .form là built in func của request, và get ra tên của item 

    if request.method == 'GET':
        items = Item.query.filter_by(item_owner=None)    #return all the items in the db MÀ CHƯA CÓ OWNER

        owned_items = Item.query.filter_by(item_owner=current_user.id) 
        return render_template('market.html', items=items, purchaseForm=purchaseForm,owned_items = owned_items, sellForm=sellForm, addForm= addForm)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(user_name=form.username.data,
                        user_email=form.email.data,
                        password=form.password1.data)   
                        #không truyền user_password mà truyền password, để hàm setter trong model generate là user_password
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash('Welcome !!', category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}:       #if there are errors
        for error in form.errors.values():
            flash(f'{error}', category='danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(user_name=form.username.data).first()
        if attempted_user and attempted_user.check_password(form.password.data):
            login_user(attempted_user)
            flash('Success!!', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Log In Error!!', category='danger')      

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('Logged Out!!', category='info')
    return redirect(url_for('home_page'))
