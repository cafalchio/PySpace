# PySpace - A Python Space Shooter

## Introduction

The game was created as a project for the course "Diploma in Software Development at Code Institute" in 2022. The requirement was to create an iteractive pure Terminal Python app deployed on a front end website. The game is a space shooter with a simple storyline. A space pilot who has to defend Earth from enemy ships. He can move his ship in all directions and shoot at the enemy ships. The game ends when the player loses all his lives. The best score is saved in a database and displayed on the website.


![PySpace](images/game_start.gif)


<a href="https://cligame.herokuapp.com" rel="nofolow">Visit and play the live version of the game here</a>


## Table of Contents

- [PySpace](#pyspace)
  - [Introduction](#introduction)
  - [Table of Contents](#table-of-contents)
  - [Strategy](#strategy)
  - [Technologies](#technologies)
  - [Features](#features)
    - [Main Page](#main-page)
    - [Options Menu](#options-menu)
    - [Rules Menu](#rules-menu)
    - [Results Menu](#results-menu)
    - [Game](#game)
  - [Testing](#testing)
  - [Unfixed Bugs](#unfixed-bugs)
  - [Features Left to Implement](#features-left-to-implement)
  - [Deployment](#deployment)
  - [Credits](#credits)
  - [Acknowledgements](#acknowledgements)


#### Strategy

- Game goal: Defend Earth from enemy ships

  - Player can move his ship in all directions
  - Can shoot at enemy ships
  - Best seven scores are saved in a database
  - Lives and score are displayed on the screen
  - Game ends when player loses all his lives


- User goals
  - Shoot at enemy ships
  - Make a high score

## Technologies

The technologies used in this project were the following:
    * HTML
    * CSS
    * JavaScript
    * Python

## Features

### Main Page

![Main page](images/main_page.png)

When the user opens the website, the page is displayed with the game title, the game description, rules and a message to press the start button to start the game.

![Game menu](images/menu.gif)

The menu is displayed in the terminal. The user can navigate through the menu with the arrow keys and press Enter key to select an option. 

### Start option

![Options Start](images/game_start.gif)

Once the user selects the start option, the game starts. 

### Records Menu

The user can select the records option to see the best seven scores saved in the database.

![Rules menu](images/records.png)

### About Menu

When the user selects the about option, a window with the game autor and version is displayed.

![Results menu](images/about.png)

### Game

The game is played on a 90x30 terminal screen. There are three enemy ships that move in random directions. 


<img src="s0.png" alt="ship 0" width="80" height="80"/>
<img src="s1.png" alt="ship 1" width="80" height="80"/>
<img src="s2.png" alt="ship 2" width="80" height="80"/>

New enemies and movement rules can be easilly added to the game. 

Each ship has a number of lives and the score will be determined 

## Testing

The website was tested on a desktop computer and a mobile phone.
Also, W3C and Jigsaw validation was used to validate the website HTML and CSS.

W3C Validation:

[W3C](assets/images/W3C.png) -->

Jigsaw Validation:

![Jigsaw](assets/images/jigsaw.png)

Jshint validator was used to validate the JavaScript code.

![Jshint](assets/images/javascript_test.png)

One warning here but was part of the implementation of the game.
Functions declared within loops referencing an outer scoped variable may lead to confusing semantics.

Lighhouse mobile and desktop testing:

![LightHouse Mobile](assets/images/lighthouse_mobile.png)

![LightHouse Desktop](assets/images/lighthouse_desktop.png)

## Unfixed Bugs

- Based on the checkers rules, the player needs to capture as many pieces as possible. The game is not programmed to do that neither to check if the player is taking the best possible move. The game is programmed to force a take.

- The computer is not programmed to take the best possible move. The computer is programmed to take a random piece.

- It was reported to crash in Android, but I was not able to reproduce the error.

## Features Left to Implement

- Implement a better AI for the computer.
- A timer to limit the time of each player.
- A smoother animation for the pieces moving.
- In the future, a multiplayer mode.

## Deployment

- The game was deployed on GitHub pages.

## Credits

- Stack Overflow
- Guido, my mentor
- w3Schools
- This channel that teaches cheker's https://www.youtube.com/watch?v=WD3NTNQElew
- developer.mozilla.org (where I passed most of my time)

## Acknowledgements

- My mentor for saving me from starting in a wrong way, which would make the project impossible to finish.
- My colleagues for the slack channel.
- The tutors for the help.
- My last hackathon team which tested the game and gave great feedbacks
