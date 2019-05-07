# "Database code" for the DB Forum.

import datetime
import psycopg2
import bleach

POSTS = [("This is the first post.", datetime.datetime.now())]

def get_posts():
  """Return all posts from the 'database', most recent first."""
  database = psycopg2.connect(database='forum')
  cursor = database.cursor()
  cursor.execute("select content, time from posts order by time desc;")
  return cursor.fetchall()
  database.close()

def add_post(content):
  """Add a post to the 'database' with the current timestamp."""
  db= psycopg2.connect(database='forum')
  c = db.cursor()
  clean_value = bleach.clean(content)
  c.execute("insert into posts values(%s);", (clean_value,))
  db.commit()
  db.close()


