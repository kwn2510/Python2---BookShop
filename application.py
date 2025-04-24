from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Customer, Employee, Book_Shelf, Kind_of_Book, Book, Invoice, Invoice_Details  

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:25102004@localhost:5432/Book Shop'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = "ntlhsntlhs"
db.init_app(app)


#Login
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        employee = Employee.query.filter_by(email=email, password=password).first()
        
        if employee and employee.password == password:
            session["employee_id"] = employee.employee_id
            session["employee_name"] = employee.employee_name
            session["position"] = employee.position
            flash(f"WELCOME, {employee.employee_name}!", "success")
            
            return redirect(url_for("select"))
        else:
            flash("Invalid email or password")
            return redirect(url_for("login"))
    return render_template("login.html")

#Logout
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully")
    return redirect(url_for("login"))

#Chọn tính năng
@app.route("/select")
def select():
    if "position" not in session:
        flash("Please log in first")
        return redirect(url_for("login"))
    
    position = session["position"].strip().lower()
    return render_template("select.html", position=position, name=session["employee_name"])
        




#Thêm khách hàng 
@app.route("/addNewCustomer", methods=['GET'])
def addNewCustomer():
    return render_template("/insert_new_customer.html")

@app.route("/addNewCustomerCommit", methods=['POST'])
def addNewCustomerCommit():
    customer_id = request.form.get("customer_id")
    customer_name = request.form.get("customer_name")
    address = request.form.get("address")
    phone = request.form.get("phone")
    email = request.form.get("email")
    # Kiểm tra xem khách hàng đã tồn tại chưa
    existing_customer = Customer.query.filter_by(phone=phone).first()
    if existing_customer:
        flash("Số điện thoại đã tồn tại. Vui lòng sử dụng số khác.", "error")
        return redirect(url_for("addNewCustomer"))
    customer = Customer(customer_id=customer_id, customer_name=customer_name, address=address, phone=phone, email=email)
    db.session.add(customer)
    db.session.commit()
    flash("Thêm khách hàng thành công", "success")
    return redirect(url_for("showAllCustomer"))

#Đọc danh sách khách hàng
@app.route("/showAllCustomer", methods=['GET', 'POST'])
def showAllCustomer():
    customers = Customer.query.all()
    return render_template("show_all_customer.html", customers=customers)

#Xóa khách hàng
@app.route("/delete_customer/<int:customer_id>", methods=['GET', 'POST'])
def delete_customer(customer_id):
    # Tìm khách hàng theo ID
    customer = Customer.query.get(customer_id)
    
    # Kiểm tra nếu khách hàng tồn tại
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return redirect(url_for("showAllCustomer"))
    else:
        return "Khách hàng không tồn tại.", 404

#Sửa thông tin khách hàng
@app.route("/edit_customer/<int:customer_id>", methods=['GET', 'POST'])
def edit_customer(customer_id):
    # Tìm khách hàng theo ID
    customer = Customer.query.get(customer_id)
    
    if not customer:
        return "Khách hàng không tồn tại.", 404

    if request.method == 'POST':
        # Lấy dữ liệu từ form
        customer.customer_name = request.form.get("customer_name")
        customer.address = request.form.get("address")
        customer.phone = request.form.get("phone")
        customer.email = request.form.get("email")
        
        # Lưu thay đổi vào cơ sở dữ liệu
        db.session.commit()
        return redirect(url_for("showAllCustomer"))

    return render_template("edit_customer.html", customer=customer)

#Thêm thông tin nhân viên
@app.route("/addNewEmployee", methods=['GET'])
def addNewEmployee():
    return render_template("insert_new_employee.html")

@app.route("/addNewEmployeeCommit", methods=['POST'])
def addNewEmployeeCommit():
    employee_id = request.form.get("employee_id")
    employee_name = request.form.get("employee_name")
    gender = request.form.get("gender")
    birthday = request.form.get("birthday")
    phone = request.form.get("phone")
    email = request.form.get("email")
    address = request.form.get("address")
    position = request.form.get("position")
    salary = request.form.get("salary")
    employee = Employee(employee_id=employee_id, employee_name=employee_name, gender=gender, 
                        birthday=birthday, phone=phone, email=email, address=address, salary=salary, 
                        position=position)
    db.session.add(employee)
    db.session.commit()
    return redirect(url_for("showAllEmployee"))

