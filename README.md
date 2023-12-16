# NBAPredictorProject
## By: Nick, Tom, Peter

## Overview:
Every year, millions of basketball fans root for their favorite NBA teams as they try to predict final playoffs brackets. While people usually have a sense of how good a team is based on its players, we wanted to find a way to utilize neural networks to predict the outcome of the playoffs for a given season. Therefore, for this project, we constructed a neural network capable of taking in data from the regular season of an NBA season and predicting the winner of an NBA game given 2 teams. So to emulate the playoff bracket, we simply run the model however many times we need to create a completed bracket, eventually crowning a champion.

Instructions:
1. Go to main.ipynb
2. To run the gui, run the cell containing `model, params_dict = create_model_gui()`. After running this cell, the user will be prompted to enter the number of hidden layers to implement in the neural network. Then, the user will be prompted to enter information about each hidden layer as well as the season they would like to run the model on.
3. Run the rest of the cells, obtaining the data for the specified season and training the model, up until you get to the "Predicting the Playoffs" section.
4. For the season the user specified, obtain each of the 1st round matchups, and set `team1vsteam2 = get_matchup_df(conn, "team1", "team2")`. Then, simply evaluate the model using `model.predict(team1vsteam2)` for each matchup. The output will be a number between 0-1, indicating the probability that team1 would win the game, so from there we can choose which teams will make it through to the next round.
   
https://colab.research.google.com/drive/19jMYZdXjxsBLUWcv17bFqVT2FvH3Ef0O


