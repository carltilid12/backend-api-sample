from flask import Flask, jsonify, request
import sys
import psycopg2 # postgres
from config import (
    DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST
)

# Database Connection

db_connection = psycopg2.connect(
    dbname = DB_NAME,
    user = DB_USERNAME,
    password = DB_PASSWORD,
    host = DB_HOST
)

app = Flask(__name__)

def spcall(qry, param, commit=False):
    try:
        cursor = db_connection.cursor()
        cursor.callproc(qry, param)
        res = cursor.fetchall()
        if commit:
            db_connection.commit()
        return res
    
    except:
        res = [("Error: " + str(sys.exc_info()[0]) + " " + str(sys.exc_info()[1]),)]

    return res

# Course Routes

# Get course function
@app.route("/courses", methods=['GET'])
def get_courses():
    try:
        courses = spcall('get_courses', param=None)
        return jsonify({
            "status": "success",
            "data": courses})
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)})

# Create course function
@app.route('/course', methods=['POST'])
def create_course():
    data = request.get_json()
    course = data.get('course')
    try:
        if course:
            res = spcall('insert_course', (course,), commit=True)
            return jsonify({
                "status": "success",
                "message": course
            })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })
    
# Get a specific course by ID
@app.route('/course/<int:course_id>', methods=['GET'])
def get_course(course_id):
    try:
        res = spcall('get_course_by_id', (course_id,), commit=False)
        return jsonify({
            "status": "success",
            "data": res})
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)})
    
# Update a course by ID
@app.route('/course/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    try:
        data = request.get_json()
        course = data.get('course')
        if course:
            res = spcall('update_course_by_id', (course_id, course,), commit=True)
            return jsonify({
                "status": "success",
                "message": course
            })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })
    
# Delete a course by ID
@app.route('/course/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    try:
        res = spcall('delete_course_by_id', (course_id,), commit=True)
        return jsonify({
            "status": "success",
            "message": "Course deleted successfully"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })
    
# Student Routes 
    
# Get student Function
@app.route("/students", methods=['GET'])
def get_students():
    try:
        students = spcall('get_students', param=None)
        return jsonify({
            "status": "success",
            "data": students})
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)})

# Create student Function
@app.route('/student', methods=['POST'])
def create_student():
    data = request.get_json()
    student = data.get('student')
    course_id = data.get('course_id')
    try:
        if student and course_id:
            res = spcall('insert_student', (student, course_id,), commit=True)
            return jsonify({
                "status": "success",
                "message": student
            })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })
    
# Get a specific student by ID
@app.route('/student/<int:student_id>', methods=['GET'])
def get_student(student_id):
    try:
        res = spcall('get_student_by_id', (student_id,), commit=False)
        return jsonify({
            "status": "success",
            "data": res})
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)})
    
# Update a student by ID
@app.route('/student/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    try:
        data = request.get_json()
        student = data.get('student')
        course_id = data.get('course_id')
        if student and course_id:
            res = spcall('update_student_by_id', (student_id, student, course_id,), commit=True)
            return jsonify({
                "status": "success",
                "message": student
            })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })
    
# Delete a student by ID
@app.route('/student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        res = spcall('delete_student_by_id', (student_id,), commit=True)
        return jsonify({
            "status": "success",
            "message": "Student deleted successfully"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })
    
if __name__ == '__main__':
    app.run(debug=True)