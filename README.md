# REVIEWS
A basic API for Reviews


<hr>

<h2>The Problem:</h2>

<b>Description</b>: Using Django, create a simple API that allows users to post and retrieve their reviews. <br>

<ul>
<li>Users are able to submit reviews to the API.</li>
<li>Users are able to retrieve reviews that they submitted.</li>
<li>Users cannot see reviews submitted by other users.</li>
<li>Use of the API requires a unique auth token for each user.</li>
<li>Submitted reviews must include, at least, the following attributes:<br>
    Rating - must be between 1 - 5<br>
    Title - no more than 64 chars<br>
    Summary - no more than 10k chars<br>
    IP Address - IP of the review submitter<br>
    Submission date - the date the review was submitted<br>
    Company - information about the company for which the review was submitted, can be simple text (e.g., name, company id, etc.) or a separate model altogether<br>
    Reviewer Metadata - information about the reviewer, can be simple text (e.g., name, email, reviewer id, etc.) or a separate model altogether<br>
</li>
</ul><br>

<hr>

<h2>The Project</h2>

<h3>Requirements</h3>

This project uses:

Python 3 <br>
Django==1.11.4 <br>
django-rest-swagger==2.1.2<br>
djangorestframework==3.6.3<br>
PyJWT==1.5.2<br>

<hr>

<h3>How To Run</h3>

<ul>
<li>Download or clone the repository</li>
<li>pip install the libraries in the file requirements.txt</li>
<li>Open a terminal or prompt inside the folder-name/reviews/src</li>
<li>Run the migration <code>python manage.py migrate</code></li>
<li>Run the server <code>python manage.py runserver</code></li>
<li>check the docks at <a href="http://localhost:8000/docs" target="_blank">http://localhost:8000/docs</a></li>
<li>Test the API as you wish.</li>
</ul>

<hr>

<h2>Folder Structure</h2>

<img src="http://i.imgur.com/40wOLmb.png">

The project is composed by 5 apps.

<ul>
<li><b>Authentication: </b> Handles the user authentication, composed by a login and logout view. This part is covered by many tests, in order to treat the authentication as a safe and controlled feature.</li>
<li><b>util: </b> Features and tools that are general for the application. Here, the things that are too generic to fit in a specific app, or are common to many apps, are stored.</li>
<li><b>Project: </b> The root app, holds the settings and configurations for the project.</li>
<li><b>Registration: </b>Handles the user registration. It has strict rules and services in order to organize the registration.</li>
<li><b>Reviews</b>: Handles the logical layer for the reviews.</li>
</ul>

<hr>

<ul>
<li><b>services.py</b>: This script is more related to the coding logic of the app itself. It is similar to basic JAVA project schemas, and they help to avoid codes on the views.py</li>
<li><b>rules.py</b>: This one is more related to the "business rules" of the app, or the "feature rules". For example, we have rules that restric the registration, you must enter a valid e-mail in order to register on the app. They are usually called from the services.py in order to validate inputs/outputs.</li>
</ul>

<hr>

<h2>APPs and CRUDs </h2>

<img src="http://i.imgur.com/MnCgjYR.png">

This section explains how to use the app from the API user point of view.

<h3>Registration</h3>

<b>Request: </b> <br>
In order to make a registration, the user might have to insert three information: <code>Name, email, password</code>. <br>
Those info must be passed in the request body, using a <code>POST</code> method, as stated on the example below.

**_Request via curl:_** <br>
<code>curl -H "Content-Type: application/json" -X POST -d '{"email":"marcelo@example.com","password":"tops3cr3t", "name":"Marcelo"}' http://127.0.0.1:8000/registration/</code> <br>
<br>

**_Response:_**<br>
If everything is fine, the response will bring a token, that should be user for making requests as a registered user.<br>
Example: <br>
<code>{
  "id_token": <JWT_TOKEN>
}</code>
<br>
This token is valid for 24h <br>

**_Password Rules_**<br>
The rules are simple: 
<ul>
<li>The name cannot be empty and should have at least 3 characters.</li>
<li>The e-mail cannot be empty, and it must have a true e-mail shape</li>
<li>the password should have at least 6 characters and should containg only letters, numbers, dashes or underscores.</li>
</ul>

<hr>

<h3>Authentication</h3>

**_Login Request_**<br>
Login attempts are made via POST method. And they are pretty straight forward: Request example via curl: <br>
<code>curl -X POST -H "Content-Type: application/json" -d '{"email":"marcelo@example.com","password":"tops3cr3t"}' http://localhost:8000/auth/login</code>
<br>

**_Login Response_**<br>
The response should be a token if everything went fine.<br>
<code>{"id_token": <JWT_TOKEN>}</code>
<br>

**_Logout Request_**<br>
Logout is basically sending our active token to the trash. This app has a **black list**, that will hold
tokens that are not valid anymore.<br>
<code>curl -X POST -H "Content-Type: application/json" -d '{"id_token":"<JWT_TOKEN>"}' http://localhost:8000/auth/logout/</code>

**_Logout Response_**<br>
Will return only a "200 OK" status.
<br>

<hr>

<h3>Reviews</h3>

Handles sending and retrieving review-data from the server, the fields are the same as declared on the problem proposal<br>
The user must have a valid token in order to send/retrieve data, and it should be placed in the "Authorization" Header.
Example:<br>

**_POST Review Request_**:<br>
The fields are <code>company_name, rating, summary and title</code>. Remember to place the token in the "Authentication" header. Example: <br>
<code>curl -X POST -H "Content-Type: application/json" -H "Authorization: <JWT_TOKEN>" -d '{"company_name": "BlurryMind","rating": 5,"summary": "A very good Company","title": "I loved it"}' http://localhost:8000/reviews/</code><br>

The following row will be created in the database:<br>
<img src="http://i.imgur.com/EKrx6Jz.png"><br>

**_POST Review Response:_**<br>
For the above request, the response will be: <br>
<code>{"status":"Your Review was stored!"}</code>

**_GET Review Request_**:<br>

Example: <br>
<code>curl -X GET -H "Content-Type: application/json" -H "Authorization: <JWT_TOKEN>" http://localhost:8000/reviews/</code>

**_GET Review Response_**:<br>
Returns a list of all the reviews that a certain user has sent<br>
Example: <br>
<img src="http://i.imgur.com/B2BsdhP.png">



<h2> Tests </h2>


All apps are covered.

<img src="http://i.imgur.com/YSw5JU1.png">

That's all, I hope you enjoy it!

