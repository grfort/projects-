from sqlalchemy import create_engine
from sqlalchemy.sql import text
import os

class Models:
    def __init__(self):
        self.engine = create_engine(os.environ.get('DB_URL', 'postgresql://zkpttjedffgdun:7a50402abf0648b467bfe604b07e2c047acc1ab10ede1972ff7f67228a3d43c2@ec2-44-195-132-31.compute-1.amazonaws.com:5432/df5d009s66jv78'))

    def executeRawSql(self, statement, params={}):
        out = None
        with self.engine.connect() as con:
            out = con.execute(text(statement), params)
        return out

    def addProfessor(self, value):
        return self.executeRawSql("""INSERT INTO professor (email, password) VALUES(:email, :password);""", value)

    def addBook(self, value):
        # value has the form { "isbn": 2, "title": "The Silmarillion", "author": "Tolkien" }
        return self.executeRawSql("""INSERT INTO book(isbn, title, author) VALUES(:isbn, :title, :author);""", value)

    def updateAssignment(self, value):
        return self.executeRawSql("""UPDATE assignment SET email=:email WHERE isbn=:isbn;""", value)
    
    def addAssignment(self, value):
        return self.executeRawSql("""INSERT INTO assignment(email, isbn) VALUES(:email, :isbn);""", value)

    def getAllAssignments(self):
        #some changes
        return self.executeRawSql("SELECT * FROM assignment;").mappings().all()

    def deleteAssignment(self, value):
        return self.executeRawSql("DELETE FROM assignment where email=:email and isbn=:isbn;", value)

    def getAssignment(self, value):
        values = self.executeRawSql("""SELECT * FROM assignment WHERE email=:email and isbn=:isbn;""", value).mappings().all()
        if len(values) == 0:
            raise Exception("Book {} has not been assignment by {}".format(value["isbn"], value["email"]))
        return values[0]

    def getAllBooks(self):
        return self.executeRawSql("SELECT * FROM book;").mappings().all()

    def getAllUsers(self):
        return self.executeRawSql("SELECT * FROM student;").mappings().all()

    def getBooksAndAssignments(self):
        return self.executeRawSql("SELECT book.isbn, email, title, author FROM book LEFT JOIN assignment ON book.isbn = assignment.isbn;").mappings().all()

    def getRegMod(self):
        return self.executeRawSql("SELECT * FROM reg_mod2;").mappings().all()

    def getcustomers(self):
        return self.executeRawSql("select c.customer_id, c.full_name, c.gender, c.age, c.occupation, c.annual_income, c.credit_rating, sum(t.sales_amount) from customers c inner join transaction t on c.customer_id = t.customer_id inner join credit_card cr on cr.customer_id = c.customer_id group by (c.customer_id);").mappings().all()
    
    def getcreditcard(self):
        return self.executeRawSql("select distinct(credit_card_type), count(t.transaction_id), sum(sales_amount) from credit_card cr inner join transaction t on cr.customer_id = t.customer_id group by (credit_card_type);").mappings().all()
    
    def getprod(self):
        return self.executeRawSql("select p.product_id, p.product_name, p.company_name, p.category, sum(t.sales_amount) from customers c inner join transaction t on c.customer_id = t.customer_id inner join credit_card cr on cr.customer_id = c.customer_id left join prod p on t.product_id = p.product_id left join date d on d.date = t.date group by p.product_id order by sum(t.sales_amount) desc;").mappings().all()

    def gettrans(self):
        return self.executeRawSql("select * from transaction;").mappings().all()
    
    def customer_age(self, age=None):
        return self.executeRawSql("""select c.customer_id, c.full_name, c.gender, c.age, c.occupation, c.annual_income, c.credit_rating, sum(t.sales_amount) from customers c inner join transaction t on c.customer_id = t.customer_id where age>=:age and age<=:age+9 group by (c.customer_id);""", {"age": age}).mappings().all()
    
    def customer_gender(self, gender=None):
        return self.executeRawSql("""select c.customer_id, c.full_name, c.gender, c.age, c.occupation, c.annual_income, c.credit_rating, sum(t.sales_amount) from customers c inner join transaction t on c.customer_id = t.customer_id where gender=:gender group by (c.customer_id);""", {"gender": gender}).mappings().all()

    def customer_combined_desc(self, min_age=0, max_age = 90, gender_one=None, gender_two = None, c1 = None, c2 = None, c3 = None, c4 = None, c5 = None, cr1 = None, cr2 = None, n=50, year1=None, year2=None, q1=None, q2=None, m1=None, m2=None, cat1=None, cat2=None,cat3=None,cat4=None,cat5=None,cat6=None):
        return self.executeRawSql("""select c.customer_id, c.full_name, c.gender, c.age, c.occupation, c.annual_income, c.credit_rating, sum(t.sales_amount) from customers c inner join transaction t on c.customer_id = t.customer_id inner join credit_card cr on cr.customer_id = c.customer_id left join prod p on t.product_id = p.product_id left join date d on d.date = t.date where age>=:min_age and age<=:max_age and gender IN (:gender_one, :gender_two) and credit_card_type IN (:c1, :c2, :c3, :c4, :c5) and credit_rating>=:cr1 and credit_rating<=:cr2 and (date_part('year',t.date)>=:year1 and date_part('year',t.date)<=:year2) and (quarter BETWEEN :q1 and :q2) and (month BETWEEN :m1 and :m2) and category IN (:cat1, :cat2,:cat3,:cat4,:cat5,:cat6) group by (c.customer_id) order by sum(t.sales_amount) desc limit :n;""", {"min_age": min_age, "max_age": max_age, "gender_one": gender_one, "gender_two":gender_two, "c1":c1, "c2":c2, "c3":c3, "c4":c4, "c5":c5, "cr1":cr1, "cr2":cr2, "n":n, "year1":year1, "year2":year2, "q1":q1, "q2":q2, "m1":m1, "m2":m2, "cat1":cat1, "cat2":cat2, "cat3":cat3, "cat4":cat4, "cat5":cat5, "cat6":cat6}).mappings().all()
    
    def customer_combined_asc(self, min_age=0, max_age = 90, gender_one=None, gender_two = None, c1 = None, c2 = None, c3 = None, c4 = None, c5 = None, cr1 = None, cr2 = None, n=50, year1=None, year2=None, q1=None, q2=None, m1=None, m2=None, cat1=None, cat2=None,cat3=None,cat4=None,cat5=None,cat6=None):
        return self.executeRawSql("""select c.customer_id, c.full_name, c.gender, c.age, c.occupation, c.annual_income, c.credit_rating, sum(t.sales_amount) from customers c inner join transaction t on c.customer_id = t.customer_id inner join credit_card cr on cr.customer_id = c.customer_id left join prod p on t.product_id = p.product_id left join date d on d.date = t.date where age>=:min_age and age<=:max_age and gender IN (:gender_one, :gender_two) and credit_card_type IN (:c1, :c2, :c3, :c4, :c5) and credit_rating>=:cr1 and credit_rating<=:cr2 and (date_part('year',t.date)>=:year1 and date_part('year',t.date)<=:year2) and (quarter BETWEEN :q1 and :q2) and (month BETWEEN :m1 and :m2) and category IN (:cat1, :cat2,:cat3,:cat4,:cat5,:cat6) group by (c.customer_id) order by sum(t.sales_amount) asc limit :n;""", {"min_age": min_age, "max_age": max_age, "gender_one": gender_one, "gender_two":gender_two, "c1":c1, "c2":c2, "c3":c3, "c4":c4, "c5":c5, "cr1":cr1, "cr2":cr2, "n":n, "year1":year1, "year2":year2, "q1":q1, "q2":q2, "m1":m1, "m2":m2, "cat1":cat1, "cat2":cat2, "cat3":cat3, "cat4":cat4, "cat5":cat5, "cat6":cat6}).mappings().all()
    
    def trans_simple_summary(self):
        return self.executeRawSql("select d.month, sum(t.sales_amount), count(t.transaction_id) from customers c inner join transaction t on c.customer_id = t.customer_id inner join credit_card cr on cr.customer_id = c.customer_id left join prod p on t.product_id = p.product_id left join date d on d.date = t.date group by d.month order by d.month asc;").mappings().all()
    
    def trans_summary(self, min_age=0, max_age = 90, gender_one=None, gender_two = None, c1 = None, c2 = None, c3 = None, c4 = None, c5 = None, cr1 = None, cr2 = None, n=50, year1=None, year2=None, q1=None, q2=None, m1=None, m2=None, cat1=None, cat2=None,cat3=None,cat4=None,cat5=None,cat6=None):
        return self.executeRawSql("""select d.month, sum(t.sales_amount), count(t.transaction_id) from customers c inner join transaction t on c.customer_id = t.customer_id inner join credit_card cr on cr.customer_id = c.customer_id left join prod p on t.product_id = p.product_id left join date d on d.date = t.date where age>=:min_age and age<=:max_age and gender IN (:gender_one, :gender_two) and credit_card_type IN (:c1, :c2, :c3, :c4, :c5) and credit_rating>=:cr1 and credit_rating<=:cr2 and (date_part('year',t.date)>=:year1 and date_part('year',t.date)<=:year2) and (quarter BETWEEN :q1 and :q2) and (month BETWEEN :m1 and :m2) and category IN (:cat1, :cat2,:cat3,:cat4,:cat5,:cat6) group by d.month order by d.month asc;""", {"min_age": min_age, "max_age": max_age, "gender_one": gender_one, "gender_two":gender_two, "c1":c1, "c2":c2, "c3":c3, "c4":c4, "c5":c5, "cr1":cr1, "cr2":cr2, "n":n, "year1":year1, "year2":year2, "q1":q1, "q2":q2, "m1":m1, "m2":m2, "cat1":cat1, "cat2":cat2, "cat3":cat3, "cat4":cat4, "cat5":cat5, "cat6":cat6}).mappings().all()

    def trans_combined_desc(self, min_age=0, max_age = 90, gender_one=None, gender_two = None, c1 = None, c2 = None, c3 = None, c4 = None, c5 = None, cr1 = None, cr2 = None, n=50, year1=None, year2=None, q1=None, q2=None, m1=None, m2=None, cat1=None, cat2=None,cat3=None,cat4=None,cat5=None,cat6=None):
        return self.executeRawSql("""select t.date, t.sales_amount, t.transaction_id from customers c inner join transaction t on c.customer_id = t.customer_id inner join credit_card cr on cr.customer_id = c.customer_id left join prod p on t.product_id = p.product_id left join date d on d.date = t.date where age>=:min_age and age<=:max_age and gender IN (:gender_one, :gender_two) and credit_card_type IN (:c1, :c2, :c3, :c4, :c5) and credit_rating>=:cr1 and credit_rating<=:cr2 and (date_part('year',t.date)>=:year1 and date_part('year',t.date)<=:year2) and (quarter BETWEEN :q1 and :q2) and (month BETWEEN :m1 and :m2) and category IN (:cat1, :cat2,:cat3,:cat4,:cat5,:cat6) order by t.sales_amount desc limit :n;""", {"min_age": min_age, "max_age": max_age, "gender_one": gender_one, "gender_two":gender_two, "c1":c1, "c2":c2, "c3":c3, "c4":c4, "c5":c5, "cr1":cr1, "cr2":cr2, "n":n, "year1":year1, "year2":year2, "q1":q1, "q2":q2, "m1":m1, "m2":m2, "cat1":cat1, "cat2":cat2, "cat3":cat3, "cat4":cat4, "cat5":cat5, "cat6":cat6}).mappings().all()
    
    def trans_combined_asc(self, min_age=0, max_age = 90, gender_one=None, gender_two = None, c1 = None, c2 = None, c3 = None, c4 = None, c5 = None, cr1 = None, cr2 = None, n=50, year1=None, year2=None, q1=None, q2=None, m1=None, m2=None, cat1=None, cat2=None,cat3=None,cat4=None,cat5=None,cat6=None):
        return self.executeRawSql("""select t.date, t.sales_amount, t.transaction_id from customers c inner join transaction t on c.customer_id = t.customer_id inner join credit_card cr on cr.customer_id = c.customer_id left join prod p on t.product_id = p.product_id left join date d on d.date = t.date where age>=:min_age and age<=:max_age and gender IN (:gender_one, :gender_two) and credit_card_type IN (:c1, :c2, :c3, :c4, :c5) and credit_rating>=:cr1 and credit_rating<=:cr2 and (date_part('year',t.date)>=:year1 and date_part('year',t.date)<=:year2) and (quarter BETWEEN :q1 and :q2) and (month BETWEEN :m1 and :m2) and category IN (:cat1, :cat2,:cat3,:cat4,:cat5,:cat6) order by t.sales_amount asc limit :n;""", {"min_age": min_age, "max_age": max_age, "gender_one": gender_one, "gender_two":gender_two, "c1":c1, "c2":c2, "c3":c3, "c4":c4, "c5":c5, "cr1":cr1, "cr2":cr2, "n":n, "year1":year1, "year2":year2, "q1":q1, "q2":q2, "m1":m1, "m2":m2, "cat1":cat1, "cat2":cat2, "cat3":cat3, "cat4":cat4, "cat5":cat5, "cat6":cat6}).mappings().all()

    def credit_combined_desc(self, min_age=0, max_age = 90, gender_one=None, gender_two = None, c1 = None, c2 = None, c3 = None, c4 = None, c5 = None, cr1 = None, cr2 = None, n=50, year1=None, year2=None, q1=None, q2=None, m1=None, m2=None, cat1=None, cat2=None,cat3=None,cat4=None,cat5=None,cat6=None):
        return self.executeRawSql("""select distinct(credit_card_type), count(t.transaction_id), sum(sales_amount) from customers c inner join transaction t on c.customer_id = t.customer_id inner join credit_card cr on cr.customer_id = c.customer_id left join prod p on t.product_id = p.product_id left join date d on d.date = t.date where age>=:min_age and age<=:max_age and gender IN (:gender_one, :gender_two) and credit_card_type IN (:c1, :c2, :c3, :c4, :c5) and credit_rating>=:cr1 and credit_rating<=:cr2 and (date_part('year',t.date)>=:year1 and date_part('year',t.date)<=:year2) and (quarter BETWEEN :q1 and :q2) and (month BETWEEN :m1 and :m2) and category IN (:cat1, :cat2,:cat3,:cat4,:cat5,:cat6) group by credit_card_type order by sum(t.sales_amount) desc limit :n;""", {"min_age": min_age, "max_age": max_age, "gender_one": gender_one, "gender_two":gender_two, "c1":c1, "c2":c2, "c3":c3, "c4":c4, "c5":c5, "cr1":cr1, "cr2":cr2, "n":n, "year1":year1, "year2":year2, "q1":q1, "q2":q2, "m1":m1, "m2":m2, "cat1":cat1, "cat2":cat2, "cat3":cat3, "cat4":cat4, "cat5":cat5, "cat6":cat6}).mappings().all()
    
    def credit_combined_asc(self, min_age=0, max_age = 90, gender_one=None, gender_two = None, c1 = None, c2 = None, c3 = None, c4 = None, c5 = None, cr1 = None, cr2 = None, n=50, year1=None, year2=None, q1=None, q2=None, m1=None, m2=None, cat1=None, cat2=None,cat3=None,cat4=None,cat5=None,cat6=None):
        return self.executeRawSql("""select distinct(credit_card_type), count(t.transaction_id), sum(sales_amount) from customers c inner join transaction t on c.customer_id = t.customer_id inner join credit_card cr on cr.customer_id = c.customer_id left join prod p on t.product_id = p.product_id left join date d on d.date = t.date where age>=:min_age and age<=:max_age and gender IN (:gender_one, :gender_two) and credit_card_type IN (:c1, :c2, :c3, :c4, :c5) and credit_rating>=:cr1 and credit_rating<=:cr2 and (date_part('year',t.date)>=:year1 and date_part('year',t.date)<=:year2) and (quarter BETWEEN :q1 and :q2) and (month BETWEEN :m1 and :m2) and category IN (:cat1, :cat2,:cat3,:cat4,:cat5,:cat6) group by credit_card_type order by sum(t.sales_amount) asc limit :n;""", {"min_age": min_age, "max_age": max_age, "gender_one": gender_one, "gender_two":gender_two, "c1":c1, "c2":c2, "c3":c3, "c4":c4, "c5":c5, "cr1":cr1, "cr2":cr2, "n":n, "year1":year1, "year2":year2, "q1":q1, "q2":q2, "m1":m1, "m2":m2, "cat1":cat1, "cat2":cat2, "cat3":cat3, "cat4":cat4, "cat5":cat5, "cat6":cat6}).mappings().all()
    
    def cat_combined_desc(self, min_age=0, max_age = 90, gender_one=None, gender_two = None, c1 = None, c2 = None, c3 = None, c4 = None, c5 = None, cr1 = None, cr2 = None, n=50, year1=None, year2=None, q1=None, q2=None, m1=None, m2=None, cat1=None, cat2=None,cat3=None,cat4=None,cat5=None,cat6=None):
        return self.executeRawSql("""select p.product_id, p.product_name, p.category, p.company_name, sum(t.sales_amount) from customers c inner join transaction t on c.customer_id = t.customer_id inner join credit_card cr on cr.customer_id = c.customer_id left join prod p on t.product_id = p.product_id left join date d on d.date = t.date where age>=:min_age and age<=:max_age and gender IN (:gender_one, :gender_two) and credit_card_type IN (:c1, :c2, :c3, :c4, :c5) and credit_rating>=:cr1 and credit_rating<=:cr2 and (date_part('year',t.date)>=:year1 and date_part('year',t.date)<=:year2) and (quarter BETWEEN :q1 and :q2) and (month BETWEEN :m1 and :m2) and category IN (:cat1, :cat2,:cat3,:cat4,:cat5,:cat6) group by p.product_id order by sum(t.sales_amount) desc limit :n;""", {"min_age": min_age, "max_age": max_age, "gender_one": gender_one, "gender_two":gender_two, "c1":c1, "c2":c2, "c3":c3, "c4":c4, "c5":c5, "cr1":cr1, "cr2":cr2, "n":n, "year1":year1, "year2":year2, "q1":q1, "q2":q2, "m1":m1, "m2":m2, "cat1":cat1, "cat2":cat2, "cat3":cat3, "cat4":cat4, "cat5":cat5, "cat6":cat6}).mappings().all()
    
    def cat_combined_asc(self, min_age=0, max_age = 90, gender_one=None, gender_two = None, c1 = None, c2 = None, c3 = None, c4 = None, c5 = None, cr1 = None, cr2 = None, n=50, year1=None, year2=None, q1=None, q2=None, m1=None, m2=None, cat1=None, cat2=None,cat3=None,cat4=None,cat5=None,cat6=None):
        return self.executeRawSql("""select p.product_id, p.product_name, p.category, p.company_name, sum(t.sales_amount) from customers c inner join transaction t on c.customer_id = t.customer_id inner join credit_card cr on cr.customer_id = c.customer_id left join prod p on t.product_id = p.product_id left join date d on d.date = t.date where age>=:min_age and age<=:max_age and gender IN (:gender_one, :gender_two) and credit_card_type IN (:c1, :c2, :c3, :c4, :c5) and credit_rating>=:cr1 and credit_rating<=:cr2 and (date_part('year',t.date)>=:year1 and date_part('year',t.date)<=:year2) and (quarter BETWEEN :q1 and :q2) and (month BETWEEN :m1 and :m2) and category IN (:cat1, :cat2,:cat3,:cat4,:cat5,:cat6) group by p.product_id order by sum(t.sales_amount) asc limit :n;""", {"min_age": min_age, "max_age": max_age, "gender_one": gender_one, "gender_two":gender_two, "c1":c1, "c2":c2, "c3":c3, "c4":c4, "c5":c5, "cr1":cr1, "cr2":cr2, "n":n, "year1":year1, "year2":year2, "q1":q1, "q2":q2, "m1":m1, "m2":m2, "cat1":cat1, "cat2":cat2, "cat3":cat3, "cat4":cat4, "cat5":cat5, "cat6":cat6}).mappings().all()

    def getSelectedMod(self, isbn=None):
        return self.executeRawSql("""SELECT * FROM book WHERE isbn=:isbn;""", {"isbn": isbn}).mappings().all()

    def getProfessorByEmail(self, email):
        values = self.executeRawSql("""SELECT * FROM professor WHERE email=:email;""", {"email": email}).mappings().all()
        if len(values) == 0:
            raise Exception("Professor {} does not exist".format(email))
        return values[0]

    def getStudentByEmail(self, email):
        values = self.executeRawSql("""SELECT * FROM student WHERE email=:email;""", {"email": email}).mappings().all()
        if len(values) == 0:
            raise Exception("Student {} does not exist".format(email))
        return values[0]

    def createModels(self):
        self.executeRawSql(
        """CREATE TABLE IF NOT EXISTS student (
            email TEXT PRIMARY KEY
        );
        """)

        self.executeRawSql(
        """CREATE TABLE IF NOT EXISTS professor (
            email TEXT PRIMARY KEY,
            password TEXT NOT NULL
        );
        """)

        self.executeRawSql(
            """CREATE TABLE IF NOT EXISTS book (
                isbn TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL
            );
            """)

        self.executeRawSql(
            """CREATE TABLE IF NOT EXISTS assignment (
                email TEXT REFERENCES student(email),
                isbn TEXT REFERENCES book(isbn),
                PRIMARY KEY (isbn, email)
            );
            """)

        self.executeRawSql(
            """CREATE TABLE IF NOT EXISTS reg_mod2 (
                isbn TEXT,
                title TEXT,
                author TEXT
            );
            """)

        self.executeRawSql(
            """CREATE TABLE IF NOT EXISTS customers (
                customer_id INT PRIMARY KEY,
                full_name VARCHAR(50),
                gender VARCHAR(50),
                age INT,
                occupation VARCHAR(24),
                annual_income INT,
                credit_rating INT
            );
            """)
        
        self.executeRawSql(
            """create table if not exists credit_card (
                customer_id INT PRIMARY KEY,
                credit_card_type VARCHAR(23)
            );
            """)


        self.executeRawSql(
            """create table if not exists product (
                product_id INT PRIMARY KEY,
                company_name VARCHAR(50),
                category VARCHAR(11),
                product_name DECIMAL(10,2),
                product_price DECIMAL(5,2)
            );
            """)
        

        self.executeRawSql(
            """ create table if not exists prod (
                product_id INT PRIMARY KEY,
                company_name VARCHAR(50),
                category VARCHAR(11),
                product_name VARCHAR(50),
                product_price DECIMAL(5,2)
            );
            """)

        self.executeRawSql(
            """ create table if not exists transaction (
                transaction_id VARCHAR(50) PRIMARY KEY,
                date DATE,
                customer_id INT,
                product_id INT,
                sales_quantity INT,
                sales_amount DECIMAL(5,2)
            );
            """)
        
        self.executeRawSql(
            """ create table if not exists date (
                date DATE PRIMARY KEY,
                year INT,
                month INT,
                day INT,
                quarter INT
            );
            """)
        

# data = ( { "id": 1, "title": "The Hobbit", "primary_author": "Tolkien" },
    #              { "id": 2, "title": "The Silmarillion", "primary_author": "Tolkien" },
    #     )

    # statement = text("""INSERT INTO book(id, title, primary_author) VALUES(:id, :title, :primary_author)""")