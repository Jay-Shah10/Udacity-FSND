#!/usr/bin/env python2
"""
This project is about testing psql queries.
This program is will answer three question as per project description.

1. what are the three most popular articles of all time?
2. Who are the most popular articles from?
3. On which days did  more than 1% of requests lead to errors?
"""
import psycopg2
import sys


def display_option():
    """
    This method is responsible for displaying options for the user.
    1-3 is for individual query search. 4 is for printing all results.
    """
    print "Please pick one of the options below. Just the number"
    print "[1] What re the most popular three articles of all time?"
    print "[2] Who are the most popular authors of all time?"
    print "[3] On which days did more than 1% of requests lead to errors? \n"
    print "[4] All of the above.\n"


def get_db_connection():
    """
    Responsible for getting a connection to postgresql database.
    :return: conn - connection object.
    """
    try:
        conn = psycopg2.connect("dbname=news")
        return conn
    except psycopg2.Error as error:
        print("Cannot connect to database %s" % error)


def get_result_of_one(conn):
    """
    Responsible for getting the result of question one.
    This is also called when user enters 1.
    :conn: - connection object.
    :return: Executes the first query and prints the answer.
    """
    cursor = conn.cursor()
    query_one = """
    SELECT articles.title, count(log.path) AS num
    FROM articles JOIN log on log.path='/article/'||articles.slug
    GROUP BY articles.title
    ORDER BY num DESC
    LIMIT 3;
    """
    cursor.execute(query_one)
    record = cursor.fetchall()
    print "Result of 1:"
    for result in record:
        # updated output format.
        print '"%s" - %d views' % (result[0], result[1])


def get_result_of_two(conn):
    """
    Prints out the result to question 2 and when the user chooses option 2.
    :conn: - connection object.
    :return: Executes the query and prints the results.
    """
    cursor = conn.cursor()
    query_two = """
    SELECT authors.name, num
    FROM authors
    JOIN (
          SELECT author, count(*) as num
          FROM articles
          INNER JOIN log ON
          log.path='/article/'||articles.slug
          GROUP BY author ORDER BY num DESC LIMIT 3
          ) as first
    ON first.author=authors.id;
    """
    cursor.execute(query_two)
    print "Result of 2: "
    record = cursor.fetchall()
    for data in record:  # updated output from suggestion.
        print '"{article}" - {views} views'.format(article=data[0],
                                                   views=data[1])


def get_result_of_three(conn):
    """
    Responsible for getting the result to question three
    and when user chooses option 3.
    :conn: connection object to database.
    :return: Executes the query and prints out the result.
    """
    cursor = conn.cursor()
    query_three = """
    SELECT sub.date, sub.error/sub.total * 100 as per
    FROM (SELECT date(log.time) as date,
         count(*) as total,
         cast(sum(cast(log.status != '200 OK' as int)) as decimal) as error
    FROM log GROUP BY date) as sub WHERE sub.error/sub.total > 0.01;
    """
    cursor.execute(query_three)
    print "Result of 3:"
    record = cursor.fetchall()
    for data in record:
        # updated output format.
        print "Date: {date} - {per} %".format(date=data[0],
                                              per=round(data[1], 2))


def get_result_of_all(conn):
    """
    Calls all other methods that execute and print out queires.
    This is ran when user choose option 4.
    :conn: connection object.
    :return: calls all other methods and prints all queries.
    """

    get_result_of_one(conn)
    print "\n"

    get_result_of_two(conn)
    print '\n'

    get_result_of_three(conn)
    print '\n'


def main():
    """
    Main
    responsible for calling other methods and passing arguements.
    Controls the overall flow of the program.
    """
    display_option()
    answer = raw_input()
    print 'selection, %s' % answer

    if int(answer) == int(1):
        conn = get_db_connection()
        get_result_of_one(conn)
        conn.close()
    elif int(answer) == int(2):
        conn = get_db_connection()
        get_result_of_two(conn)
        conn.close()
    elif int(answer) == int(3):
        conn = get_db_connection()
        get_result_of_three(conn)
        conn.close()
    elif int(answer) == int(4):
        conn = get_db_connection()
        get_result_of_all(conn)
        conn.close()
    else:
        print "Please rerun this program and" \
              " choose an option listed above. 1, 2, 3, or 4."


if __name__ == "__main__":
    main()
