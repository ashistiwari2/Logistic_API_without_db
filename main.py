from fastapi import FastAPI
from pydantic import BaseModel,Field
from sklearn.linear_model import LogisticRegression
import pandas as pd

file_csv=pd.read_csv("Fish.csv")
x=file_csv.iloc[:,1:].values
y=file_csv.iloc[:,0:-6].values

# Creating FastAPI instance
app = FastAPI(
    title="Logistic Regression Model without connecting to local database",
    description="To determine Species of Fish given all the parameters"
)


# Creating class to define the request body
# and the type hints of each attribute

class request_body(BaseModel):
    Weight:float=Field(description="Enter weight of fish in float or integer ",title="Weight of fish")
    Length1:float
    Length2:float
    Length3:float
    Height:float
    Width:float
    class Config:
         schema_extra = {
            "example": {
                "Weight": 10.4,
                "Length1": 9.6,
                "Length2": 9.5,
                "Length3": 9.2,
                "Height": 3.4,
                "Width": 2.3
            }
        }


# Creating and Fitting our Model
clf = LogisticRegression()
clf.fit(x,y)


# Creating an Endpoint to receive the data
# to make prediction on.
@app.post('/predict')
def predict(data: request_body):
    # Making the data in a form suitable for prediction
    test_data = [[
       data.Weight,
        data.Length1,
        data.Length2,
        data.Length3,
        data.Height,
        data.Width
    ]]

    # Predicting the Class
    class_idx = clf.predict(test_data)[0]
    print(class_idx)
    # Return the Result
    return {'Species':class_idx}
