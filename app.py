from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

from base import Match, db

app = Flask(__name__)
api = Api(app)

app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://localhost/jackzerilli"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True 

db.init_app(app)
app.app_context().push()

parser = reqparse.RequestParser()
parser.add_argument('p1')
parser.add_argument('p2')
parser.add_argument('surface')
parser.add_argument('round')
parser.add_argument('level')


class PredictMatch(Resource):
    def get(self):
        # use parser and find the user's query
        args = parser.parse_args()
        player1 = args['p1']
        player2 = args['p2']
        match_round = args['round']
        surface = args['surface']
        level = args['level']

        print(Match.get_bp_converted(player1))
        output = Match.get_wins_vs_opponent(player1, player2)

        # vectorize the user's query and make a prediction

        # create JSON object
        # output = {'prediction': pred_text, 'confidence': confidence}
        # output = 'hello'
        
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
    app.run(debug=True)