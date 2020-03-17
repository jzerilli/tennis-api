#Importing sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy import desc
#Instantiating sqlalchemy object

DEFAULT_HEIGHT = 170
DEFAULT_AGE = 28
DEFAULT_RANK = 1000
DEFAULT_BP_SAVED = 0
DEFAULT_BP_CONVERT = 0
DEFAULT_HAND = 0

db = SQLAlchemy()
#Creating database class
class Match(db.Model):
    __tablename__ = 'matches'
    tourney_id = db.Column(db.String(100), primary_key=True)
    tourney_name = db.Column(db.String(50))
    surface = db.Column(db.String(10))
    draw_size = db.Column(db.Integer)
    tourney_level = db.Column(db.String(1))
    tourney_date = db.Column(db.Date)
    match_num = db.Column(db.String(10))
    winner_id = db.Column(db.BigInteger)
    winner_seed = db.Column(db.String(10))
    winner_entry = db.Column(db.String(5))
    winner_name = db.Column(db.String(50))
    winner_hand = db.Column(db.String(1))
    winner_ht = db.Column(db.Integer)
    winner_ioc = db.Column(db.String(3))
    winner_age = db.Column(db.Float)
    loser_id = db.Column(db.BigInteger)
    loser_seed = db.Column(db.String(10))
    loser_entry = db.Column(db.String(5))
    loser_name = db.Column(db.String(50))
    loser_hand = db.Column(db.String(1))
    loser_ht = db.Column(db.Integer)
    loser_ioc = db.Column(db.String(5))
    loser_age = db.Column(db.Float)
    score = db.Column(db.String(50))
    best_of = db.Column(db.Integer)
    match_round = db.Column(db.String(10))
    minutes_duration = db.Column(db.Integer)
    w_ace = db.Column(db.Integer)
    w_df = db.Column(db.Integer)
    w_svpt = db.Column(db.Integer)
    w_firstin = db.Column(db.Integer)
    w_firstwon = db.Column(db.Integer)
    w_secondwon = db.Column(db.Integer)
    w_servegames = db.Column(db.Integer)
    w_bpsaved = db.Column(db.Integer)
    w_bpfaced = db.Column(db.Integer)
    l_ace = db.Column(db.Integer)
    l_df = db.Column(db.Integer)
    l_svpt = db.Column(db.Integer)
    l_1stin = db.Column(db.Integer)
    l_1stwon = db.Column(db.Integer)
    l_2ndwon = db.Column(db.Integer)
    l_svgms = db.Column(db.Integer)
    l_bpsaved = db.Column(db.Integer)
    l_bpfaced = db.Column(db.Integer)
    winner_rank = db.Column(db.Integer)
    winner_rank_points = db.Column(db.Integer)
    loser_rank = db.Column(db.Integer)
    loser_rank_points = db.Column(db.Integer)

    @classmethod    
    def get_wins_vs_opponent(cls, winner, loser):        
        return db.session.query(Match).filter(and_( 
            Match.winner_name == winner,
            Match.loser_name == loser,
        )).count()

    @classmethod    
    def get_bp_saved(cls, player):        
        loss_matches = db.session.query(Match).with_entities(Match.l_bpsaved.label('bpsaved'), Match.l_bpfaced.label('bpfaced')).filter(Match.loser_name == player)
        win_matches = db.session.query(Match).with_entities(Match.w_bpsaved.label('bpsaved'), Match.w_bpfaced.label('bpfaced')).filter(Match.winner_name == player)
        all_matches = loss_matches.union_all(win_matches).subquery()

        bp_saved =  db.session.query(func.sum(all_matches.c.bpsaved)).first()[0]
        bp_faced =  db.session.query(func.sum(all_matches.c.bpfaced)).first()[0]

        if bp_faced and bp_saved:
            return bp_saved/bp_faced
        else:
            return DEFAULT_BP_SAVED

    @classmethod    
    def get_bp_converted(cls, player):        
        win_matches = db.session.query(Match).with_entities(Match.l_bpsaved.label('bpsaved'), Match.l_bpfaced.label('bpfaced')).filter(Match.winner_name == player)
        loss_matches = db.session.query(Match).with_entities(Match.w_bpsaved.label('bpsaved'), Match.w_bpfaced.label('bpfaced')).filter(Match.loser_name == player)
        all_matches = loss_matches.union_all(win_matches).subquery()

        bp_saved =  db.session.query(func.sum(all_matches.c.bpsaved)).first()[0]
        bp_faced =  db.session.query(func.sum(all_matches.c.bpfaced)).first()[0]

        if bp_faced and bp_saved:
            return 1 - bp_saved/bp_faced
        else:
            return DEFAULT_BP_CONVERT

    @classmethod    
    def get_rank(cls, player):        
        win_date, win_rank =  db.session.query(Match).with_entities(Match.tourney_date, Match.winner_rank).filter(
            Match.winner_name == player
        ).order_by(Match.tourney_date.desc()).first()
        
        loss_date, loss_rank =  db.session.query(Match).with_entities(Match.tourney_date, Match.loser_rank).filter(
            Match.loser_name == player
        ).order_by(Match.tourney_date.desc()).first()

        if not win_date and not loss_date:
            return DEFAULT_RANK
        
        if not win_date or not loss_date:
            if win_date:
                return win_rank
            else:
                return loss_rank

        if win_date > loss_date:
            return win_rank
        else:
            return loss_rank

    @classmethod    
    def get_age(cls, player):        
        win_date, win_age =  db.session.query(Match).with_entities(Match.tourney_date, Match.winner_age).filter(
            Match.winner_name == player
        ).order_by(Match.tourney_date.desc()).first()
        
        loss_date, loss_age =  db.session.query(Match).with_entities(Match.tourney_date, Match.loser_age).filter(
            Match.loser_name == player
        ).order_by(Match.tourney_date.desc()).first()

        if not win_date and not loss_date:
            return DEFAULT_AGE
        
        if not win_date or not loss_date:
            if win_date:
                return win_age
            else:
                return loss_age

        if win_date > loss_date:
            return win_age
        else:
            return loss_age

    @classmethod    
    def get_height(cls, player):        
        win_date, win_height =  db.session.query(Match).with_entities(Match.tourney_date, Match.winner_ht).filter(
            Match.winner_name == player
        ).order_by(Match.tourney_date.desc()).first()
        
        loss_date, loss_height =  db.session.query(Match).with_entities(Match.tourney_date, Match.loser_ht).filter(
            Match.loser_name == player
        ).order_by(Match.tourney_date.desc()).first()

        if win_date:
            return win_height
        if loss_date:
            return loss_height
        else:
            return DEFAULT_HEIGHT

    @classmethod 
    def get_hand(cls, player):        
        win_hand =  db.session.query(Match).with_entities(Match.winner_hand).filter(
            Match.winner_name == player
        ).order_by(Match.tourney_date.desc()).first()
        
        loss_hand =  db.session.query(Match).with_entities(Match.loser_hand).filter(
            Match.loser_name == player
        ).order_by(Match.tourney_date.desc()).first()

        if win_hand:
            if win_hand[0] == 'R':
                return 0
            else:
                return 1
        elif loss_hand:
            if loss_hand[0] == 'R':
                return 0
            else:
                return 1
        else:
            return DEFAULT_HAND

       