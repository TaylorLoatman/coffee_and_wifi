from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, SelectField
from wtforms.validators import DataRequired, url
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired('Please enter cafe name.')])
    location = StringField('Google Map Location Url', validators=[url(message='Please enter a valid url.')])
    hour_open = StringField('Opening Time e.g. 8:30AM',validators=[DataRequired
                                                                     ('Please enter valid time format 00:00AM/PM')])
    close_hour = StringField('Time Close e.g. 5:00PM', validators=
                                                        [DataRequired('Please enter valid time format 00:00AM/PM')])
    coffee = SelectField('Coffee Rating', choices=['✘', '☕️', '☕️ ☕️', '☕️ ☕️ ☕️', '☕️ ☕️ ☕️ ☕️',
                                                   '☕️ ☕️ ☕️ ☕️ ☕️'], validators=[DataRequired()])
    wifi = SelectField('Wifi Strength Rating', choices=['✘', '💪', '💪 💪', '💪 💪 💪', '💪 💪 💪 💪',
                                                        '💪 💪 💪 💪 💪'], validators=[DataRequired()])
    power = SelectField('Power Socket Availability', choices=['✘', '🔌', '🔌 🔌', '🔌 🔌 🔌',
                        '🔌 🔌 🔌 🔌', '🔌 🔌 🔌 🔌 🔌'], validators=[DataRequired()])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_data = []
        for i in form:
            new_data.append(i.data)

        with open('cafe-data.csv', 'a') as csv_file:
            write_data = csv.writer(csv_file)
            write_data.writerow(new_data[:7])
            csv_file.close()
        print("True")
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
