# GoCovid
## *Api for posting data about victims*
---
### Idea:-

Idea is to ask the victims some simple wuestions about their no of outings in recent time,Have they visited any abroad countires recently or not
,their home town and users will provide their data through rhe app. Now the app will interract with this api to store data in database once data 
has been stored the idea is to train a machine learning model to preduct the chances of a person being a victim and mark the sensitive areas.

---
### Requirements and Installation guide:-
 
 **Requirements:-**

1. Python 3 is required ideally (Python 3.6 or above).
2. The other requirements are specified in the ```requirements.txt``` file

**Installation Guide:-**
> Clone the repository 
> Move in to the repostory folder through terminal or cmd and type 
> ```pip install requirements.txt``` to install all the dependencies.
---

### How to run the application:-

Once all the dependencies are installed type ```python app.py``` to run the application your application will run in [this link](http://127.0.0.1:5000) 

### EndPoints In the api:-


1. ***/register*** :-

  * Only Post Request is allowed *

Takes in 3 Parameters
1. username(String)
2. password(String)
3. isadmin(0 if you want to register as an admin and 1 if you are not an admin) 

The admin password is **/20#admin@covid**


2. ***/login*** :-

  * Only Post Request is allowed *

Takes in 2 Parameters
1. username(String)
2. password(String)

~~
if valid credentials are provided it returns an unique aceess token and refresh token else returns **{'msg': 'No user with that username or password is wrong'}**
so the users will have their unique access token and refresh token.
the access token is required to login again and in every endpoint however it is destroyed after every 5 mins
so it needes to be refreshed by the refresh token. ~~


3. **/findme:-  **
  (Access Token Required):-  
  [GET request is allowed]
  Returns their user name if the user is logged in else returns **return {'msg' :'User Does not exist'}  **

4. **/logout :- **
  (Access Token Required)
  [POST request allowed]
  Blacklists user's current access token

5.**/add  :- **
  (Access Token Required)
  [POST request is allowed]
  ### Required paramaeters:-
  
  1. home_town (type = string), throws error message if not provided (error meseeage = 'home_town must be provided')
  2. OutingNo (type = int) , throws error message if not provided
  3. RatioOut (type = int), throws error message if not provided
  4. RatioIn (type = int) ,throws error message if not provided
Adds the information in the database , if the user is admin he can add as many posts as he wants however if he is not he can provide only one information(About his own)  

6.**/refresh:-**
  [POST request is allowed]
  (Refresh token required)
  Refreshes the access token and provides a new access token











