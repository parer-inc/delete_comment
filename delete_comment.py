"""This service allows to delete comment from db"""
import os
import sys
import time
import MySQLdb
from rq import Worker, Queue, Connection
from methods.connection import get_redis, get_cursor

r = get_redis()

def delete_comment(id):
    """Deletes comment from db (table comments)"""
    cursor, db = get_cursor()
    if not cursor or not db:
        # log that failed getting cursor
        return False
    q = f"DELETE FROM comments WHERE id='{id}'"
    try:
        cursor.execute(q)
    except MySQLdb.Error as error:
        print(error)
        # Log
        return False
        # sys.exit("Error:Failed to delete a comment")
    db.commit()
    return True


if __name__ == '__main__':
    q = Queue('delete_comment', connection=r)
    with Connection(r):
        worker = Worker([q], connection=r,  name='delete_comment')
        worker.work()
