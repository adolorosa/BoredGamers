from boredgamers import db
from boredgamers.models import Game
import csv


def upload_games_data():

    with open ('bgg_sample.csv', 'r') as games_data:
        data = csv.DictReader(games_data)

        for row in data:
            game = Game(
                id=row['game_id'], rank=row['rank'], bgg_url=row['bgg_url'], name=row['names'], min_players=row['min_players'], 
                max_players='max_players', average_time=row['avg_time'], min_time=row['min_time'], max_time=row['max_time'], 
                year=row['year'], average_rating=row['avg_rating'], geek_rating=row['geek_rating'], num_votes=row['num_votes'], 
                image_url=row['image_url'], age=row['age'], mechanic=row['mechanic'], owned=row['owned'], category=row['category'], 
                designer=row['designer']
            )
            db.session.add(game)
            db.session.commit()

upload_games_data()