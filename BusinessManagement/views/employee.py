from flask import Blueprint, redirect, render_template, request, flash, url_for
from sql.db import DB
employee = Blueprint('employee', __name__, url_prefix='/employee')


@employee.route("/search", methods=["GET"])
def search():
    rows = []
    order_options = ['asc','desc']
    # DO NOT DELETE PROVIDED COMMENTS
    # TODO search-1 retrieve employee id as id, first_name, last_name, email, company_id, company_name using a LEFT JOIN
    query = "SELECT employee.id as 'id', employee.first_name, employee.last_name, employee.email, employee.company_id, employee.company_name FROM IS601_MP3_Employees employee LEFT JOIN IS601_MP3_Companies companies ON employee.company_id = companies.id WHERE 1=1"
    args = {} # <--- add values to replace %s/%(named)s placeholders
    allowed_columns = ["first_name", "last_name", "email", "company_name"]
    # TODO search-2 get fn, ln, email, company, column, order, limit from request args
    first_name = request.args.get('fn')
    last_name = request.args.get('ln')
    email = request.args.get('email')
    company = request.args.get('company')
    column = request.args.get("column")
    order = request.args.get('order')
    limit = request.args.get('limit',default=10, type = int)
    '''
    UCID: mm2836, Date Implemented: 04/07/23
    '''
    # TODO search-3 append like filter for first_name if provided
    if first_name:
        query += " AND employee.first_name LIKE %(first_name)s"
        args["first_name"] = f"%{first_name}%"
    # TODO search-4 append like filter for last_name if provided
    if last_name:
        query += " AND employee.last_name LIKE %(last_name)s"
        args["last_name"] = f"%{last_name}%"
    # TODO search-5 append like filter for email if provided
    if email:
        query += " AND employee.email LIKE %(email)s"
        args["email"] = f"%{email}%"
    # TODO search-6 append equality filter for company_id if provided
    if company:
        query += " AND employee.company_id = {company}"
        args["company"] = f"%{company}%"
    # TODO search-7 append sorting if column and order are provided and within the allowed columns and order options (asc, desc)
    if column and order:
        if column in allowed_columns and order in ['asc','desc']:
            query += f" ORDER BY {column} {order}"
    '''
    UCID: mm2836, Date Implemented: 04/07/23
    '''
    # TODO search-8 append limit (default 10) or limit greater than 1 and less than or equal to 100
    try:
        limit = int(limit)
        if limit > 100 or limit < 1:
            flash("Invalid Limit. Limit must be between 1 and 100","error")
        else:
            query += " LIMIT %(limit)s"
            args["limit"] = int(limit)
    # TODO search-9 provide a proper error message if limit isn't a number or if it's out of bounds
    except ValueError:
        flash("Limit must be an integer","error")
    print("query",query)
    print("args", args)
    try:
        result = DB.selectAll(query, args)
        if result.status:
            rows = result.rows
    except Exception as e:
        # TODO search-10 make message user friendly
        flash("An error occurred. Please try again.", "error")
        print("The error occurred while searching for employees: {e}")
    
    # hint: use allowed_columns in template to generate sort dropdown
    # hint2: convert allowed_columns into a list of tuples representing (value, label)
    allowed_columns_list = [(value, value) for value in allowed_columns]
    # do this prior to passing to render_template, but not before otherwise it can break validation
    return render_template("list_employees.html", rows=rows, allowed_columns=allowed_columns_list)
    '''
    UCID: mm2836, Date Implemented: 04/07/23
    '''