#Đọc danh sách nhân viên
@app.route("/showAllEmployee")
def showAllEmployee():
    employees = Employee.query.all() 
    return render_template("show_all_employee.html", employees=employees)

#Xóa nhân viên
@app.route("/delete_employee/<int:employee_id>", methods=['GET', 'POST'])
def delete_employee(employee_id):
    employee = Employee.query.get(employee_id)
    
    if employee:
        db.session.delete(employee)
        db.session.commit()
        return redirect(url_for("showAllEmployee"))
    else:
        return "Nhân viên không tồn tại.", 404
    
#Sửa thông tin nhân viên
@app.route("/edit_employee/<int:employee_id>", methods=['GET', 'POST'])
def edit_employee(employee_id):
    employee = Employee.query.get(employee_id)
    
    if not employee:
        return "Nhân viên không tồn tại.", 404

    if request.method == 'POST':
        employee.employee_name = request.form.get("employee_name")
        employee.gender = request.form.get("gender")
        employee.birthday = request.form.get("birthday")
        employee.phone = request.form.get("phone")
        employee.email = request.form.get("email")
        employee.address = request.form.get("address")
        employee.position = request.form.get("position")
        employee.salary = request.form.get("salary")
        employee.password = request.form.get("password")

        db.session.commit()
        return redirect(url_for("showAllEmployee"))
    return render_template("edit_employee.html", employee=employee)


#Thêm thông tin kệ sách
@app.route("/addNewBookShelf", methods=['GET'])
def addNewBookShelf():
    return render_template("insert_new_book_shelf.html")

@app.route("/addNewBookShelfCommit", methods=['GET'])
def addNewBookShelfCommit():
    number = request.args.get("number")
    location = request.args.get("location")
    book_shelf = Book_Shelf(number=number, location=location)
    db.session.add(book_shelf)
    db.session.commit()
    return redirect(url_for("showAllBookShelf"))

#Đọc thông tin kệ sách
@app.route("/showAllBookShelf", methods=['GET'])
def showAllBookShelf():
    book_shelves = Book_Shelf.query.all()
    return render_template("show_all_book_shelf.html", book_shelves=book_shelves)   

#Sửa thông tin kệ sách
@app.route("/edit_book_shelf/<int:number>", methods=['GET', 'POST'])
def edit_book_shelf(number):
    # Tìm kệ sách theo số (number)
    book_shelf = Book_Shelf.query.get(number)
    
    if not book_shelf:
        return "Kệ sách không tồn tại.", 404

    if request.method == 'POST':
        book_shelf.location = request.form.get("location")

        db.session.commit()
        return redirect(url_for("showAllBookShelf"))

    return render_template("edit_book_shelf.html", book_shelf=book_shelf)

#Xóa thông tin kệ sách
@app.route("/delete_book_shelf/<int:number>", methods=['GET', 'POST'])
def delete_book_shelf(number):
    # Tìm kệ sách theo số (number)
    book_shelf = Book_Shelf.query.get(number)
    
    if not book_shelf:
        return "Kệ sách không tồn tại.", 404

    # Xóa kệ sách
    db.session.delete(book_shelf)
    db.session.commit()
    return redirect(url_for("showAllBookShelf"))

#Thêm thông tin thể loại sách
@app.route("/addNewKindOfBook", methods=['GET'])
def addNewKindOfBook():
    return render_template("insert_new_kind_of_book.html")

@app.route("/addNewKindOfBookCommit", methods=['POST'])
def addNewKindOfBookCommit():
    id = request.form.get("id")
    name = request.form.get("name")
    book_shelf_number = request.form.get("book_shelf_number")
    kind_of_book = Kind_of_Book(id=id, name=name, book_shelf_number=book_shelf_number)
    db.session.add(kind_of_book)
    db.session.commit()
    return redirect(url_for("showAllKindofBook"))

