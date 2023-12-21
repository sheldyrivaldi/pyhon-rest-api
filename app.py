# untuk install flask : pip install flask
# untuk install mysql db : pip install flask_mysqldb

from flask import Flask, jsonify, request, make_response
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

# Config MYSQL
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)

def is_valid_string(value) -> bool:
    # Function to check if a value is a valid string
    return isinstance(value, str)

def is_valid_integer(value) -> bool:
    # Function to check if a value is a valid string
    return isinstance(value, int)

@app.route('/')
def root():
    return 'Selamat datang di tutotial restfull API python'

@app.route("/person", methods=["GET"])
def person():
    return jsonify({
        'name': 'Faqih',
        'address': 'Bandung',
        'email': 'faqih@gmail.com',
    })

@app.route("/dosen", methods=["GET", "POST"])
def dosen():
    if request.method == 'GET':
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM dosen")

            # Get column name from cursor description
            coloum_name = [i[0] for i in cursor.description]
            print(coloum_name)

            # fetch data and format into list of dictionaries
            data = []
            dosen = cursor.fetchall()
            for row in dosen:
                print(row)
                data.append(dict(zip(coloum_name, row)))

            cursor.close()
            return jsonify(data)
        
        except Exception as e:
            print(f"Error: {str(e)}")
            return make_response(jsonify({'code': 500, 'error': 'Internal Server Error'}), 500)
    
    elif request.method == 'POST':
        try:
            cursor = mysql.connection.cursor()

            data_json = request.get_json()

            nama = data_json.get('nama')
            if nama is None: return make_response(jsonify({'code': 400, 'status': 'Bad Request', 'message': 'nama is required!'}), 400)
            if not is_valid_string(nama): return make_response(jsonify({'code': 400, 'status': 'Bad Request', 'message': 'nama is alphabet!'}), 400)
            if len(nama) > 50:  return make_response(jsonify({'code': 400, 'status': 'Bad Request', 'message': 'max 50 character!'}), 400)

            univ = data_json.get('univ')
            if univ is None: return make_response(jsonify({'code': 400, 'status': 'Bad Request', 'message': 'univ is required!'}), 400)
            if not is_valid_string(univ): return make_response(jsonify({'code': 400, 'status': 'Bad Request', 'message': 'univ is alphabet!'}), 400)
            if len(univ) > 50:  return make_response(jsonify({'code': 400, 'status': 'Bad Request', 'message': 'max 50 character!'}), 400)

            jurusan = data_json.get('jurusan')
            if jurusan is None: return make_response(jsonify({'code': 400, 'status': 'Bad Request', 'message': 'jurusan is required!'}), 400)
            if not is_valid_string(jurusan): return make_response(jsonify({'code': 400, 'status': 'Bad Request', 'message': 'jurusan is alphabet!'}), 400)
            if len(jurusan) > 50:  return make_response(jsonify({'code': 400, 'status': 'Bad Request', 'message': 'max 50 character!'}), 400)

            sql = "INSERT INTO dosen (nama, univ, jurusan) VALUES (%s, %s, %s)"
            val = (nama, univ, jurusan)
            cursor.execute(sql, val)

            mysql.connection.commit()

            cursor.close()
            return jsonify({'code': 200, 'message': 'Data added successfully!'})
        except Exception as e:
            print(f"Error: {str(e)}")
            return make_response(jsonify({'code': 500, 'error': 'Internal Server Error'}), 500)
    
@app.route('/dosen/<int:id>', methods=['GET', 'DELETE', 'PUT', 'PATCH'])
def dosen_with_id(id):
    if request.method == 'GET':
        try: 
            if id is None: return make_response(jsonify({'code': 400, 'status': 'Bad Request', 'message': 'id param is required!'}), 400)
            if len(str(id)) > 11:  return make_response(jsonify({'code': 400, 'status': 'Bad Request', 'message': 'max 11 character!'}), 400)
            
            cursor = mysql.connection.cursor()
            sql = "SELECT * FROM dosen WHERE id = %s"
            cursor.execute(sql, (id,))


            coloum_name = [i[0] for i in cursor.description]
            dosen = cursor.fetchone()
            data = dict(zip(coloum_name, dosen))
            cursor.close()

            return jsonify(data)
        
        except Exception as e:
            print(f"Error: {str(e)}")

            return make_response(jsonify({'code': 500, 'error': 'Internal Server Error'}), 500)

    elif request.method == 'DELETE':
        try:
            if id is None: return make_response(jsonify({'code': 400, 'status': 'Bad Request', 'message': 'id param is required!'}), 400)
            if id > 11:  return make_response(jsonify({'code': 400, 'status': 'Bad Request', 'message': 'max 11 character!'}), 400)
        
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM dosen WHERE id = %s"
            val = (id,)
            cursor.execute(sql, val)

            mysql.connection.commit()

            cursor.close()
            return jsonify({'code': 200, 'message': 'Data deleted successfully!'})
        except Exception as e:
            print(f"Error: {str(e)}")

            return make_response(jsonify({'code': 500, 'error': 'Internal Server Error'}), 500)
    
    elif request.method == 'PUT' or request.method == 'PATCH':
        try:
            cursor = mysql.connection.cursor()

            sql = "SELECT * FROM dosen WHERE id = %s"
            cursor.execute(sql, (id,))


            coloum_name = [i[0] for i in cursor.description]
            dosen = cursor.fetchone()
            data = dict(zip(coloum_name, dosen))

            nama = data['nama']
            univ = data['univ']
            jurusan = data['jurusan']

            if id is None: return make_response(jsonify({'code': 400, 'status': 'Bad Request', 'message': 'id param is required!'}), 400)
            if id > 11:  return make_response(jsonify({'code': 400, 'status': 'Bad Request', 'message': 'max 11 character!'}), 400)
        
            
            data_json = request.get_json()

            if data_json.get('nama'): nama = data_json.get('nama')
            if nama and  not is_valid_string(nama): return make_response(jsonify({'code': 400, 'status': 'Bad Request', 'message': 'nama is alphabet!'}), 400)
            if nama and len(nama) > 50:  return make_response(jsonify({'code': 400, 'status': 'Bad Request', 'message': 'max 50 character!'}), 400)

            if data_json.get('univ'): univ = data_json.get('univ')
            if univ and  not is_valid_string(univ): return make_response(jsonify({'code': 400, 'status': 'Bad Request', 'message': 'univ is alphabet!'}), 400)
            if univ and len(univ) > 50:  return make_response(jsonify({'code': 400, 'status': 'Bad Request', 'message': 'max 50 character!'}), 400)

            if data_json.get('jurusan'): jurusan = data_json.get('jurusan')
            if jurusan and  not is_valid_string(jurusan): return make_response(jsonify({'code': 400, 'status': 'Bad Request', 'message': 'jurusan is alphabet!'}), 400)
            if jurusan and len(jurusan) > 50:  return make_response(jsonify({'code': 400, 'status': 'Bad Request', 'message': 'max 50 character!'}), 400)

            sql = "UPDATE dosen SET nama=%s, univ=%s, jurusan=%s WHERE id = %s"
            val = (nama, univ, jurusan, id,)
            cursor.execute(sql, val)

            mysql.connection.commit()

            cursor.close()
            return jsonify({'code': 200, 'message': 'Data updated successfully!'})
        except Exception as e:
            print(f"Error: {str(e)}")

            return make_response(jsonify({'code': 500, 'error': 'Internal Server Error'}), 500)

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)