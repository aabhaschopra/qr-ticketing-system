from flask import Flask, jsonify, request, render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/check_ticket', methods=['GET'])
def check_ticket():
    # Retrieve the QR code from the request parameters
    id = request.args.get('id')

    conn = sqlite3.connect('tickets.db')

    cursor = conn.execute('''SELECT status FROM tickets
                             WHERE id={};'''.format(id))
    result = cursor.fetchone()

    if result is not None:
        status = result[0]
        if status == 'unused':
            conn.execute('''UPDATE tickets
                            SET status='used'
                            WHERE id={};'''.format(id))
            conn.commit()
            conn.close()

            return "<p style='color: #70AD47; font-size: 50px; font-family: Lucida Console'>Valid ID: {}</p>".format(id)
        else:
            return "<p style='color: #ED7D31; font-size: 50px; font-family: Lucida Console;'>Code already scanned for ID: {}</p>".format(id)
    else:
        return jsonify({'status': 'unknown'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
