from flask import request, session, redirect, url_for, render_template, flash

from . models import Models
from . forms import AddReaderForm, SignUpForm, SignInForm

from src import app

models = Models()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/books')
def show_books():
    try:
        if session['user_available']:
            booksAndAssignments = models.gettrans()
            summary = models.trans_simple_summary()
            return render_template('books.html', booksAndAssignments=booksAndAssignments, summary=summary)
        flash('User is not Authenticated')
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))

@app.route('/customer')
def show_book2():
    try:
        if session['user_available']:
            booksAndAssignments = models.getcustomers()
            return render_template('customer.html', booksAndAssignments=booksAndAssignments)
        flash('User is not Authenticated')
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))

@app.route('/credit_card')
def show_book3():
    try:
        if session['user_available']:
            booksAndAssignments = models.getcreditcard()
            return render_template('credit_card.html', booksAndAssignments=booksAndAssignments)
        flash('User is not Authenticated')
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))

@app.route('/category')
def show_book4():
    try:
        if session['user_available']:
            booksAndAssignments = models.getprod()
            return render_template('category.html', booksAndAssignments=booksAndAssignments)
        flash('User is not Authenticated')
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))

@app.route('/add', methods=['GET', 'POST'])
def add_reader():
    try:
        if session['user_available']:
            reader = AddReaderForm(request.form)
            if request.method == 'POST':
                models.addAssignment({"email": reader.email.data, "isbn": reader.isbn.data})
                return redirect(url_for('show_books'))
            return render_template('add.html', reader=reader)
    except Exception as e:
        flash(str(e))
    flash('User is not Authenticated')
    return redirect(url_for('index'))

@app.route('/send_data', methods = ['POST'])
def get_data_from_html():
        age = request.form['age']
        gender = request.form['gender']
        credit_card = request.form['credit_card']
        credit_rating = request.form['credit_rating']
        year = request.form['year']
        quarter = request.form['quarter']
        m1 = request.form['m1']
        m2 = request.form['m2']
        bottom = request.form['bottom']
        top = request.form['top']
        category = request.form['category']
        min_age = age[1:3]
        max_age = age[4:6]
        gender_one = gender.split(",")[0]
        gender_two = gender.split(",")[1]
        c1 = credit_card.split(",")[0]
        c2 = credit_card.split(",")[1]
        c3 = credit_card.split(",")[2]
        c4 = credit_card.split(",")[3]
        c5 = credit_card.split(",")[4]
        cr1 = credit_rating.split(",")[0]
        cr2 = credit_rating.split(",")[1]
        year1 = year.split(",")[0]
        year2 = year.split(",")[1]
        q1 = quarter.split(",")[0]
        q2 = quarter.split(",")[1]
        cat1 = category.split(",")[0]
        cat2 = category.split(",")[1]
        cat3 = category.split(",")[2]
        cat4 = category.split(",")[3]
        cat5 = category.split(",")[4]
        cat6 = category.split(",")[5]
        if len(top)==0 and len(bottom)==0:
           n=500
           booksAndAssignments = models.trans_combined_desc(min_age = min_age, max_age = max_age, gender_one=gender_one, gender_two = gender_two, c1=c1, c2=c2, c3=c3, c4=c4, c5=c5, cr1=cr1, cr2=cr2, n=n, year1=year1, year2=year2, q1=q1, q2=q2, m1=m1, m2=m2, cat1=cat1, cat2=cat2, cat3=cat3, cat4=cat4, cat5=cat5, cat6=cat6)
        elif len(top)!=0 and len(bottom)==0:    
           n = top
           booksAndAssignments = models.trans_combined_desc(min_age = min_age, max_age = max_age, gender_one=gender_one, gender_two = gender_two, c1=c1, c2=c2, c3=c3, c4=c4, c5=c5, cr1=cr1, cr2=cr2, n=n, year1=year1, year2=year2, q1=q1, q2=q2, m1=m1, m2=m2, cat1=cat1, cat2=cat2, cat3=cat3, cat4=cat4, cat5=cat5, cat6=cat6)
        elif len(top)==0 and len(bottom)!=0:    
           n = bottom
           booksAndAssignments = models.trans_combined_asc(min_age = min_age, max_age = max_age, gender_one=gender_one, gender_two = gender_two, c1=c1, c2=c2, c3=c3, c4=c4, c5=c5, cr1=cr1, cr2=cr2, n=n, year1=year1, year2=year2, q1=q1, q2=q2, m1=m1, m2=m2, cat1=cat1, cat2=cat2, cat3=cat3, cat4=cat4, cat5=cat5, cat6=cat6)
        summary = models.trans_summary(min_age = min_age, max_age = max_age, gender_one=gender_one, gender_two = gender_two, c1=c1, c2=c2, c3=c3, c4=c4, c5=c5, cr1=cr1, cr2=cr2, n=n, year1=year1, year2=year2, q1=q1, q2=q2, m1=m1, m2=m2, cat1=cat1, cat2=cat2, cat3=cat3, cat4=cat4, cat5=cat5, cat6=cat6)
        #booksAndAssignments = models.customer_combined_desc(min_age = min_age, max_age = max_age, gender_one=gender_one, gender_two = gender_two, c1=c1, c2=c2, c3=c3, c4=c4, c5=c5, cr1=cr1, cr2=cr2, n=n, year1=year1, year2=year2, q1=q1, q2=q2, m1=m1, m2=m2)
        return render_template('books.html', booksAndAssignments=booksAndAssignments, summary = summary)


