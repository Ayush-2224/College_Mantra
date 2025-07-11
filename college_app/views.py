from django.shortcuts import render
from django.http import HttpResponse
from django.db import transaction, connection
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import College  # Import College model
from django.contrib.auth.models import User
from django.urls import reverse



def is_college(user):
    return College.objects.filter(College_ID=user.username).exists()

# Custom decorator to ensure the user is a College member
def college_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not is_college(request.user):
            messages.error(request, "You must be a college member to access this page.")
            return redirect("college_app:college_login")  # Redirect to college login page
        return view_func(request, *args, **kwargs)
    return _wrapped_view
# College login view
def college_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("college_app:college_home")  # Redirect after successful login
           
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'colleges/login.html')

    return render(request, 'colleges/login.html')  # Render login page


# College signup view
def college_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            try:
                # Start the transaction block
                with transaction.atomic():
                    # Create the User instance
                    user = User.objects.create_user(username=username, password=password)
                    user.save()

                    # Additional operations for college can be added here (e.g., creating a College model)
                    # Example: Create a College instance
                    # college = College(username=user, college_name="College Name", ...)
                    # college.save()

                    # If everything goes well, commit the transaction
                    messages.success(request, "College registered successfully!")
                    return redirect('college_app:college_login')  # Redirect to login page after registration
                
            except Exception as e:
                # If an error occurs, the transaction will be rolled back
                messages.error(request, f"An error occurred: {e}")
                return redirect('college_app:college_signup')  # Stay on the signup page

        else:
            messages.error(request, "Passwords do not match.")

    return render(request, 'colleges/signup.html')

# College logout view
def college_logout(request):
    logout(request)
    return redirect("cm_app:home")


