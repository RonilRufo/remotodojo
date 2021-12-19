PYTHON CODING CHALLENGE
===

Requirements
---

Rule: You can use any database technology.

Please construct the following:
- Create authentication for the user where user can input email and password--Website Landing Page:
- Allow user to login
- Allow users to register
- (Challenge: show list of 'public' Posts)
- Create a user login Page
- Create a user registration page--After the user logs in, the User is redirected to the homepage
- The home page shows a list of Twits user has created
- Users can see a list of Posts
- Users can create Post, and edit Post--Create new Post page
- Users can input a Post with a limit of 255 words.
- Users can publish a post
- Users can cancel creating the post--Edit post page
- From the homepage, the user can select a Post to edit
- Users can edit a Published post
- Users can cancel updating the post--Delete a Post
- From the homepage, the user should be able to delete a Post--Challenge: allow the user to make a - post-Public or Private
- A private post can only be viewed by the owner of the post
- Public post can be viewed by everyone and is listed on Website Landing Page

***

Project Setup
---

**Docker setup:**

Running the server:
```
docker-compose up --build
```

Create a Super User:
```
docker-compose exec backend ./manage.py createsuperuser
```

Site will be available at **http://localhost:8000**

***

Running Tests
---
Tests were added to provide more support on the solutions provided. To run the tests, simply use any of the following command:

**Coverage**
```
docker-compose exec backend coverage run --omit="*migrations*" -m pytest
```
To see a report of the amount of code covered, simply run the following command:
```
docker-compose exec backend coverage report -m
```

**Built-in Test Manager**
```
docker-compose exec backend ./manage.py test
```