@employee.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        # TODO add-1 retrieve form data for first_name, last_name, company, email
        first_name = str(request.form.get("first_name"))
        last_name = str(request.form.get("last_name"))
        company = str(request.form.get("company"))
        email = str(request.form.get("email"))

        has_error = False # use this to control whether or not an insert occurs
        # TODO add-2 first_name is required (flash proper error message)
        if not first_name:
            flash("First name is required","error")
            has_error = True
        # TODO add-3 last_name is required (flash proper error message)
        if not last_name:
            flash("Last name is required","error")
            has_error = True
        # TODO add-4 company (may be None)
        if not company:
            company = None
        # TODO add-5 email is required (flash proper error message)
        if not email:
            flash("Email is required","error")
            has_error = True
        # TODO add-5a verify email is in the correct format
        if "@" not in email or "." not in email:
            flash("Email not in valid format.","error")
            has_error = True

        if not has_error:
            try:
                result = DB.insertOne("""
                INSERT INTO IS601_MP3_Employees (first_name, last_name, company, email)
                VALUES (%s, %s, %s, %s)
                """, (first_name, last_name, company, email)
                ) # <-- TODO add-6 add query and add arguments
                if result.status:
                    flash("Created Employee Record", "success")
            except Exception as e:
                # TODO add-7 make message user friendly
                flash("An error occurred while creating employee", "danger")
    return render_template("add_employee.html")
    '''
    UCID: mm2836, Date Implemented: 04/07/23
    '''
@employee.route("/edit", methods=["GET", "POST"])
def edit():
    # TODO edit-1 request args id is required (flash proper error message)
    id = False
    if not request.args.get('id'): # TODO update this for TODO edit-1
        flash("Employee ID is required.", "error")
    else:
        if request.method == "POST":
            
            # TODO edit-1 retrieve form data for first_name, last_name, company, email
            first_name = str(request.form.get('first_name'))
            last_name = str(request.form.get('last_name'))
            company = str(request.form.get('company'))
            email = str(request.form.get('email'))
            has_error = False # use this to control whether or not an insert occurs
            # TODO add-2 first_name is required (flash proper error message)
            if not first_name:
                flash("First name is required","error")
                has_error = True
            # TODO add-3 last_name is required (flash proper error message)
            if not last_name:
                flash("Last name is required","error")
                has_error = True
            # TODO add-4 company (may be None)
            if not company:
                company = None
            # TODO add-5 email is required (flash proper error message)
            if not email:
                flash("Email is required","error")
                has_error = True
            # TODO add-5a verify email is in the correct format
            if "@" not in email or "." not in email:
                flash("Email not in valid format.","error")
                has_error = True
            '''
            UCID: mm2836, Date Implemented: 04/07/23
            '''
            if not has_error:
                try:
                    # TODO edit-6 fill in proper update query
                    result = DB.update("""
                    UPDATE IS601_MP3_Employees SET
                    first_name=%s,
                    last_name=%s,
                    company=%s,
                    email=%s
                    WHERE id = %s
                    """, (first_name, last_name, company, email,id))
                    if result.status:
                        flash("Updated record", "success")
                except Exception as e:
                    # TODO edit-7 make this user-friendly
                    flash(f"Error updating record {e}.", "danger")
        row = {}
        try:
            # TODO edit-8 fetch the updated data 
            result = DB.selectOne("""SELECT 
            employee.first_name,
            employee.last_name,
            employee.company_name,
            employee.email
            FROM IS601_MP3_Employees employee LEFT JOIN IS601_MP3_Companies companies ON employee.company_id = companies.id
            WHERE employee.id = %s"""
            , id)
            if result.status:
                row = result.row
        except Exception as e:
            # TODO edit-9 make this user-friendly
            flash(f"Error fetching data: {str(e)}.", "danger")
    # TODO edit-10 pass the employee data to the render template
    return render_template("edit_employee.html", row = row)
    '''
    UCID: mm2836 Date Implemented: 04/07/23
    '''
@employee.route("/delete", methods=["GET"])
def delete():
    # TODO delete-5 if id is missing, flash necessary message and redirect to search
    if not request.args.get("id"):
        flash("Employee ID is required.", "danger")
        return redirect(url_for("employee.search"))
    else:
    # TODO delete-1 delete employee by id
        result = DB.delete("""DELETE FROM employees WHERE id = %s""", id)
        if result.status:
            # TODO delete-4 ensure a flash message shows for successful delete
            flash("Employee record has been deleted.", "success")
    # TODO delete-3 pass all argument except id to this route
    args = request.args.copy()
    args.pop("id")
    # TODO delete-2 redirect to employee search
    return redirect(url_for("employee.search", **args))
    pass
'''
UCID: mm2836, Date Implemented: 04/07/23
'''
    