@login_required(login_url='college_app:college_login')  # Ensures the user is logged in before accessing this page
def college_register(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():  # Start a transaction block to ensure atomicity

                # Retrieve the data from the registration form
                college_id = request.user.username  # Using the username as the college_id
                college_name = request.POST.get('college_name')
                college_type = request.POST.get('college_type')
                contact_no = request.POST.get('contact_no')
                email = request.POST.get('email')
                location = request.POST.get('location')
                website = request.POST.get('website')

                # Validate required fields (you can add more validations here as needed)
                if not college_name or not college_type or not contact_no or not email:
                    raise ValueError("All fields are required!")

                # Create and save the College instance
                college = College(
                    College_ID=college_id,  # Using the logged-in user's username as the college ID
                    College_Name=college_name,
                    College_Type=college_type,
                    Contact_No=contact_no,
                    Email=email,
                    Location=location,
                    Website=website
                )
                college.save()

                # If everything goes well, show a success message
                messages.success(request, "College registered successfully!")
                return redirect('college_app:college_home')  # Redirect to the college home page after successful registration

        except Exception as e:
            # If any error occurs, the transaction will be rolled back
            messages.error(request, f"An error occurred during registration: {e}")
            return redirect('college_app:college_register')  # Redirect back to the registration page on error

    # If the method is GET, render the registration form
    return render(request, 'colleges/register.html')


# Function to fetch the college list
# @college_required
# def get_college_list():
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT * FROM College")  # Adjust table name to match your model table
#         results = cursor.fetchall()
#     return results


# Function to fetch the preference list
# def get_preference_list():
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT * FROM preference")
#         results = cursor.fetchall()
#     return results


# Function to fetch the course list

# def get_course_list():
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT * FROM Course")
#         results = cursor.fetchall()
#     return results


# # View to display college list
# def college_list(request):
#     # Fetch college, preference, and course lists
#     colleges = get_college_list()
#     preferences = get_preference_list()
#     courses = get_course_list()

#     return render(request, 'colleges/college_list.html', {
#         'colleges': colleges,
#         'preference': preferences,
#         'courses': courses
#     })

# Home page for colleges
def college_home(request):
    return render(request, 'colleges/home.html')
@login_required(login_url='college_app:college_login') 
@college_required
def college_courses(request):
    college_id=request.user.username
    # SQL query to fetch seat matrix for a specific college
    query = """
        SELECT 
            c.College_Name,
            co.Branch_Name,
            co.Program_Name,
            sm.General,
            sm.General_PwD,
            sm.OBC_NCL,
            sm.OBC_NCL_PwD,
            sm.SC,
            sm.SC_PwD,
            sm.ST,
            sm.ST_PwD,
            sm.Total_Seats,
            sm.Allocated_Seats
        FROM 
            Seat_Matrix sm
        JOIN 
            College_Course cc ON sm.College_ID = cc.College_ID AND sm.Course_ID = cc.Course_ID
        JOIN 
            College c ON cc.College_ID = c.College_ID
        JOIN 
            Course co ON cc.Course_ID = co.Course_ID
        WHERE 
            c.College_ID = %s;
    """

    # Execute the query and fetch data
    with connection.cursor() as cursor:
        cursor.execute(query, [college_id])
        rows = cursor.fetchall()

    # Create a list of dictionaries to hold the data
    college_courses = [
        {
            'college_name': row[0],
            'branch_name': row[1],
            'program_name': row[2],
            'general': row[3],
            'general_pwd': row[4],
            'obc_ncl': row[5],
            'obc_ncl_pwd': row[6],
            'sc': row[7],
            'sc_pwd': row[8],
            'st': row[9],
            'st_pwd': row[10],
            'total_seats': row[11],
            'allocated_seats': row[12],
        }
        for row in rows
    ]

    # Render the template with the data
    return render(request, "colleges/college_courses.html", {
        "college_courses": college_courses,
        "college_id": college_id,
    })
@login_required(login_url='college_app:college_login')
@college_required 
def show_college_allocation(request):
    college_id = request.user.username  # Assuming the username is the College_ID

    with connection.cursor() as cursor:
        query = '''
        SELECT 
            c.Candidate_Name, 
            c.Gender, 
            c.DOB, 
            c.Candidate_Rank, 
            c.XII_Percentage, 
            c.Category, 
            c.Nationality, 
            c.Address, 
            c.Email, 
            c.Phone, 
            co.College_Name, 
            co.College_Type, 
            co.Location, 
            cu.Branch_Name, 
            cu.Program_Name, 
            a.Allocation_ID, 
            a.Payment_Status
        FROM col_allo ca
        JOIN College co ON ca.College_ID = co.College_ID
        JOIN Course cu ON ca.Course_ID = cu.Course_ID
        JOIN Allocation a ON ca.Allocation_ID = a.Allocation_ID
        JOIN can_alloc ca2 ON a.Allocation_ID = ca2.Allocation_ID
        JOIN Candidate c ON ca2.username = c.username
        WHERE co.College_ID = %s;
        '''
        cursor.execute(query, [college_id])  # Pass the college_id as parameter to filter
        rows = cursor.fetchall()  # Fetch all rows for the specified college

    context = {'students': rows}  # Pass the student data to the template
    return render(request, 'colleges/college_allocation.html', context)


# views.py
def update_seats(request):
    # Get the college_id from the logged-in user's username
    username = request.user.username
    college_id = username  # Create a function to get college_id from username

    # Fetch current seat data for all courses of the given college
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT cc.Course_ID, c.Branch_Name, sm.General, sm.General_PwD, sm.OBC_NCL, sm.OBC_NCL_PwD, 
                   sm.SC, sm.SC_PwD, sm.ST, sm.ST_PwD, sm.Total_Seats, sm.Allocated_Seats
            FROM College_Course cc
            JOIN Course c ON cc.Course_ID = c.Course_ID
            JOIN Seat_Matrix sm ON cc.College_ID = sm.College_ID AND cc.Course_ID = sm.Course_ID
            WHERE cc.College_ID = %s
        """, [college_id])
        courses = cursor.fetchall()
         
        print(courses)
    if request.method == 'POST':
        # If POST request, update the seat numbers
        for course in courses:
            course_id = course[0]
            # Assuming the form will send updated seat data like 'general', 'obc', etc.
            general_seat = request.POST.get(f'general_{course_id}')
            general_pwd_seat = request.POST.get(f'general_pwd_{course_id}')
            obc_seat = request.POST.get(f'obc_{course_id}')
            obc_pwd_seat = request.POST.get(f'obc_pwd_{course_id}')
            sc_seat = request.POST.get(f'sc_{course_id}')
            sc_pwd_seat = request.POST.get(f'sc_pwd_{course_id}')
            st_seat = request.POST.get(f'st_{course_id}')
            st_pwd_seat = request.POST.get(f'st_pwd_{course_id}')
            total_seat = request.POST.get(f'total_{course_id}')
            
            # Update the seat values
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE Seat_Matrix
                    SET General = %s, General_PwD = %s, OBC_NCL = %s, OBC_NCL_PwD = %s, 
                        SC = %s, SC_PwD = %s, ST = %s, ST_PwD = %s, Total_Seats = %s
                    WHERE College_ID = %s AND Course_ID = %s
                """, [general_seat, general_pwd_seat, obc_seat, obc_pwd_seat, sc_seat, sc_pwd_seat, 
                      st_seat, st_pwd_seat, total_seat, college_id, course_id])
        
        return redirect(reverse('college_app:update_seats'))  # Redirect after updating the seats (you can define your success URL)

    # Render a template that shows current seat data and form for updating
    return render(request, 'colleges/update_seats.html', {'courses': courses})
