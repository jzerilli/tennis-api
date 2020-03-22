from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import xgboost as xgb
import numpy as np
from base import Match, db
import os

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True 

db.init_app(app)
app.app_context().push()

parser = reqparse.RequestParser()
parser.add_argument('p1')
parser.add_argument('p2')
parser.add_argument('surface')

bst = xgb.Booster()  # init model
bst.load_model('final.model')  # load data



class PredictMatch(Resource):
    def get(self):
        args = parser.parse_args()
        player1 = args['p1']
        player2 = args['p2']
        surface = args['surface']
        player1_stats = Match.get_rank(player1), Match.get_age(player1), Match.get_height(player1), Match.get_serve_in(player1), Match.get_ace(player1), Match.get_bp_saved(player1), Match.get_serve_won(player1), Match.get_bp_converted(player1), Match.get_return_won(player1), Match.get_wins_pct(player1, None, True), Match.get_wins_pct(player1, surface, True), Match.get_wins_pct(player1, None, False), Match.get_wins_pct(player1, surface, False), Match.get_wins_vs_opponent(player1, player2), Match.get_wins_vs_opponent(player1, player2, surface)
        player2_stats = Match.get_rank(player2), Match.get_age(player2), Match.get_height(player2), Match.get_serve_in(player2), Match.get_ace(player2), Match.get_bp_saved(player2), Match.get_serve_won(player2), Match.get_bp_converted(player2), Match.get_return_won(player2), Match.get_wins_pct(player2, None, True), Match.get_wins_pct(player2, surface, True), Match.get_wins_pct(player1, None, False), Match.get_wins_pct(player1, surface, False), Match.get_wins_vs_opponent(player2, player1), Match.get_wins_vs_opponent(player2, player1, surface)
        
        prediction_data = []
        for i in range(15):
            prediction_data.append(player1_stats[i] - player2_stats[i])

        prediction_data = np.array(prediction_data)
        dtest = xgb.DMatrix(np.asmatrix(prediction_data))
        win_probability = bst.predict(dtest)[0]

        output = {'p1_name': player1, 'p1_win_prob': str(win_probability),
                    'p2_name': player2, 'p2_win_prob': str(1 - win_probability)}


        print(output)
        return output

class PlayerList(Resource):
    def get(self):
        #return a list of players, rankings, etc
        return "player list"


# Setup the Api resource routing here
# Route the URL to the resource
api.add_resource(PredictMatch, '/')
api.add_resource(PlayerList, '/players')

if __name__ == '__main__':
    app.run()