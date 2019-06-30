from flask import Flask, render_template, request

my_app = Flask('flask_demo')

@app.route('/')
def show_predict_form():
    return render_template('predictorform.html')

# this line is decorating the results function
@app.route('/results', methods = ['POST'])

def results():
    form = request.form
    if request.method == 'POST':
        # write the function that loads the model
        model = get_model()
        year = request.form['year']
        predicted_val = model.predict(year)
        return render_template('resultsform.html', year = year, predicted_val = predicted_val)

if __name__ == '__main__':
    my_app.run('localhost', '9999', debug = True)