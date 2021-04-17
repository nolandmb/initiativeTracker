# COMBAT INITIATIVE TRACKER
#### Video Demo:  https://youtu.be/ekN48jmyDsk
#### Description:web app to track the combat initiative for a game of Dungeons and Dragons

For my final project I made a web app to track the combat initiative for a game of Dungeons and Dragons. The app will let the user added and delete characters from a data base. Then they can choose which characters are in the encounter and add them to a table. After calculating each character’s initiative score the table is sorted highest to lowest.
The application.py file is responsible for rendering the HTML files and handling the database request. It will also allow for multiple users to have characters of the same name. For example, if user a has a character named Luke in the data base It will also let user b have a Luke character. It will not list them as the same character. When using the app, it will only pull the characters that belong to the currently logged in user.
Extras.py has a few extra functions used in applications.py. It makes sure that the user is logged in before being able to use the app. It also handles the error checking for the app.
The layout.html file contains the nav bar and other elements that are used on multiple pages.
The log in and register html files handle users. Log in lets and existing user log in to the app to get access to their characters. Register sets up a new user.
The index page is where most everything happens. Python is not used on this page for the initiative tracking. Javascript handles the dynamics of this page. The user can add and delete characters to the initiative list. They will be able to add a condition to the active player. Clicking roll initiative will generate a random number that is added to the characters modifier for a total initiative score. The table is then sorted from highest to lowest initiative score. The user can iterate through the players and it will highlight the active player. If the active player is the last player in the list clicking on the next player button will activate the first player in the list and increase the round by one.
The sql database contains the users and characters information. The python code in the cs50 IDE is slightly different from the git hub and python anywhere code. Pythonanywhere used a differet SQL version so I had to change some syntax to make it work.

project can be found at
nolandmb.pythonanywhere.com


