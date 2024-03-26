from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db = SQLAlchemy(app)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    feedback = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
def first_page():
    return render_template('first_page.html')


@app.route('/add_game', methods=['POST', 'GET'])
def add_games():
    if request.method == "POST":
        title = request.form['title']
        date = request.form['date']
        feedback = request.form['feedback']

        game = Game(title=title, date=date, feedback=feedback)

        try:
            db.session.add(game)
            db.session.commit()
            return redirect('/all_games')
        except:
            return "При добавлении новой пройденной игры произошла ошибка"
    else:
        return render_template("add_game.html")


@app.route('/all_games')
def all_games():
    games = Game.query.all()
    return render_template("all_games.html", games=games)


@app.route('/all_games/<int:id>')
def game_detail(id):
    game = Game.query.get(id)
    return render_template("game_detail.html", game=game)


@app.route('/all_games/<int:id>/delete')
def game_delete(id):
    game = Game.query.get_or_404(id)

    try:
        db.session.delete(game)
        db.session.commit()
        return redirect('/all_games')
    except:
        return "При удалении статьи возникла ошибка"


@app.route('/all_games/<int:id>/update', methods=['POST', 'GET'])
def game_update(id):
    game = Game.query.get(id)
    if request.method == "POST":
        game.title = request.form['title']
        game.date = request.form['date']
        game.feedback = request.form['feedback']

        try:
            db.session.commit()
            return redirect('/all_games')
        except:
            return "При редактировании статьи произошла ошибка"
    else:
        return render_template("game_update.html", game=game)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