#Đọc thông tin thể loại sách
@app.route("/showAllKindofBook")
def showAllKindofBook():
    kind_of_books = Kind_of_Book.query.all()
    return render_template("show_all_Kind_of_book.html", kind_of_books=kind_of_books)

# Sửa thông tin thể loại sách
@app.route("/edit_kind_of_book/<int:id>", methods=['GET', 'POST'])
def edit_kind_of_book(id):
    kind_of_book = Kind_of_Book.query.get(id)  # Tìm thể loại sách theo ID
    
    if not kind_of_book:
        return "Thể loại sách không tồn tại.", 404

    if request.method == 'POST':
        # Lấy dữ liệu từ form
        kind_of_book.name = request.form.get("name")
        kind_of_book.book_shelf_number = request.form.get("book_shelf_number")

        # Lưu thay đổi vào cơ sở dữ liệu
        db.session.commit()
        return redirect(url_for("showAllKindofBook"))

    # Hiển thị form sửa thông tin thể loại sách
    return render_template("edit_kind_of_book.html", kind_of_book=kind_of_book)

#Xóa thể loại sách
@app.route("/delete_kind_of_book/<int:id>", methods=['GET', 'POST'])
def delete_kind_of_book(id):
    kind_of_book = Kind_of_Book.query.get(id)
    
    if kind_of_book:
        db.session.delete(kind_of_book)
        db.session.commit()
        return redirect(url_for("showAllKindofBook"))
    else:
        return "Sách không tồn tại.", 404


#Thêm thông tin sách
@app.route("/addNewBook", methods=['GET'])
def addNewBook():
    kinds_of_book = Kind_of_Book.query.all()
    return render_template("insert_new_book.html", kinds_of_book=kinds_of_book)

@app.route("/addNewBookCommit", methods=['POST'])
def addNewBookCommit():
    book_id = request.form.get("book_id")
    book_name = request.form.get("book_name")
    authors = request.form.get("authors")
    publishing_year = request.form.get("publishing_year")
    kind_of_book = request.form.get("kind_of_book")
    cost = request.form.get("cost")
    quantity = request.form.get("quantity")
    book = Book(book_id=book_id, book_name=book_name, authors=authors, 
                publishing_year=publishing_year, kind_of_book=kind_of_book, 
                cost=cost, quantity=quantity)
    db.session.add(book)
    db.session.commit()
    return redirect(url_for("showAllBook"))

#Đọc thông tin sách
@app.route("/showAllBook")
def showAllBook():
    # Truy vấn kết hợp giữa bảng Book và Kind_of_Book
    books = db.session.query(
        Book.book_id,
        Book.book_name,
        Book.authors,
        Book.publishing_year,
        Kind_of_Book.name.label("name"),  
        Book.cost,
        Book.quantity
    ).join(Kind_of_Book, Book.kind_of_book == Kind_of_Book.id).all() 

    return render_template("show_all_book.html", books=books)

