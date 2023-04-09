from flask import Blueprint, redirect, render_template, request, flash, url_for
from sql.db import DB
employee = Blueprint('employee', __name__, url_prefix='/employee')


@employee.route("/search", methods=["GET"])
def search():
    rows = []
    # DO NOT DELETE PROVIDED COMMENTS
    # TODO search-1 retrieve employee id as id, first_name, last_name, email, company_id, company_name using a LEFT JOIN
    query = """SELECT employee.id as "id", first_name, last_name, email, company_id, company_name
    FROM employee LEFT JOIN company
    ON employee.company_id = company.id
    WHERE 1=1"""
    args = {} # <--- add values to replace %s/%(named)s placeholders
    allowed_columns = ["first_name", "last_name", "email", "company_name"]
    # TODO search-2 get fn, ln, email, company, column, order, limit from request args
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    email = request.args.get('email')
    company_name = request.args.get('company_name')
    column = request.args('column')
    order = request.args.get('order')
    limit = request.args.get('limit',default=10, type = int)
    # TODO search-3 append like filter for first_name if provided
    if first_name:
        query += f" AND first_name LIKE '%{first_name}%"
    # TODO search-4 append like filter for last_name if provided
    if last_name:
        query += f" AND last_name LIKE '%{last_name}%"
    # TODO search-5 append like filter for email if provided
    if email:
        query += f" AND email LIKE '%{email}%"
    # TODO search-6 append equality filter for company_id if provided
    if company_name:
        query += f" AND company_name LIKE '%{company_name}%"
    # TODO search-7 append sorting if column and order are provided and within the allowed columns and order options (asc, desc)
    if column in allowed_columns and order in ['asc','desc']:
        query += f" ORDER BY {column} {order}"
    # TODO search-8 append limit (default 10) or limit greater than 1 and less than or equal to 100
    try:
        if limit >= 100 or limit < 1:
            flash("Invalid Limit. Limit must be between 1 and 100","error")
            query += " LIMIT %(limit)s"
            args["limit"] = limit
            print("query",query)
            print("args", args)
    # TODO search-9 provide a proper error message if limit isn't a number or if it's out of bounds
    except ValueError:
        flash("Limit must be an integer","error")
    
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
    options =[]
    for col in allowed_columns:
        label = col.replace("_", " ").title()
        options.append((col,label))
    # do this prior to passing to render_template, but not before otherwise it can break validation

    return render_template("list_employees.html", rows=rows, allowed_columns=allowed_columns)

@employee.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        # TODO add-1 retrieve form data for first_name, last_name, company, email
        # TODO add-2 first_name is required (flash proper error message)
        # TODO add-3 last_name is required (flash proper error message)
        # TODO add-4 company (may be None)
        # TODO add-5 email is required (flash proper error message)
        # TODO add-5a verify email is in the correct format
        has_error = False # use this to control whether or not an insert occurs
            
        if not has_error:
            try:
                result = DB.insertOne("""
                INSERT INTO ...
                """, ...
                ) # <-- TODO add-6 add query and add arguments
                if result.status:
                    flash("Created Employee Record", "success")
            except Exception as e:
                # TODO add-7 make message user friendly
                flash(str(e), "danger")
    return render_template("add_employee.html")

@employee.route("/edit", methods=["GET", "POST"])
def edit():
    # TODO edit-1 request args id is required (flash proper error message)
    id = False
    if not id: # TODO update this for TODO edit-1
        pass
    else:
        if request.method == "POST":
            
            # TODO edit-1 retrieve form data for first_name, last_name, company, email
            # TODO edit-2 first_name is required (flash proper error message)
            # TODO edit-3 last_name is required (flash proper error message)
            # TODO edit-4 company (may be None)
            # TODO edit-5 email is required (flash proper error message)
            # TODO edit-5a verify email is in the correct format
            has_error = False # use this to control whether or not an insert occurs

            
                
            if not has_error:
                try:
                    # TODO edit-6 fill in proper update query
                    result = DB.update("""
                    UPDATE ... SET
                    ...
                    """, ...)
                    if result.status:
                        flash("Updated record", "success")
                except Exception as e:
                    # TODO edit-7 make this user-friendly
                    flash(e, "danger")
        row = {}
        try:
            # TODO edit-8 fetch the updated data 
            result = DB.selectOne("""SELECT 
            ...
            FROM ... LEFT JOIN ... 
            WHERE ..."""
            , id)
            if result.status:
                row = result.row
        except Exception as e:
            # TODO edit-9 make this user-friendly
            flash(str(e), "danger")
    # TODO edit-10 pass the employee data to the render template
    return render_template("edit_employee.html", ...)

@employee.route("/delete", methods=["GET"])
def delete():
    # TODO delete-1 delete employee by id
    # TODO delete-2 redirect to employee search
    # TODO delete-3 pass all argument except id to this route
    # TODO delete-4 ensure a flash message shows for successful delete
    # TODO delete-5 if id is missing, flash necessary message and redirect to search
    pass