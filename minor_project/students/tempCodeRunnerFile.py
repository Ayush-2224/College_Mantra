import MySQLdb
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student, College
from django.contrib.auth.decorators import login_required
from django.db import connection

def allocate_colleges():
    # Establish the database connection
    db = MySQLdb.connect(
        host="localhost",
        user="root",
        password="Ayush2224@",
        db="dbis",
    )
    
    cursor = db.cursor()
    
    try:
        # Start a transaction
        db.begin()  # Use `db.begin()` for MySQLdb to begin a transaction
        
        allocation_id = 100000  # Starting allocation_id
        
        # Step 1: Sort students by rank
        cursor.execute("SELECT username FROM students_student ORDER BY rank ASC")
        students = cursor.fetchall()

        for student in students:
            username = student[0]
            allocation_made = False  # Track if an allocation is made for the student
            
            # Step 2: Get the student's preferences
            cursor.execute("""
                SELECT p.choice_id, p.college_id, p.course_id
                FROM can_pref cp
                JOIN preference p ON cp.choice_id = p.choice_id
                WHERE cp.username = %s
                ORDER BY p.choice_no ASC
            """, (username,))
            preferences = cursor.fetchall()

            # Check each preference in order
            for preference in preferences:
                choice_id, college_id, course_id = preference
                
                # Step 3: Check seat availability in seat_matrix
                cursor.execute("""
                    SELECT total_seats FROM seat_matrix
                    WHERE college_id = %s AND course_id = %s
                """, (college_id, course_id))
                result = cursor.fetchone()

                if result and result[0] > 0:  # If seats are available
                    # Step 4: Create allocation record
                    cursor.execute("""
                        INSERT INTO allocation (allocation_id, payment_status)
                        VALUES (%s, %s)
                    """, (allocation_id, 0))  # Assuming payment_status is 0 (not paid)
                    
                    # Insert into col_allo table
                    cursor.execute("""
                        INSERT INTO col_allo (college_id, course_id, allocation_id)
                        VALUES (%s, %s, %s)
                    """, (college_id, course_id, allocation_id))

                    # Insert into can_allo table
                    cursor.execute("""
                        INSERT INTO can_allo (username, allocation_id)
                        VALUES (%s, %s)
                    """, (username, allocation_id))

                    # Update seat matrix
                    cursor.execute("""
                        UPDATE seat_matrix
                        SET total_seats = total_seats - 1
                        WHERE college_id = %s AND course_id = %s
                    """, (college_id, course_id))

                    allocation_made = True
                    allocation_id += 1  # Increment the allocation ID for the next allocation
                    break  # Exit the preference loop after successful allocation

            # If no preference led to an allocation, the student remains unallocated

        # Commit the transaction after all allocations
        db.commit()
        print("College allocation completed successfully.")

    except MySQLdb.Error as error:
        # Rollback in case of any error
        db.rollback()
        print(f"Error occurred: {error}. Transaction rolled back.")

    finally:
        # Close the cursor and database connection
        cursor.close()
        db.close()

# Call the allocation function
allocate_colleges()
