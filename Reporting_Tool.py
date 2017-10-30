#!/usr/bin/env python2

import psycopg2


def db_connect():
    """ Creates and returns a connection to the database defined by DBNAME,
        as well as a cursor for the database.

        Returns:
            db, c - a tuple. The first element is a connection to the database.
                    The second element is a cursor for the database.
    """
    try:
        db = psycopg2.connect("dbname=news")  # Connect to database
        c = db.cursor()  # Create cursor
        return db, c
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def main():
    print("\n")
    print 'Welcome to the Reporting Tool!'
    print("\n")


def reports():
    """Function will ask and collect answer
    from user on what report wants to run."""
    print 'Please select the report you want to check:'
    print 'For Most read articles enter 1'
    print 'For Most read authors enter 2'
    print 'For Most read articles enter 3'
    print 'For ALL the reports enter All'
    global user_answer
    user_answer = raw_input('Your selection: ').lower()
    if user_answer == '1':
        print most_read_articles()
        return ask_user_again()
    if user_answer == '2':
        print most_read_authors()
        return ask_user_again()
    if user_answer == '3':
        print errors_by_day()
        return ask_user_again()
    if user_answer == 'all':
        print all_reports()
        return ask_user_again()
    else:
        print 'Invalid option'
        print '\n'
        return reports()


def most_read_articles():
    """Function will contact DB and print out Most Read Articles information.
    Once done will ask if further reports are needed"""
    db, c = db_connect()
    c.execute(
        "select * from most_read;"
        )
    most_read = c.fetchall()
    db.close()
    print("\n")
    print 'Most Read Articles'
    for res in most_read:
        print "Article", res[0], "-----> Total Views", res[1]
    print("\n")


def most_read_authors():
    """Function will contact DB and print out Most Read Authors information."""
    db, c = db_connect()
    c.execute(
        "select * from popular_authors;"
        )
    popular_authors = c.fetchall()
    db.close()
    print("\n")
    print 'Most Read Authors'
    for auth in popular_authors:
        print "Author", auth[0], "-----> Total Reads", auth[1]
    print("\n")


def errors_by_day():
    """Function will contact DB and print out days where the errors
    where over 1% of the total views."""
    db, c = db_connect()
    c.execute(
        "select * from error_over_one;"
        )
    error_over_one = c.fetchall()
    db.close()
    print("\n")
    print 'Errors over 1%'
    for error in error_over_one:
        print "Day", error[0], "----->", error[1], "%"
    print("\n")


def all_reports():
    """Function will contact DB and print out all three reports"""
    most_read_articles()
    most_read_authors()
    errors_by_day()


def ask_user_again():
    """Function will ask if further reports are needed, if so
    will return to report selection or close connection"""
    print'Do you want to check another report? (Yes / No)'
    ask_user_again_answer = raw_input().lower()
    if ask_user_again_answer == 'yes':
        print '\n'
        return reports()
    if ask_user_again_answer == 'no':
        print("\n")
        print 'Thank you for using the reporting tool.'
        print 'Have a good day!'
        print '\n'
    else:
        print 'Invalid selection, please try again.'
        print '\n'
        return ask_user_again()

if __name__ == '__main__':
    main()

reports()
