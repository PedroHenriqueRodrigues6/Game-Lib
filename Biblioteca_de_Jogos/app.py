from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "biblioteca-jogos-dev"
DB = Path(__file__).with_name("biblioteca.db")

def connect():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con

def init_db():
    with connect() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS genres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            platform TEXT NOT NULL,
            release_year INTEGER,
            status TEXT NOT NULL DEFAULT 'Disponível'
              CHECK(status IN ('Disponível','Emprestado')),
            genre_id INTEGER NOT NULL,
            FOREIGN KEY (genre_id) REFERENCES genres(id)
        );
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER NOT NULL,
            borrower TEXT NOT NULL,
            loan_date TEXT NOT NULL DEFAULT CURRENT_DATE,
            return_date TEXT,
            status TEXT NOT NULL DEFAULT 'Ativo'
              CHECK(status IN ('Ativo','Devolvido')),
            FOREIGN KEY (game_id) REFERENCES games(id)
        );
        """)
        if db.execute("SELECT COUNT(*) FROM genres").fetchone()[0] == 0:
            db.executemany("INSERT INTO genres(name) VALUES (?)",
                [("Ação",),("Aventura",),("RPG",),("Esportes",),("Terror",),("Corrida",)])
            db.executemany("""INSERT INTO games(title,platform,release_year,status,genre_id)
                VALUES (?,?,?,?,?)""", [
                ("The Last of Us Part II","PlayStation 4",2020,"Disponível",2),
                ("Red Dead Redemption 2","PlayStation 4",2018,"Emprestado",2),
                ("God of War Ragnarök","PlayStation 5",2022,"Disponível",1),
                ("EA Sports FC 25","PlayStation 5",2024,"Disponível",4)
            ])
            db.execute("""INSERT INTO loans(game_id,borrower,loan_date,status)
                VALUES (2,'Carlos Mendes',date('now'), 'Ativo')""")

@app.route("/")
def index():
    with connect() as db:
        total=db.execute("SELECT COUNT(*) FROM games").fetchone()[0]
        available=db.execute("SELECT COUNT(*) FROM games WHERE status='Disponível'").fetchone()[0]
        active=db.execute("SELECT COUNT(*) FROM loans WHERE status='Ativo'").fetchone()[0]
        games=db.execute("""SELECT g.*, ge.name AS genre FROM games g
          JOIN genres ge ON ge.id=g.genre_id ORDER BY g.title""").fetchall()
    return render_template("index.html",games=games,total=total,available=available,active=active)

@app.route("/games/new",methods=["GET","POST"])
@app.route("/games/<int:game_id>/edit",methods=["GET","POST"])
def game_form(game_id=None):
    with connect() as db:
        game=db.execute("SELECT * FROM games WHERE id=?",(game_id,)).fetchone() if game_id else None
        genres=db.execute("SELECT * FROM genres ORDER BY name").fetchall()
        if request.method=="POST":
            data=(request.form["title"].strip(),request.form["platform"].strip(),
                  int(request.form["release_year"]) if request.form.get("release_year") else None,
                  request.form["status"],int(request.form["genre_id"]))
            if game_id:
                db.execute("""UPDATE games SET title=?,platform=?,release_year=?,status=?,genre_id=?
                              WHERE id=?""",(*data,game_id))
                flash("Jogo atualizado com sucesso.","success")
            else:
                db.execute("""INSERT INTO games(title,platform,release_year,status,genre_id)
                              VALUES (?,?,?,?,?)""",data)
                flash("Jogo cadastrado com sucesso.","success")
            return redirect(url_for("index"))
    return render_template("game_form.html",game=game,genres=genres)

@app.post("/games/<int:game_id>/delete")
def game_delete(game_id):
    with connect() as db:
        try:
            db.execute("DELETE FROM games WHERE id=?",(game_id,))
            flash("Jogo excluído.","success")
        except sqlite3.IntegrityError:
            flash("Não é possível excluir um jogo que possui histórico de empréstimos.","error")
    return redirect(url_for("index"))

@app.route("/genres",methods=["GET","POST"])
def genres():
    with connect() as db:
        if request.method=="POST":
            try:
                db.execute("INSERT INTO genres(name) VALUES (?)",(request.form["name"].strip(),))
                flash("Gênero cadastrado.","success")
            except sqlite3.IntegrityError:
                flash("Esse gênero já existe.","error")
            return redirect(url_for("genres"))
        rows=db.execute("""SELECT ge.*,COUNT(g.id) AS game_count FROM genres ge
          LEFT JOIN games g ON g.genre_id=ge.id GROUP BY ge.id ORDER BY ge.name""").fetchall()
    return render_template("genres.html",genres=rows)

@app.post("/genres/<int:genre_id>/delete")
def genre_delete(genre_id):
    with connect() as db:
        try:
            db.execute("DELETE FROM genres WHERE id=?",(genre_id,))
            flash("Gênero excluído.","success")
        except sqlite3.IntegrityError:
            flash("Não é possível excluir um gênero associado a jogos.","error")
    return redirect(url_for("genres"))

@app.route("/loans",methods=["GET","POST"])
def loans():
    with connect() as db:
        if request.method=="POST":
            game_id=int(request.form["game_id"])
            borrower=request.form["borrower"].strip()
            game=db.execute("SELECT * FROM games WHERE id=?",(game_id,)).fetchone()
            if not game or game["status"]!="Disponível":
                flash("Este jogo não está disponível para empréstimo.","error")
            elif not borrower:
                flash("Informe o nome de quem está retirando o jogo.","error")
            else:
                db.execute("INSERT INTO loans(game_id,borrower) VALUES (?,?)",(game_id,borrower))
                db.execute("UPDATE games SET status='Emprestado' WHERE id=?",(game_id,))
                flash("Empréstimo registrado.","success")
            return redirect(url_for("loans"))
        available=db.execute("SELECT id,title,platform FROM games WHERE status='Disponível' ORDER BY title").fetchall()
        rows=db.execute("""SELECT l.*,g.title,g.platform FROM loans l JOIN games g ON g.id=l.game_id
          ORDER BY l.id DESC""").fetchall()
    return render_template("loans.html",games=available,loans=rows)

@app.post("/loans/<int:loan_id>/return")
def return_loan(loan_id):
    with connect() as db:
        loan=db.execute("SELECT * FROM loans WHERE id=?",(loan_id,)).fetchone()
        if loan and loan["status"]=="Ativo":
            db.execute("UPDATE loans SET status='Devolvido',return_date=CURRENT_DATE WHERE id=?",(loan_id,))
            db.execute("UPDATE games SET status='Disponível' WHERE id=?",(loan["game_id"],))
            flash("Devolução registrada. Jogo disponível novamente.","success")
    return redirect(url_for("loans"))

if __name__=="__main__":
    init_db()
    app.run(debug=True)
