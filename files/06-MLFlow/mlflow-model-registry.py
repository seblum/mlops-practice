# MLFLow Model Registry

print("MLFlow Model Registry Tutorial Script")


print("> register model in registry 1.0")

import mlflow.sklearn
import mlflow.pyfunc
from sklearn.ensemble import RandomForestRegressor

run_name="registry-example-run"
params = {"n_estimators": 4, "random_state": 42}

run_name = 'logging model example'
with mlflow.start_run(run_name=run_name) as run:
   rfr = RandomForestRegressor(**params).fit([[0, 1, 0]], [1])
   mlflow.log_params(params)
   # Log and store the model and the MLFlow Model Registry
   mlflow.sklearn.log_model(rfr, artifact_path="sklearn-model")

model_uri = "runs:/{}/sklearn-model".format(run.info.run_id)
model_name = f"{namespace}-RandomForestRegressionModel"

model = mlflow.pyfunc.load_model(model_uri=model_uri)
data = [[0, 1, 0]]
model_pred = model.predict(data)
print(f"model_pred: {model_pred}")



## ---------------------
print("> register model in registry 2.0")

# The previously stated Model URI and name are needed to register a MLFlow Model
mv = mlflow.register_model(model_uri, model_name)
print("Name: {}".format(mv.name))
print("Version: {}".format(mv.version))
print("Stage: {}".format(mv.current_stage))



## ---------------------
print("> Use model for prediction")

import mlflow.pyfunc

# Load model for prediction. Keep note that we now specified the model version.
model = mlflow.pyfunc.load_model(
   model_uri=f"models:/{model_name}/{mv.version}"
)

# Predict based on the loaded model
data = [[0, 1, 0]]
model_pred = model.predict(data)
print(f"model_pred: {model_pred}")



## ---------------------
print("> Transition model to another stage")

# Transition the model to another stage
client = MlflowClient()

stage = 'Staging' # None, Production

client.transition_model_version_stage(
    name=model_name,
    version=mv.version,
    stage=stage
)



