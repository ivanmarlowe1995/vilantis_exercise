# Vilantis Application Exercise 
****
## Context
This readme file serves as a guidance in determining the instructions on how to deploy the interviewer's machine. It serves as reference to the functionalities of the developed website application.

### Features
* Validate and connect an endpoint URL on the Data Pusher API __(AWS API Gateway)__
* Receive the data coming from the endpoint and store in a messaging queue __(AWS Lambda & SQS Queue)__
  * Parse and format the incoming data to be able to be seamlessly integrated in an __RDBMS__ 
  * Expected raw table: __country_relation__
* Store the received data in an RDBMS __(AWS RDS)__
* Create a view that will essentially format the raw ingested table (__country_relation_revised__)
* Create a view to generate the relationships of each country (__country_relation_score__)
* Determine click history from a specified requestor and store in the database (__click_history__)
* Create an interface with pagination support for the 3 core tables/views:
  * Country Relationship Scores
  * Country Relation RAW
  * Website Click History
* Create a filter capability up to 4 columns which supports the following expression for each field in the interface:
  * __=__
  * __IN__
  * __LIKE__
  * __>=__
  * __<=__
  * __>__
  * __<__
* Feature to order columns on ascending or descending order

## Interface

### Admin Click History
![image](https://user-images.githubusercontent.com/22069559/183402910-4071b0de-514a-43d6-a431-95dde25e1fa8.png)

### Country Relations Raw
![image](https://user-images.githubusercontent.com/22069559/183403067-2b6ac3ac-9513-4873-a809-4db10540f12d.png)

### Country Relationships Score
![image](https://user-images.githubusercontent.com/22069559/183403237-0db514c8-e009-4f09-a204-554fa46024c1.png)

## Notes about ingesting and cleansing data
* The raw data was expected to not contain all attributes consistently (missing __Min. Reputation Level to Occur__) 
  * Handled accordingly by making this blank in the table initally then created a view with a low-reliability due to many factors on determining the values of this field:
    * the data contains negative points for a favorable event or an event showed a positive reputation change while marking it as inhospitable 
    * Many rows contain neutral reputation type but has values associated with very high negative reputation change
    * Some records contain a very high negative value for a suspicious act
    * There is a minimal margin of values for inhospitable and suspicious
* Some challenges about generating the Relationship between two countries were met:
  * Had to create a country dimensional table to get the complete list of countries worldwide
  * There were alot of records that has a substring that belong to another country so the country extraction for the text produced was more than 2 (e.g. Sudan, South Sudan, Guinea, East Guinea)
    * Resolution was Categorize the dataset per country with the smallest length
    * Get only the countries with ranks based on length in descending order
    
## Deployment

### Steps
1. Clone this repository.
2. Import via pycharm or IDE tools that support venv
3. Include the `.env` file to the base path
4. After importing as a Flask project, set the environment variable and run:
```
export FLASK_ENV=development
flask run
```
5. Install any missing dependencies that are listed in the `requirements.txt`
6. Access the localhost server `http://127.0.0.1:5000/`



