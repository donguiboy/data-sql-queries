# pylint: disable=C0103, missing-docstring
import sqlite3

conn = sqlite3.connect('data/movies.sqlite')

db1 = conn.cursor()

def detailed_movies(db):
    '''return the list of movies with their genres and director name'''
    query = """
    SELECT title, genres, name
    FROM movies
    JOIN directors ON movies.director_id = directors.id
    """
    db.execute(query)
    results = db.fetchall()
    return results

def late_released_movies(db):
    '''return the list of all movies released after their director death'''
    query = """SELECT title
    FROM movies
    JOIN directors ON movies.director_id = directors.id
    WHERE start_year > death_year
    """
    db.execute(query)
    results = db.fetchall()
    movie_list = []
    for row in results:
        movie_list.append(row[0])
    return movie_list

def stats_on(db, genre_name):#DONE
    query= """SELECT genres, count(id) as number_of_movies, round(avg(minutes),2) Avg_lenght
    FROM movies m
    where upper(genres) = upper(?)
    Group by genres"""
    db.execute(query,(genre_name,))
    results = db.fetchone()
    stat_dict = {"genre":results[0],"number_of_movies":results[1],"avg_length":results[2]}
    return stat_dict

def top_five_directors_for(db, genre_name):
    '''return the top 5 of the directors with the most movies for a given genre'''
    query = """SELECT d.name, count(m.title) as number_movies
    FROM directors d
    Join movies m on m.director_id  = d.id
    WHERE upper(m.genres) like ?
    GROUP by d.name, m.genres
    Order by number_movies desc
    Limit 5"""
    db.execute(query,(genre_name,))
    results = db.fetchall()
    return results

def movie_duration_buckets(db):
    '''return the movie counts grouped by bucket of 30 min duration'''
    query ="""SELECT (minutes/30+1)*30 time_range, COUNT(*)
FROM movies
WHERE minutes IS NOT NULL
GROUP BY time_range
"""
    db.execute(query)
    results = db.fetchall()
    return results


def top_five_youngest_newly_directors(db):
    '''return the top 5 youngest directors when they direct their first movie'''
    query = """SELECT d.name, m.start_year - d.birth_year  as age
            FROM movies m
            left join directors d on d.id=m.director_id
            WHERE d.birth_year IS NOT NULL
            ORDER BY m.start_year-birth_year  asc, birth_year asc
            limit 5
            """
    db.execute(query)
    results = db.fetchall()
    return results