@app.route('/send_data_credit', methods = ['POST'])
def get_data_from_html7():
        age = request.form['age']
        gender = request.form['gender']
        credit_card = request.form['credit_card']
        credit_rating = request.form['credit_rating']
        year = request.form['year']
        quarter = request.form['quarter']
        m1 = request.form['m1']
        m2 = request.form['m2']
        bottom = request.form['bottom']
        top = request.form['top']
        category = request.form['category']
        min_age = age[1:3]
        max_age = age[4:6]
        gender_one = gender.split(",")[0]
        gender_two = gender.split(",")[1]
        c1 = credit_card.split(",")[0]
        c2 = credit_card.split(",")[1]
        c3 = credit_card.split(",")[2]
        c4 = credit_card.split(",")[3]
        c5 = credit_card.split(",")[4]
        cr1 = credit_rating.split(",")[0]
        cr2 = credit_rating.split(",")[1]
        year1 = year.split(",")[0]
        year2 = year.split(",")[1]
        q1 = quarter.split(",")[0]
        q2 = quarter.split(",")[1]
        cat1 = category.split(",")[0]
        cat2 = category.split(",")[1]
        cat3 = category.split(",")[2]
        cat4 = category.split(",")[3]
        cat5 = category.split(",")[4]
        cat6 = category.split(",")[5]
        if len(top)==0 and len(bottom)==0:
           n=500
           booksAndAssignments = models.credit_combined_desc(min_age = min_age, max_age = max_age, gender_one=gender_one, gender_two = gender_two, c1=c1, c2=c2, c3=c3, c4=c4, c5=c5, cr1=cr1, cr2=cr2, n=n, year1=year1, year2=year2, q1=q1, q2=q2, m1=m1, m2=m2, cat1=cat1, cat2=cat2, cat3=cat3, cat4=cat4, cat5=cat5, cat6=cat6)
        elif len(top)!=0 and len(bottom)==0:    
           n = top
           booksAndAssignments = models.credit_combined_desc(min_age = min_age, max_age = max_age, gender_one=gender_one, gender_two = gender_two, c1=c1, c2=c2, c3=c3, c4=c4, c5=c5, cr1=cr1, cr2=cr2, n=n, year1=year1, year2=year2, q1=q1, q2=q2, m1=m1, m2=m2, cat1=cat1, cat2=cat2, cat3=cat3, cat4=cat4, cat5=cat5, cat6=cat6)
        elif len(top)==0 and len(bottom)!=0:    
           n = bottom
           booksAndAssignments = models.credit_combined_asc(min_age = min_age, max_age = max_age, gender_one=gender_one, gender_two = gender_two, c1=c1, c2=c2, c3=c3, c4=c4, c5=c5, cr1=cr1, cr2=cr2, n=n, year1=year1, year2=year2, q1=q1, q2=q2, m1=m1, m2=m2, cat1=cat1, cat2=cat2, cat3=cat3, cat4=cat4, cat5=cat5, cat6=cat6)
        #booksAndAssignments = models.customer_combined_desc(min_age = min_age, max_age = max_age, gender_one=gender_one, gender_two = gender_two, c1=c1, c2=c2, c3=c3, c4=c4, c5=c5, cr1=cr1, cr2=cr2, n=n, year1=year1, year2=year2, q1=q1, q2=q2, m1=m1, m2=m2)
        return render_template('credit_card.html', booksAndAssignments=booksAndAssignments)

