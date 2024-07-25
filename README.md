Note: You'll need to set the OPEN_AI_KEY in the .env file before starting the server.
-


The following steps are used to set up and start the project
-
1. cd into the project folder and run pip install -r requirements.txt.
2. To start flask server run "flask --app app  run"  .


For Postman testing you use the following URLs.
-
1. http://127.0.0.1:5000/api/rep_performance?rep_id=185
2. http://127.0.0.1:5000/api/team_performance
3. http://127.0.0.1:5000/api/performance_trends?time_period=monthly
4. http://127.0.0.1:5000/api/performance_trends?time_period=quarterly
