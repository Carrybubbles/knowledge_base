from flask import Flask, request
from h2o import h2o
from h2o.estimators import H2OGeneralizedLinearEstimator

app = Flask(__name__)
h2o.connect(ip="h2o", port=54321)


@app.route('/ok')
def health():
    return "Hello, World!"


@app.route('/model', methods=['POST', 'GET'])
def model():
    if request.method == 'GET':
        return str(h2o.models())
    else:
        prostate = h2o.import_file("https://h2o-public-test-data.s3.amazonaws.com/smalldata/prostate/prostate.csv")

        prostate['CAPSULE'] = prostate['CAPSULE'].asfactor()
        prostate['RACE'] = prostate['RACE'].asfactor()
        prostate['DCAPS'] = prostate['DCAPS'].asfactor()
        prostate['DPROS'] = prostate['DPROS'].asfactor()

        predictors = ["AGE", "RACE", "VOL", "GLEASON"]
        response_col = "CAPSULE"

        train, test = prostate.split_frame(ratios=[0.8], seed=1234)

        glm_model = H2OGeneralizedLinearEstimator(family="binomial",
                                                  lambda_=0,
                                                  compute_p_values=True)
        glm_model.train(predictors, response_col, training_frame=prostate)
        return str(h2o.models())