@app.route('/send_data_cat', methods = ['POST'])
def get_data_from_html8():
        age = request.form['age']
        gender = request.form['gender']
        credit_card = request.form['credit_card']
        credit_rating = request.form['credit_rating']
        year = request.form['year']
        quarter = request.form['quarter']
        m1 = request.form['m1']
        m2 = request.form['m2']
        bottom = request.form['bottom']
        top = request.form['top']
        category = request.form['category']
        min_age = age[1:3]
        max_age = age[4:6]
        gender_one = gender.split(",")[0]
        gender_two = gender.split(",")[1]
        c1 = credit_card.split(",")[0]
        c2 = credit_card.split(",")[1]
        c3 = credit_card.split(",")[2]
        c4 = credit_card.split(",")[3]
        c5 = credit_card.split(",")[4]
        cr1 = credit_rating.split(",")[0]
        cr2 = credit_rating.split(",")[1]
        year1 = year.split(",")[0]
        year2 = year.split(",")[1]
        q1 = quarter.split(",")[0]
        q2 = quarter.split(",")[1]
        cat1 = category.split(",")[0]
        cat2 = category.split(",")[1]
        cat3 = category.split(",")[2]
        cat4 = category.split(",")[3]
        cat5 = category.split(",")[4]
        cat6 = category.split(",")[5]
        if len(top)==0 and len(bottom)==0:
           n=500
           booksAndAssignments = models.cat_combined_desc(min_age = min_age, max_age = max_age, gender_one=gender_one, gender_two = gender_two, c1=c1, c2=c2, c3=c3, c4=c4, c5=c5, cr1=cr1, cr2=cr2, n=n, year1=year1, year2=year2, q1=q1, q2=q2, m1=m1, m2=m2, cat1=cat1, cat2=cat2, cat3=cat3, cat4=cat4, cat5=cat5, cat6=cat6)
        elif len(top)!=0 and len(bottom)==0:    
           n = top
           booksAndAssignments = models.cat_combined_desc(min_age = min_age, max_age = max_age, gender_one=gender_one, gender_two = gender_two, c1=c1, c2=c2, c3=c3, c4=c4, c5=c5, cr1=cr1, cr2=cr2, n=n, year1=year1, year2=year2, q1=q1, q2=q2, m1=m1, m2=m2, cat1=cat1, cat2=cat2, cat3=cat3, cat4=cat4, cat5=cat5, cat6=cat6)
        elif len(top)==0 and len(bottom)!=0:    
           n = bottom
           booksAndAssignments = models.cat_combined_asc(min_age = min_age, max_age = max_age, gender_one=gender_one, gender_two = gender_two, c1=c1, c2=c2, c3=c3, c4=c4, c5=c5, cr1=cr1, cr2=cr2, n=n, year1=year1, year2=year2, q1=q1, q2=q2, m1=m1, m2=m2, cat1=cat1, cat2=cat2, cat3=cat3, cat4=cat4, cat5=cat5, cat6=cat6)
        #booksAndAssignments = models.customer_combined_desc(min_age = min_age, max_age = max_age, gender_one=gender_one, gender_two = gender_two, c1=c1, c2=c2, c3=c3, c4=c4, c5=c5, cr1=cr1, cr2=cr2, n=n, year1=year1, year2=year2, q1=q1, q2=q2, m1=m1, m2=m2)
        return render_template('category.html', booksAndAssignments=booksAndAssignments)



