from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/check_ticket', methods=['GET'])
def check_ticket():
    # Retrieve the QR code from the request parameters
    id = request.args.get('id')

    connection = mysql.connector.connect(
    	host = "<your-username>.mysql.pythonanywhere-services.com",
    	user = "<your-username>",
    	password = "<your-password>",
    	database = "<your-username>$tickets"
    )

    cursor = connection.cursor()
    cursor.execute('''SELECT status FROM tickets
                               WHERE id={};'''.format(id))
    result = cursor.fetchone()

    if result is not None:
        status = result[0]
        if status == 'unused':
            cursor.execute('''UPDATE tickets
                            SET status='used'
                            WHERE id={};'''.format(id))

            connection.commit()
            connection.close()

            return "<p style='color: #70AD47; font-size: 50px; font-family: Lucida Console'>Valid ID: {}</p>".format(id)
        else:
            return "<p style='color: #ED7D31; font-size: 50px; font-family: Lucida Console;'>Code already scanned for ID: {}</p>".format(id)
    else:
        return jsonify({'status': 'unknown'})

if __name__ == '__main__':
    app.run()
