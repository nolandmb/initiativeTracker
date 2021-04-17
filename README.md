# COMBAT INITIATIVE TRACKER
#### Video Demo:  https://youtu.be/ekN48jmyDsk
#### Description:

Hello this is my cs50 final project. It is a web app designed to track the combat initiative for a game of Dungeons and Dragons or any d20 based RPG. The app will let the user add and delete characters from a data base. The user can then choose which characters are in the encounter and add them to a table using a drop down menu of their characters. Each user will only see the characters that they have created. Even if two users have a character with the same name the app know which one belongs to which user.

Clicking the roll initiative button while calculate each players initiative score by getting a random number between 1 and 20 and adding it to the players modifier. After calculating each character’s initiative score the table is sorted highest to lowest initiative score.

Sorting the table by initiative was harder than I thought. I need some help with this part, so I headed over to w3schools. Here I found some code that I could easily modified to work for this app. After a quick modification of the code my sorting was working great.

After the table is build and the players are in the list the GM can now track who turn it is. The active player is highlighted with red, bold text. Clicking the next player button with then highlight the next character in the table. If the last player in the table is active and the next player button is clicked the first player will then be highlighted and the round count will increase to show a new round has started.

The GM can also add conditions to the active player. For example, one player has been blinded. The user can select blinded from the condition dropdown box and click the add condition button. This will update the active players condition cell on the table.
The application.py file is responsible for rendering the HTML files and handling the database request.

Extras.py has a few extra functions used in applications.py. It makes sure that the user is logged in before being able to use the app. I had to get some help with the log in code from https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/ It also handles the error checking for the app.

The layout.html file contains the nav bar and other elements that are used on multiple pages. The nav bar is a bootstrap template.
The log in and register html files handles users. Log in lets and existing user log in to the app to get access to their list of character. Register sets up a new user.

The sql database contains the users and characters information. The data base also keeps track of the GM id. The GM id is what links the characters to the user. This allows the character list to be unique for each user.

The python code in the cs50 IDE is slightly different from the git hub and python anywhere code. Pythonanywhere used a different SQL version. So, when I uploaded the app to their server I had to change some syntax to make it work. With their database.