@app.route('/send_data3', methods = ['POST'])
def get_data_from_html3():
        age = request.form['age']
        gender = request.form['gender']
        credit_card = request.form['credit_card']
        credit_rating = request.form['credit_rating']
        year = request.form['year']
        quarter = request.form['quarter']
        m1 = request.form['m1']
        m2 = request.form['m2']
        bottom = request.form['bottom']
        top = request.form['top']
        category = request.form['category']
        min_age = age[1:3]
        max_age = age[4:6]
        gender_one = gender.split(",")[0]
        gender_two = gender.split(",")[1]
        c1 = credit_card.split(",")[0]
        c2 = credit_card.split(",")[1]
        c3 = credit_card.split(",")[2]
        c4 = credit_card.split(",")[3]
        c5 = credit_card.split(",")[4]
        cr1 = credit_rating.split(",")[0]
        cr2 = credit_rating.split(",")[1]
        year1 = year.split(",")[0]
        year2 = year.split(",")[1]
        q1 = quarter.split(",")[0]
        q2 = quarter.split(",")[1]
        cat1 = category.split(",")[0]
        cat2 = category.split(",")[1]
        cat3 = category.split(",")[2]
        cat4 = category.split(",")[3]
        cat5 = category.split(",")[4]
        cat6 = category.split(",")[5]
        if len(top)==0 and len(bottom)==0:
           n=500
           booksAndAssignments = models.customer_combined_desc(min_age = min_age, max_age = max_age, gender_one=gender_one, gender_two = gender_two, c1=c1, c2=c2, c3=c3, c4=c4, c5=c5, cr1=cr1, cr2=cr2, n=n, year1=year1, year2=year2, q1=q1, q2=q2, m1=m1, m2=m2, cat1=cat1, cat2=cat2, cat3=cat3, cat4=cat4, cat5=cat5, cat6=cat6)
        elif len(top)!=0 and len(bottom)==0:    
           n = top
           booksAndAssignments = models.customer_combined_desc(min_age = min_age, max_age = max_age, gender_one=gender_one, gender_two = gender_two, c1=c1, c2=c2, c3=c3, c4=c4, c5=c5, cr1=cr1, cr2=cr2, n=n, year1=year1, year2=year2, q1=q1, q2=q2, m1=m1, m2=m2, cat1=cat1, cat2=cat2, cat3=cat3, cat4=cat4, cat5=cat5, cat6=cat6)
        elif len(top)==0 and len(bottom)!=0:    
           n = bottom
           booksAndAssignments = models.customer_combined_asc(min_age = min_age, max_age = max_age, gender_one=gender_one, gender_two = gender_two, c1=c1, c2=c2, c3=c3, c4=c4, c5=c5, cr1=cr1, cr2=cr2, n=n, year1=year1, year2=year2, q1=q1, q2=q2, m1=m1, m2=m2, cat1=cat1, cat2=cat2, cat3=cat3, cat4=cat4, cat5=cat5, cat6=cat6)
        #booksAndAssignments = models.customer_combined_desc(min_age = min_age, max_age = max_age, gender_one=gender_one, gender_two = gender_two, c1=c1, c2=c2, c3=c3, c4=c4, c5=c5, cr1=cr1, cr2=cr2, n=n, year1=year1, year2=year2, q1=q1, q2=q2, m1=m1, m2=m2)
        return render_template('customer.html', booksAndAssignments=booksAndAssignments)

@app.route('/delete/<email>/<isbn>', methods=('GET', 'POST'))
def delete_book(isbn, email):
    try:
        models.deleteAssignment({"email": email, "isbn": isbn})
        return redirect(url_for('show_books'))
    except Exception as e:
        flash(str(e))
        return redirect(url_for('index'))


@app.route('/update/<email>/<isbn>', methods=('GET', 'POST'))
def update_book(isbn, email):
    try:
        br = models.getAssignment({"email": email, "isbn": isbn})
        reader = AddReaderForm(request.form, obj=br)
        if request.method == 'POST':
            models.updateAssignment({"email": reader.email.data, "isbn": reader.isbn.data})
            return redirect(url_for('show_books'))
        return render_template('update.html', reader=reader)
    except Exception as e:
        flash(str(e))
        return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    try:
        signupform = SignUpForm(request.form)
        if request.method == 'POST':
            models.addProfessor({"email": signupform.email.data, "password": signupform.password.data})
            return redirect(url_for('signin'))
        return render_template('signup.html', signupform=signupform)
    except Exception as e:
        flash(str(e))
        return redirect(url_for('index'))


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    try:
        signinform = SignInForm(request.form)
        if request.method == 'POST':
            em = signinform.email.data
            log = models.getProfessorByEmail(em)
            if log.password == signinform.password.data:
                session['current_user'] = em
                session['user_available'] = True
                return redirect(url_for('show_books'))
            else:
                flash('Cannot sign in')
        return render_template('signin.html', signinform=signinform)
    except Exception as e:
        flash(str(e))
        return redirect(url_for('index'))


@app.route('/about_user')
def about_user():
    try:
        if session['user_available']:
            regmodules = models.getRegMod()
            user = models.getProfessorByEmail(session['current_user'])
            return render_template('about_user.html', user=user, regmodules=regmodules)
        flash('You are not a Authenticated User')
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    try:
        session.clear()
        session['user_available'] = False
        return redirect(url_for('index'))
    except Exception as e:
        flash(str(e))
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
