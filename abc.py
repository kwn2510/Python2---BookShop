'''
#Thêm thông tin nhân viên
@app.route("/addNewEmployee")
def addNewEmployee():
    return render_template("insert_new_employee.html")

@app.route("/addNewEmployeeCommit")
def addNewEmployeeCommit():
    employee_id = request.args.get("employee_id")
    employee_name = request.args.get("employee_name")
    gender = request.args.get("gender")
    birthday = request.args.get("birthday")
    phone = request.args.get("phone")
    email = request.args.get("email")
    address = request.args.get("address")
    position = request.args.get("position")
    salary = request.args.get("salary")
    employee = Employee(employee_id=employee_id, employee_name=employee_name, gender=gender, birthday=birthday, phone=phone, email=email, address=address, salary=salary, position=position)
    db.session.add(employee)
    db.session.commit()
    return render_template("insert_new_employee_success.html")

#Thêm thông tin kệ sách
@app.route("/addNewBookShelf")
def addNewBookShelf():
    return render_template("insert_new_book_shelf.html")

@app.route("/addNewBookShelfCommit")
def addNewBookShelfCommit():
    number = request.args.get("number")
    location = request.args.get("location")
    book_shelf = Book_Shelf(number=number, location=location)
    db.session.add(book_shelf)
    db.session.commit()
    return render_template("insert_new_book_shelf_success.html")

#Thêm thông tin thể loại sách
@app.route("/addNewKindOfBook")
def addNewKindOfBook():
    return render_template("insert_new_kind_of_book.html")

@app.route("/addNewKindOfBookCommit")
def addNewKindOfBookCommit():
    id = request.args.get("id")
    name = request.args.get("name")
    book_shelf_number = request.args.get("book_shelf_number")
    kind_of_book = Kind_of_Book(id=id, name=name, book_shelf_number=book_shelf_number)
    db.session.add(kind_of_book)
    db.session.commit()
    return render_template("insert_new_kind_of_book_success.html")
#Thêm thông tin sách
@app.route("/addNewBook")
def addNewBook():
    return render_template("insert_new_book.html")

@app.route("/addNewBookCommit")
def addNewBookCommit():
    book_id = request.args.get("book_id")
    book_name = request.args.get("book_name")
    authors = request.args.get("authors")
    publishing_year = request.args.get("publishing_year")
    kind_of_book = request.args.get("kind_of_book")
    cost = request.args.get("cost")
    quantity = request.args.get("quantity")
    book = Book(book_id=book_id, book_name=book_name, authors=authors, publishing_year=publishing_year, kind_of_book=kind_of_book, cost=cost, quantity=quantity)
    db.session.add(book)
    db.session.commit()
    return render_template("insert_new_book_success.html")

#Thêm thông tin hóa đơn
@app.route("/addNewInvoice")
def addNewInvoice():
    return render_template("insert_new_invoice.html")

@app.route("/addNewInvoiceCommit")
def addNewInvoiceCommit():
    invoice_id = request.args.get("invoice_id")
    customer_id = request.args.get("customer_id")
    employee_id = request.args.get("employee_id")
    date_of_invoice = request.args.get("date_of_invoice")
    total_invoice = request.args.get("total_invoice")
    invoice = Invoice(invoice_id=invoice_id, customer_id=customer_id, employee_id=employee_id, date_of_invoice=date_of_invoice, total_invoice=total_invoice)
    db.session.add(invoice)
    db.session.commit()
    return render_template("insert_new_invoice_success.html")

#Thêm thông tin chi tiết hóa đơn
@app.route("/addNewInvoiceDetails")
def addNewInvoiceDetails():
    return render_template("insert_new_invoice_detail.html")

@app.route("/addNewInvoiceDetailsCommit")
def addNewInvoiceDetailsCommit():
    invoice_id = request.args.get("invoice_id")
    book_id = request.args.get("book_id")
    quantity = request.args.get("quantity")
    cost_book = request.args.get("cost_book")
    total = request.args.get("total")
    customer_id = request.args.get("customer_id")
    invoice_detail = Invoice_Details(invoice_id=invoice_id, book_id=book_id, quantity=quantity, cost_book=cost_book, total=total, customer_id=customer_id)
    db.session.add(invoice_detail)
    db.session.commit()
    return render_template("insert_new_invoice_details_success.html")

#Đọc dữ liệu
@app.route("/show_All_Customer")
def showAllCustomer():
    customers = Customer.query.all()
    return render_template("show_all_customer.html", customers=customers)

#Đọc thông tin nhân viên
@app.route("/show_All_Employee")
def showAllEmployee():
    employees = Employee.query.all()
    return render_template("show_all_employee.html", employees=employees)

#Đọc thông tin kệ sách
@app.route("/show_All_BookShelf")
def showAllBookShelf():
    book_shelfs = Book_Shelf.query.all()
    return render_template("show_all_book_shelf.html", book_shelfs=book_shelfs)

#Đọc thông tin thể loại sách
@app.route("/show_All_Kind_of_book")
def show_All_Kind_of_book():
    kind_of_books = Kind_of_Book.query.all()
    return render_template("show_all_Kind_of_book.html", kind_of_books=kind_of_books)

#Đọc thông tin sách
@app.route("/show_All_Book")
def showAllBook():
    books = Book.query.all()
    return render_template("show_all_book.html", books=books)

#Đọc thông tin hóa đơn
@app.route("/show_All_Invoice")
def show_All_Invoice():
    invoices = Invoice.query.all()
    return render_template("show_all_invoice.html", invoices=invoices)

#Đọc thông tin chi tiết hóa đơn
@app.route("/show_All_Invoice_Details")
def show_All_Invoice_Details():
    invoice_details = Invoice_Details.query.all()
    return render_template("show_all_invoice_details.html", invoice_details=invoice_details)

#Tìm kiếm dữ liệu
#Tìm kiếm thông tin khách hàng
@app.route("/find_customer")
def find_customer():
    return render_template("find_customer.html")

@app.route("/find_customer_result")
def find_customer_result():
    customer_id = int(request.args.get("customer_id"))
    customer = Customer.query.get(customer_id)
    return render_template("find_customer_result.html",customer=customer)

#Tìm kiếm thông tin nhân viên
@app.route("/find_employee")
def find_employee():
    return render_template("find_employee.html")

@app.route("/find_employee_result")
def find_employee_result():
    employee_id = int(request.args.get("employee_id"))
    employee = Employee.query.get(employee_id)
    return render_template("find_employee_result.html",employee=employee)

#Tìm kiếm thông tin kệ sách
@app.route("/find_book_shelf")
def find_book_shelf():
    return render_template("find_book_shelf.html")

@app.route("/find_book_shelf_result")
def find_employee_result():
    number = request.args.get("number")
    book_shelfs = Book_Shelf.query.get(number)
    return render_template("find_book_shelf_result.html",book_shelfs=book_shelfs)

#Tìm kiếm thông tin kệ thể loại sách
@app.route("/find_Kind_of_book")
def find_Kind_of_book():
    return render_template("find_Kind_of_book.html")

@app.route("/find_Kind_of_book_result")
def find_Kind_of_book_result():
    ID = request.args.get("id")
    kind_of_book = Kind_of_Book.query.get(ID)
    return render_template("find_Kind_of_book_result.html",kind_of_book=kind_of_book)

#Tìm kiếm thông tin sách
@app.route("/find_book")
def find_book():
    return render_template("find_book.html")

@app.route("/find_book_result")
def find_book_result():
    book_id = request.args.get("book_id")
    book = Book.query.get(book_id)
    return render_template("find_book_result.html",book=book)

#Tìm kiếm thông tin hóa đơn
@app.route("/find_invoice")
def find_invoice():
    return render_template("find_invoice.html")

@app.route("/find_invoice_result")
def find_invoice_result():
    invoice_id = request.args.get("invoice_id")
    invoice = Invoice.query.get(invoice_id)
    return render_template("find_invoice_result.html",invoice=invoice)

#Tìm kiếm thông tin chi tiết hóa đơn
@app.route("/find_invoice_details")
def find_invoice_details():
    return render_template("find_invoice_details.html")

@app.route("/find_invoice_details_result")
def find_invoice_details_result():
    invoice_id = int(request.args.get("invoice_id"))
    invoice_details = Invoice_Details.query.get(invoice_id)
    return render_template("find_invoice_details_result.html",invoice_details=invoice_details)


#Sửa dữ liệu
#Sửa thông tin khách hàng
@app.route("/infoCustomer")
def infoCustomer():
    customers = Customer.query.all()
    return render_template("update_customer.html", customers=customers)

@app.route("/update_customer_commit")
def update_customer_commit():
    customer_id = request.args.get("customer_id")
    customer = Customer.query.get(customer_id)
    customer.customer_name = request.args.get("customer_name")
    customer.address = request.args.get("address")
    customer.phone = request.args.get("phone")
    customer.email = request.args.get("email")
    db.session.commit()
    return render_template("update_customer_success.html")

#Sửa thông tin nhân viên
@app.route("/infoEmployee")
def infoEmployee():
    employees =  Employee.query.all()
    return render_template("update_employee.html", employees=employees)

@app.route("/update_employee_commit")
def update_employee_commit():
    employee_id = request.args.get("employee_id")
    employee = Employee.query.get(employee_id)
    employee.employee_name = request.args.get("employee_name")
    employee.gender = request.args.get("gender")
    employee.birthday = request.args.get("birthday")
    employee.phone = request.args.get("phone")
    employee.email = request.args.get("email")
    employee.address = request.args.get("address")
    employee.position = request.args.get("position")
    employee.salary = request.args.get("salary")
    db.session.commit()
    return render_template("update_employee_success.html")

#Sửa thông tin kệ sách
@app.route("/infoBookShelf")
def infoBookShelf():
    book_shelfs =  Book_Shelf.query.all()
    return render_template("update_bookshelf.html", book_shelfs=book_shelfs)

@app.route("/update_bookshelf_commit")
def update_bookshelf_commit():
    number = request.args.get("number")
    book_shelf = Book_Shelf.query.get(number)
    book_shelf.location = request.args.get("location")
    db.session.commit()
    return render_template("update_bookshelf_success.html")

#Sửa thông tin thể loại sách
@app.route("/info_Kind_of_book")
def info_Kind_of_book():
    kind_of_books =  Kind_of_Book.query.all()
    return render_template("update_bookshelf.html", kind_of_books=kind_of_books)

@app.route("/update_Kind_of_book_commit")
def update_Kind_of_book_commit():
    ID = request.args.get("id")
    kind_of_books = Kind_of_Book.query.get(ID)
    kind_of_books.name = request.args.get("name")
    db.session.commit()
    return render_template("update_Kind_of_book_success.html")
    
#Sửa thông tin sách
@app.route("/infoBook")
def infoBook():
    books =  Book.query.all()
    return render_template("update_book.html", books=books)

@app.route("/update_book_commit")
def update_book_commit():
    book_id = request.args.get("book_id")
    book = Book.query.get(book_id)
    book.name = request.args.get("book_name")
    book.authors = request.args.get("authors")
    book.publishing_year = request.args.get("publishing_year")
    book.kind_of_book = request.args.get("kind_of_book")
    book.cost = request.args.get("cost")
    book.quantity = request.args.get("quantity")
    db.session.commit()
    return render_template("update_book_success.html")

#Sửa thông tin hóa đơn
@app.route("/infoInvoice")
def infoInvoice():
    invoices = Invoice.query.all()
    return render_template("update_invoice.html", invoices=invoices)

@app.route("/update_invoice_commit")
def update_invoice_commit():
    invoice_id = request.args.get("invoice_id")
    invoice = Invoice.args.get(invoice_id)
    invoice.customer_id = request.args.get("customer_id")
    invoice.employee_id = request.args.get("employee_id")
    invoice.date_of_invoice = request.args.get("date_of_invoice")
    invoice.total_invoice = request.args.get("total_invoice")
    db.session.commit()
    return render_template("update_invoice_success.html")

#Sửa thông tin chi tiết hóa đơn
@app.route("/infoInvoiceDetails")
def infoInvoiceDetails():
    invoices_details = Invoice_Details.query.all()
    return render_template("update_invoice_details.html", invoices_details=invoices_details)

@app.route("/update_invoice_details_commit")
def update_invoice_details_commit():
    invoice_id = request.args.get("invoice_id")
    book_id = request.args.get("book_id")
    new_book_id = request.args.get("new_book_id") #thêm dòng này để lấy giá trị book_id mới
    invoice_detail = Invoice_Details.query.get(invoice_id, book_id)
    invoice_detail.book_id = new_book_id #sử dụng book_id mới để cập nhật
    invoice_detail.quantity = request.args.get("quantity")
    invoice_detail.cost_book = request.args.get("cost_book")
    invoice_detail.customer_id = request.args.get("customer_id")
    db.session.commit()
    return render_template("update_invoice_details_success.html")
    

#//Xóa thông tin kệ sách//
@app.route("/in_fo_BookShelf")
def in_fo_BookShelf():
    return render_template("delete_bookshelf.html",book_shelfs=book_shelfs)

@app.route("/delete_bookshelf")
def delete_bookshelf():
    number = request.args.get("number")
    book_shelf = Book_Shelf.query.get(number)
    db.session.delete(book_shelf)
    db.session.commit()
    return render_template("delete_bookshelf_success.html")

#//Xóa thông tin thể loại sách//
@app.route("/in_fo_Kind_of_book")
def in_fo_Kind_of_book():
    return render_template("delete_Kind_of_book.html",kind_of_books=kind_of_books)

@app.route("/delete_Kind_of_book")
def delete_Kind_of_book():
    ID = request.args.get("id")
    kind_of_book = Kind_of_Book.query.get(ID)
    db.session.delete(kind_of_book)
    db.session.commit()
    return render_template("delete_Kind_of_book_success.html")

#//Xóa thông tin sách//
@app.route("/in_fo_Book")
def in_fo_Book():
    return render_template("delete_book.html",books=books)

@app.route("/delete_book")
def delete_book():
    book_id = request.args.get("book_id")
    book = Book.query.get(book_id)
    db.session.delete(book)
    db.session.commit()
    return render_template("delete_book_success.html")

#//Xóa thông tin hóa đơn//
@app.route("/in_fo_Invoice")
def in_fo_Invoice():
    return render_template("delete_invoice.html",invoices=invoices)

@app.route("/delete_invoice")
def delete_invoice():
    invoice_id = request.args.get("invoice_id")
    invoice = Invoice.query.get(invoice_id)
    db.session.delete(invoice)
    db.session.commit()
    return render_template("delete_invoice_success.html")

#//Xóa thông tin chi tiết hóa đơn//
@app.route("/in_fo_Invoice_Details")
def in_fo_Invoice_Details():
    return render_template("delete_invoice_details.html",invoice_details=invoice_details)

@app.route("/delete_invoice_details")
def delete_invoice_details():
    invoice_id = request.args.get("invoice_id")
    book_id = request.args.get("book_id")
    invoice_detail = Invoice_Details.query.get((invoice_id, book_id))
    db.session.delete(invoice_detail)
    db.session.commit()
    return render_template("delete_invoice_details_success.html")
    '''