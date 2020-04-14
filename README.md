# tennis-api

This is an api to predict the winner of a ATP Tour match. It was made using Flask, Sqlalchemy, and XGBoost.

The api is currently being hosted at https://tennis-prediction-api.herokuapp.com

example usage of the api at https://tennis-match-predictor.herokuapp.com/

### Current features

GET https://tennis-prediction-api.herokuapp.com/players
- output: list of all players supported by the model.  The model has been trained on the past decade or so of ATP tour matches

GET https://tennis-prediction-api.herokuapp.com/?p1=PLAYER1&p2=PLAYER2&surface=SURFACE
- inputs: p1: the name of the first player in the matchup
          p2: the name of the second player in the matchup
          surface: the surface the match is being played on. Accepted surfaces are Clay, Grass, and Hard
          
- returns: {"p1_name": "PLAYER1", "p1_win_prob": "x", "p2_name": "PLAYER2", "p2_win_prob": "1-x"}
  where the win probabilites are floats between 0 and 1 such that both add to 1.
  
 
 ### Planned features:
 - More inputs for predictons like such as the round of the match played or tournament
 - Player statistics searchable by name in order to get a better idea of why one player is favored over the other
