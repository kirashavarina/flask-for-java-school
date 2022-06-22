import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_album(album_id):
    conn = get_db_connection()
    album = conn.execute('SELECT * FROM albums WHERE id = ?',
                        (album_id,)).fetchone()
    conn.close()
    if album is None:
        abort(404)
    return album

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'

@app.route('/')
def index():
    conn = get_db_connection()
    albums = conn.execute('SELECT * FROM albums').fetchall()
    conn.close()
    return render_template('index.html', albums=albums)
    
@app.route('/<int:album_id>')
def album(album_id):
    album = get_album(album_id)
    return render_template('album.html', album=album)
    
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year_album = request.form['year_album']

        if not title:
            flash('Title is required!')
        elif not author:
            flash('Author is required!')
        elif not year_album:
            flash('Year of the album is required!')
        #elif not isinstance(year_album, int):
            #flash('Year of the album must be number!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO albums (title, author, year_album) VALUES (?, ?, ?)',
                         (title, author, year_album))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')
    
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    album = get_album(id)

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year_album = request.form['year_album']

        if not title:
            flash('Title is required!')
        elif not author:
            flash('Author is required!')
        elif not year_album:
            flash('Year of the album is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE albums SET title = ?, author = ?, year_album = ?'
                         ' WHERE id = ?',
                         (title, author, year_album, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', album=album)
    
@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    album = get_album(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM albums WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(album['title']))
    return redirect(url_for('index'))