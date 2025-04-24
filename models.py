from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

#Tạo bảng hóa đơn
class Invoice(db.Model):
    __tablename__ = 'Invoice'
    invoice_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customer.customer_id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('Employee.employee_id'), nullable=False)
    date_of_invoice = db.Column(db.Date, nullable=False)
    total_invoice = db.Column(db.Float, nullable=False)
    invoice_details = db.relationship('Invoice_Details', backref='invoice', lazy=True)

    
#Tạo bảng khách hàng
class Customer(db.Model):
    __tablename__ = 'Customer'
    customer_id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    invoices = db.relationship('Invoice', backref='customer', lazy=True)


#Tạo bảng nhân viên
class Employee(db.Model):
    __tablename__ = 'Employee'
    employee_id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    phone = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    address = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(255), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    password = db.Column(db.String(200), nullable=True)
    invoice = db.relationship('Invoice', backref='employee', lazy=True)
    works_at = db.relationship('Work_at', backref='employee', lazy=True)

#Tạo bảng kệ sách
class Book_Shelf(db.Model):
    __tablename__ = 'Book_shelf'
    number = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(255), nullable=False)
    kind_of_book = db.relationship('Kind_of_Book', backref='book_shelf', uselist=False, lazy=True)

#Tạo bảng thể loại sách
class Kind_of_Book(db.Model):
    __tablename__ = 'Kind_of_book'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    book_shelf_number = db.Column(db.Integer, db.ForeignKey('Book_shelf.number'), nullable=False)
    books = db.relationship('Book', backref='category', lazy=True)

#Tạo bảng sách
class Book(db.Model):
    __tablename__ = 'Book'
    book_id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(500), nullable=False)
    authors = db.Column(db.String(255), nullable=False)
    publishing_year = db.Column(db.String(4), nullable=False)
    kind_of_book = db.Column(db.Integer, db.ForeignKey('Kind_of_book.id'), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    #invoices = db.relationship('Invoice_Details', backref='book', lazy=True)


#Tạo bảng chi tiết hóa đơn
class Invoice_Details(db.Model):
    __tablename__ = 'Invoice_Details'
    invoice_id = db.Column(db.Integer, db.ForeignKey('Invoice.invoice_id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('Book.book_id'), nullable=False)  # Định nghĩa cột book_id
    quantity = db.Column(db.Integer, nullable=False)
    cost_book = db.Column(db.Float, nullable=False)
    book = db.relationship('Book', backref='invoice_details')
    
#Tạo bảng vị trí làm việc
class Work_at(db.Model):
    __tablename__ = 'Work_at'
    employee_id = db.Column(db.Integer, db.ForeignKey('Employee.employee_id'), primary_key=True)
    number_book_shelf = db.Column(db.Integer, db.ForeignKey('Book_shelf.number'), primary_key=True)
    