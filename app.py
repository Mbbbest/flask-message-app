from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from flask import flash



# Initialize the Flask app
app = Flask(__name__)
app.secret_key = "secret"  # Needed for flash messages

# Set up the database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///contact.db"  # Database URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Avoid unnecessary warnings
db = SQLAlchemy(app)  # Initialize the database object

# Define the database model (this will act like a table in the database)
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each message
    name = db.Column(db.String(100))  # Name field
    email = db.Column(db.String(120))  # Email field
    message = db.Column(db.Text)  # Message content

# Define the contact form using FlaskForm from Flask-WTF
class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email(message="Invalid email address.")])
    message = TextAreaField("Message", validators=[DataRequired(), Length(min=10, max=500, message="Message must be between 10 and 500 characters.")])

# Home page
@app.route("/")
def home():
    return render_template("index.html")  # Rendering the homepage (index.html)

# Contact page
@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data

        # Save to the database
        new_message = Contact(name=name, email=email, message=message)
        db.session.add(new_message)
        db.session.commit()

        # Flash success message
        flash(f"Thanks {name}, your message has been saved!", "success")
        return redirect(url_for('contact'))

    return render_template("contact.html", form=form)

# View all messages
@app.route("/messages")
def messages():
    page = request.args.get('page', 1, type=int)
    all_messages = Contact.query.paginate(page, 5, False)  # 5 messages per page
    return render_template("messages.html", messages=all_messages.items, pagination=all_messages)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create the database and tables if not already created
    app.run(debug=True)  # Run the app in debug mode
