from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
from tasks import make_celery

app = Flask(__name__)

#celery config
app.config['CELERY_BROKER_URL'] = 'amqp://localhost//'								#using rabbitmq 						
app.config['CELERY_BACKEND'] = 'amqp://localhost//'

celery = make_celery(app)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'someemail@gmail@gmail.com'							#test gmail account
app.config['MAIL_PASSWORD'] = 'password'

mail = Mail(app)

@app.route('/')
def index():
	return render_template('index.html')

#send mail with celery
@celery.task(name='web.process')														
def send_email(msg):
    with app.app_context():
        mail.send(msg)
	
@app.route('/process', methods=['POST'])
def process():
	email = request.form['email']
	subject = request.form['subject']
	body = request.form['body']

	msg = Message(subject,sender='someemail@gmail.com',recipients=[email])
	msg.body = body
	if email and subject and body:														#checking if all the inputs are filled
		send_email.delay(msg)															
		return jsonify({'success' : 'your message has sent.'})

	return jsonify({'error' : 'Missing data!'})

if __name__ == '__main__':
	app.run(debug=True)