#Xóa sách
@app.route("/delete_book/<int:book_id>", methods=['GET', 'POST'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    
    if book:
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for("showAllBook"))
    else:
        return "Sách không tồn tại.", 404
    
#Sửa thông tin sách
@app.route("/edit_book/<int:book_id>", methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get(book_id)
    kinds_of_book = Kind_of_Book.query.all()
    
    if not book:
        return "Sách không tồn tại.", 404

    if request.method == 'POST':
        book.book_name = request.form.get("book_name")
        book.authors = request.form.get("authors")
        book.publishing_year = request.form.get("publishing_year")
        book.kind_of_book = request.form.get("kind_of_book")
        book.cost = request.form.get("cost")
        book.quantity = request.form.get("quantity")

        db.session.commit()
        return redirect(url_for("showAllBook"))
    return render_template("edit_book.html", book=book, kinds_of_book=kinds_of_book)

#Tìm kiếm sách
@app.route("/search", methods=['GET'])
def search():
    query = request.args.get("q")  # Lấy tham số chuỗi tìm kiếm từ URL
    if query:
        books = Book.query.filter(
            (Book.book_name.ilike(f"%{query}%")) | 
            (Book.authors.ilike(f"%{query}%"))
        ).all()
        results = [
            {
                "book_id": book.book_id,
                "book_name": book.book_name,
                "authors": book.authors,
                "publishing_year": book.publishing_year,
                "kind_of_book": book.kind_of_book,
                "cost": book.cost,
                "quantity": book.quantity
            }
            for book in books
        ]
    else:
        results = [] 

    return jsonify(results)

#Số lượng sách bán ra
@app.route("/statistics_books_sold")
def statistics_books_sold():
    # Truy vấn tổng số lượng sách đã bán, nhóm theo book_id
    statistics = db.session.query(
        Book.book_id,
        Book.book_name,
        db.func.sum(Invoice_Details.quantity).label("total_quantity")
    ).join(Invoice_Details, Book.book_id == Invoice_Details.book_id) \
     .group_by(Book.book_id, Book.book_name) \
     .all()

    # Truyền dữ liệu thống kê vào template
    return render_template("statistics_books_sold.html", statistics=statistics)

#Thêm thông tin hóa đơn
@app.route("/addNewInvoice", methods=['GET'])
def addNewInvoice():
    customers = Customer.query.all() 
    employees = Employee.query.all()  
    return render_template("insert_new_invoice.html", customers=customers, employees=employees)

@app.route("/addNewInvoiceCommit", methods=['POST'])
def addNewInvoiceCommit():
    invoice_id = request.form.get("invoice_id")
    customer_id = request.form.get("customer_id")
    employee_id = request.form.get("employee_id")
    date_of_invoice = request.form.get("date_of_invoice")
    total_invoice = request.form.get("total_invoice")
    invoice = Invoice(invoice_id=invoice_id, customer_id=customer_id, employee_id=employee_id, 
                      date_of_invoice=date_of_invoice, total_invoice=total_invoice)
    db.session.add(invoice)
    db.session.commit()
    return redirect(url_for("showAllInvoice"))

#Đọc thông tin hóa đơn
@app.route("/showAllInvoice", methods=['GET'])
def showAllInvoice():
    # Truy vấn tất cả hóa đơn từ bảng Invoice
    invoices = db.session.query(
        Invoice.invoice_id,
        Invoice.date_of_invoice,
        Invoice.total_invoice,
        Customer.customer_name.label("customer_name"),
        Employee.employee_name.label("employee_name")
    ).join(Customer, Invoice.customer_id == Customer.customer_id) \
     .join(Employee, Invoice.employee_id == Employee.employee_id).all()

    # Truyền dữ liệu hóa đơn vào template
    return render_template("show_all_invoice.html", invoices=invoices)

#Sửa hóa đơn
@app.route("/edit_invoice/<int:invoice_id>", methods=['GET', 'POST'])
def edit_invoice(invoice_id):
    # Tìm hóa đơn theo ID
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        return "Hóa đơn không tồn tại.", 404

    if request.method == 'POST':
        # Lấy dữ liệu từ form
        invoice.customer_id = request.form.get("customer_id")
        invoice.employee_id = request.form.get("employee_id")
        invoice.date_of_invoice = request.form.get("date_of_invoice")
        invoice.total_invoice = request.form.get("total_invoice")

        # Lưu thay đổi vào cơ sở dữ liệu
        db.session.commit()
        return redirect(url_for("showAllInvoice"))

    # Lấy danh sách khách hàng và nhân viên để hiển thị trong form
    customers = Customer.query.all()
    employees = Employee.query.all()

    # Hiển thị form sửa hóa đơn
    return render_template("edit_invoice.html", invoice=invoice, customers=customers, employees=employees)

#Xóa thông tin hóa đơn
@app.route("/delete_invoice/<int:invoice_id>", methods=['GET', 'POST'])
def delete_invoice(invoice_id):
    # Tìm hóa đơn theo ID
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        return "Hóa đơn không tồn tại.", 404

    # Xóa hóa đơn
    db.session.delete(invoice)
    db.session.commit()
    return redirect(url_for("showAllInvoice"))

#Thêm thông tin chi tiết hóa đơn
@app.route("/addNewInvoiceDetails", methods=['GET'])
def addNewInvoiceDetails():
    invoices = Invoice.query.all()  # Lấy tất cả hóa đơn từ bảng Invoice
    books = Book.query.all()  # Lấy tất cả sách từ bảng Book
    customers = Customer.query.all()  # Lấy tất cả khách hàng từ bảng Customer
    return render_template("insert_new_invoice_detail.html", invoices=invoices, books=books, customers=customers)

@app.route("/addNewInvoiceDetailsCommit", methods=['POST'])
def addNewInvoiceDetailsCommit():
    invoice_id = request.form.get("invoice_id")
    book_id = request.form.get("book_id")
    quantity = int(request.form.get("quantity"))
    cost_book = float(request.form.get("cost_book"))

    if not book_id:
        return "Vui lòng chọn sách.", 400
    total_cost = quantity * cost_book
    invoice_detail = Invoice_Details(invoice_id=invoice_id, book_id=book_id, quantity=quantity, cost_book=cost_book)
    db.session.add(invoice_detail)
    invoice = Invoice.query.get(invoice_id)
    if invoice:
        invoice.total_invoice = (invoice.total_invoice or 0) + total_cost

    db.session.commit()
    return redirect(url_for("showAllInvoiceDetails"))

#Đọc chi tiết hóa đơn
@app.route("/showAllInvoiceDetails", methods=['GET'])
def showAllInvoiceDetails():
    # Truy vấn tất cả chi tiết hóa đơn từ bảng Invoice_Details
    invoice_details = db.session.query(
        Invoice_Details.invoice_id,
        Invoice_Details.book_id,  # Thêm book_id vào truy vấn
        Invoice_Details.quantity,
        Invoice_Details.cost_book,
        Book.book_name.label("book_name"),
        Customer.customer_name.label("customer_name")
    ).join(Invoice, Invoice_Details.invoice_id == Invoice.invoice_id) \
     .join(Book, Invoice_Details.book_id == Book.book_id) \
     .join(Customer, Invoice.customer_id == Customer.customer_id).all()

    # Truyền dữ liệu chi tiết hóa đơn vào template
    return render_template("show_all_invoice_details.html", invoice_details=invoice_details)

#Sửa chi tiết hóa đơn
@app.route("/edit_invoice_detail/<int:invoice_id>/<int:book_id>", methods=['GET', 'POST'])
def edit_invoice_detail(invoice_id, book_id):
    invoice_detail = Invoice_Details.query.filter_by(invoice_id=invoice_id, book_id=book_id).first()
    if not invoice_detail:
        return "Chi tiết hóa đơn không tồn tại.", 404

    if request.method == 'POST':
        invoice_detail.book_id = request.form.get("book_id")
        invoice_detail.quantity = request.form.get("quantity")
        invoice_detail.cost_book = request.form.get("cost_book")
        invoice_detail.total = float(invoice_detail.quantity) * float(invoice_detail.cost_book)

        db.session.commit()
        return redirect(url_for("showAllInvoiceDetails"))

    return render_template("edit_invoice_detail.html", invoice_detail=invoice_detail)

#Xóa thông tin chi tiết hóa đơn
@app.route("/delete_invoice_details", methods=['GET'])
def delete_invoice_details():
    invoice_id = request.args.get("invoice_id")
    book_id = request.args.get("book_id")

    # Tìm chi tiết hóa đơn dựa trên invoice_id và book_id
    invoice_detail = Invoice_Details.query.filter_by(invoice_id=invoice_id, book_id=book_id).first()
    if not invoice_detail:
        return "Chi tiết hóa đơn không tồn tại.", 404  

    db.session.delete(invoice_detail)
    db.session.commit()
    return redirect(url_for("showAllInvoiceDetails"))


if __name__ == '__main__':
    app.run(debug=True)
