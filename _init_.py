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
    try:
        if student:
            res = spcall('insert_student', (student,), commit=True)
            return jsonify({
                "status": "success",
                "message": student
            })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })
    
if __name__ == '__main__':
    app.run(debug=True)