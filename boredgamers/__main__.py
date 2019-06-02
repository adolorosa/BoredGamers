from boredgamers import db, app
from boredgamers.models import User, Game
import argparse
import csv


# parse arguments:
parser = argparse.ArgumentParser()
parser.add_argument("action", help="""
Type \'python3 -m boredgamers init_db\' to initialize the database\n
    or \'python3 -m boredgamers upload_games\' to populate the database with games data\n
    or \'python3 boredgamers run_app\' to start the server
        """)
args = parser.parse_args()



# populate the database with games data:
def upload_games_data():

    exists = Game.query.filter_by(id=Game.id).first()
    iterations_count = 0

    with open ('bgg_sample.csv', 'r') as games_data:
        data = csv.DictReader(games_data)

        for row in data:
            if not exists:
                game = Game(
                    id=row['game_id'], rank=row['rank'], bgg_url=row['bgg_url'], name=row['names'], min_players=row['min_players'], 
                    max_players='max_players', average_time=row['avg_time'], min_time=row['min_time'], max_time=row['max_time'], 
                    year=row['year'], average_rating=row['avg_rating'], geek_rating=row['geek_rating'], num_votes=row['num_votes'], 
                    image_url=row['image_url'], age=row['age'], mechanic=row['mechanic'], owned=row['owned'], category=row['category'], 
                    designer=row['designer']
                )
                db.session.add(game)
                iterations_count += 1
                if iterations_count == 10:
                    db.session.commit()
                    iterations_count = 0


# assign the command line arguments to their functions:
def do_sth(args):
    action = args.action
    if action == "init_db":
        db.create_all()
    elif action == "upload_games":
        upload_games_data()
    elif action == "run_app":
        if __name__ == "__main__":
            app.run(debug=True)
    else:
        print("""
        Use either \'python3 -m boredgamers init_db\'\n
            or \'python3 -m boredgamers upload_games\'\n
            or \'python3 -m boredgamers run_app\'
                """)

do_sth(args)