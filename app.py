from flask import Flask, url_for, redirect, request, render_template
import pickle

app = Flask(__name__)

model = pickle.load(open('loan_predictor.pkl', 'rb'))

def data_processing(gender, married, dependents, education, self_employed, property_area):
    gender = 0 if gender == 'Female' else 1
    married = 0 if married == 'No' else 1
    education = 0 if education == 'Not Graduate' else 1
    self_employed = 0 if self_employed == 'No' else 1
    dependents_dict = {
        '0': 0,
        '1': 1,
        '2': 2,
        '3+': 3,
    }
    dependents = dependents_dict[dependents]
    property_area_dict = {
        'Rural': 0,
        'Semiurban': 1,
        'Urban': 2
    }
    property_area = property_area_dict[property_area]
    return gender, married, dependents, education, self_employed, property_area

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prediction', methods=['POST'])
def prediction():
    name = request.form.get('name')
    gender = request.form.get('gender')
    married = request.form.get('married')
    dependents = request.form.get('dependents')
    education = request.form.get('education')
    self_employed = request.form.get('self_employed')
    applicant_income = request.form.get('applicant_income')
    coapplicant_income = request.form.get('coapplicant_income')
    loan_amount = request.form.get('loan_amount')
    loan_amount_term = request.form.get('loan_amount_term')
    credit_history = request.form.get('credit_history')
    property_area = request.form.get('property_area')

    gender, married, dependents, education, self_employed, property_area = data_processing(
        gender, married, dependents, education, self_employed, property_area)
    
    loan_status = model.predict([[
        int(gender), int(married), int(dependents), int(education), int(self_employed), int(applicant_income), int(coapplicant_income), int(loan_amount), int(loan_amount_term), int(credit_history), int(property_area)]])

    pred_result = ''
    if loan_status == 1:
        pred_result = f'Dear {name}, you are eligible for getting the specified loan amount and your application will be sanctioned by the bank.'

    else:
        pred_result = f'Sorry {name}, you are not eligible for receiving loan from the bank.'

    return render_template('prediction.html', pred_result=pred_result)

if __name__ == '__main__':
    app.run() 