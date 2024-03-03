from flask import Flask, render_template, request
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
from core.check_input import validate_input
from core.log import create_logger
from core.create_plot import visulize_data


app = Flask(__name__)
# Create a logger
logger = create_logger()

# Load pre-trained models
models = {
    'Linear Regression': 'linear_regression_model.pkl',
    'Random Forest': 'random_forest_model.pkl',
    # Add more models as needed
}
# Load the saved model from the pickle file
#with open("linear_regression_model.pkl", "rb") as f:
 #   model = pickle.load(f)

# Define a route to render the HTML form
@app.route("/")
def home():
    logger.info('Rendering home page')
    return render_template("index.html",models=models)

# Define a route to handle form submission and make predictions
@app.route("/predict", methods=["POST"])
def predict():
    logger.info('Received form submission')
    # Get the input values from the form
    
    rd_spend = request.form["rd_spend"]
    administration = request.form["administration"]
    marketing_spend = request.form["marketing_spend"]
    state = request.form["state"]
    selected_model = request.form["model"]

    logger.info(f'Input values: R&D Spend={rd_spend}, Administration={administration}, Marketing Spend={marketing_spend}, State={state}')
    logger.info(f'Selected model: {selected_model}')

    # Convert input values to floats
    try:
        rd_spend = float(rd_spend)
        administration = float(administration)
        marketing_spend = float(marketing_spend)
    except ValueError:
        logger.error('Invalid input values')
        return render_template("index.html", errors=['Input values must be valid numbers'])
    
    # Validate input
    errors = validate_input(rd_spend, administration, marketing_spend, state)
    
    if errors:
        logger.error('Validation failed. Errors: %s', errors)
        return render_template("index.html", errors=errors)
    
    logger.info('Input validation successful')

    # Load the selected model
    model_file = models[selected_model]
    with open(model_file, "rb") as f:
        model = pickle.load(f)
    #print(state)
    # Load the dataset to get column names
    columns = ['R&D Spend', 'Administration', 'Marketing Spend', 'State']
    
    # Create a DataFrame with the input values
    input_data = pd.DataFrame([[rd_spend, administration, marketing_spend, state]],
                              columns=columns)
    # Perform label encoding for the 'State' column
    label_encoder = LabelEncoder()
    input_data['State'] = label_encoder.fit_transform(input_data['State'])

    # Create plot
    plot_url=visulize_data(rd_spend, administration, marketing_spend)

    # Make prediction using the loaded model
    logger.info('Making prediction')
    prediction = model.predict(input_data)
    logger.info('Prediction: %s', prediction)

    
    # Render the result template with the prediction
    return render_template("result.html", prediction=round(prediction[0],4),plot_url=plot_url,selected_model=selected_model)

if __name__ == "__main__":
    app.run(debug=True)
