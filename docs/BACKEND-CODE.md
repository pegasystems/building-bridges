Understanding the backend code
=============

## Typical API call flow

Let's present it on example for api point: `api/surveys/<string:survey_url>/questions`

1. User make POST API call to `api/surveys/<string:survey_url>/questions`
2. Restplus looks for the proper function to handle the request (using **namespace**, **route** and then checking the API call type). In our example, it will find a function in [that](../bridges/api/endpoints/questions.py) file.
3. This function is decorated by `@api.expect` - it means, it checks if the API call looks good and have required parameters, as shown in *swagger*. These models are defined [here](api/serializers.py). If the API call is not correct, it will automatically return *400 BAD REQUEST*.
4. If the API call is correct, the function proceedes, and we typically parse the given API data in [logic](../bridges/api/logic.py) file, which typically ask database [here](../bridges/database/mongo.py).
5. While getting the database documents, we parse them using `from_dict` function, which takes simple *json* file which we got from mongo, and make it an object of some class (something similar to ORM). We then operate on that objects, instead of json files. You can see that classes in the `database/objects` directory.
6. Then we simply return some data from an API call. Additionaly, if a function is decorated by `@api.marshal_with`, we restrict the data send to user by the model defined in that decorator.
7. User is happy!

If some unhandled exception occur during the API call, then it will be handled by the `default_error_handler` function defined [here](../bridges/api/restplus.py)


