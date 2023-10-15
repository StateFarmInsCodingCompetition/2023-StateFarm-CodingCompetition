from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import SelectField
from simple_data_tool import SimpleDataTool

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secret key

data_tool = SimpleDataTool()

# Define a form for selecting data
class DataSelectionForm(FlaskForm):
    data_type = SelectField('Data Type', choices=[('agents', 'Agents'), ('claims', 'Claims')])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = DataSelectionForm()

    if form.validate_on_submit():
        data_type = form.data_type.data
        if data_type == 'agents':
            data = data_tool.get_agent_data()
        elif data_type == 'claims':
            data = data_tool.get_claim_data()
        else:
            data = []

        return render_template('index.html', form=form, data=data)

    return render_template('index.html', form=form, data=None)

if __name__ == '__main__':
    app.run(debug=True)
