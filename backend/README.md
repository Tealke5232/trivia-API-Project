# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1.x Use Flask-CORS to enable cross-domain requests and set response headers.  
2.x Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3.x Create an endpoint to handle GET requests for all available categories.
4.x Create an endpoint to DELETE question using a question ID.
5.x Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6.x Create a POST endpoint to get questions based on category.
7.x Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8.x Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9.x Create error handlers for all expected errors including 400, 404, 422 and 500.

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code.

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```
## documentation
Here is the Documentation on all the API calls.

1. /questions  :: returns a json response with success status, total_questions, categories, and questions. Questions are returned as paginated. returns 200 for success, if there are no questions 1 will be generated to remind you to add trivia quesitons.

      return jsonify({
            'success': True,                        ## success !!
            'total_questions': len(questions),      ## total trivia questions in db
            'categories': categories_list,          ## list of available categories
            'questions': paginated_questions        ## the questions, paginated
        }), 200


2. /questions/<int:id>  method = Delete   :: Deletes the question with the corresponding ID, returns 200 if successful deletion, returns 404 if question was not found with corresponding id

      return jsonify({
                'success': True,                               ## success
                'message': "Trvia Question has been deleted"   ## general message returned
            }), 200


3. /questions   method = Post  ::  recieves a request in the form of json, parses the data between question, answer, difficulty, and category. inserts that data into the DB as a question and returns 201 on succesful completion. if unsuccessful returns 422. if there is a search term, the request will be treached as a search function, trivia questions containing the string searched will be returned.

      ## if searchTerm != null          SEARCH
      return jsonify({
                  'success': True,                            ## success
                  'questions': current_questions,             ## questions found in search, paginated
                  'total_questions': len(questions),          ## total # of searched questions in DB
                  'current_category': None                    ## search so no current category
              }), 200


    ## if searchTerm = null           ADD
    return jsonify({
                'success': True,                                        ## success  
                'created': question.id,                                 ## id of created trivia question
                'questions': current_questions,                         ## questions, paginated
                'total_questions': len(Question.query.all()),           ## length of questions in DB
                'message' : 'successfuly added the trivia quesiton'     ## success message
            }), 201



4. /categories/<int:category_id>/questions   ::  takes the category ID and returns a json response consisting of success, questions (paginated) within the category, total_questions within category and current category with success code of 200. if category with that id is not found returns 404

    return jsonify({
              'success': True,                      ## success  
              'questions': current_questions,       ## questions within category, paginated
              'total_questions': len(selection),    ## total questions in category
              'current_category': category_id       ## category
          }), 200



5. /quizzes   method = Post  ::   recieves the request in the form of json.  request consists of previous question, and category. if category = 0, category is all. returns a json response consisting of success and a random new question(may more maynot be category oriented depending on input)

    return jsonify({
            'success': True,              ## success
            'question': next_question     ## the next questions
        }), 200

6. /categories     ::    returns a dictionary of all the available categories.

    return jsonify({
            'success': True,      ## success
            'categories': data    ## dictionary of available categories
        }), 200


6. error Handlers   ::   400, 404, 405, 410, 422, 500, 505  are covered


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
