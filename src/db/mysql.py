#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pymysql


def get_con():
    return pymysql.Connect('127.0.0.1', 'root', 'root', 'douban')


def add_book(_id, book_name, tags, intro, rating, url):
    connection = get_con()
    cursor = connection.cursor()

    sql = """insert into books(id, book_name, tags, intro, rating, url) values (%s, "%s", "%s", "%s", %s, "%s")""" \
          % (_id, book_name, tags, intro, rating, url)

    try:
        cursor.execute(sql)
        connection.commit()
    except Exception as e:
        # log("sql执行异常:", e)
        connection.rollback()

    connection.close()


def add_tag(name):
    connection = get_con()
    cursor = connection.cursor()

    sql = """insert into tags(name, done, page_start) values ("%s", %s, 0)""" % (name, 0)

    try:
        cursor.execute(sql)
        connection.commit()
    except Exception as e:
        # log("sql执行异常:", e)
        connection.rollback()

    connection.close()


def update_tag_start(name, start):
    connection = get_con()
    cursor = connection.cursor()

    sql = """update tags set page_start = %s where name = "%s" """ % (start, name)

    try:
        cursor.execute(sql)
        connection.commit()
    except Exception as e:
        # log("sql执行异常:", e)
        connection.rollback()

    connection.close()


def update_tag_done(name):
    connection = get_con()
    cursor = connection.cursor()

    sql = """update tags set done = %s where name = "%s" """ % (1, name)

    try:
        cursor.execute(sql)
        connection.commit()
    except Exception as e:
        # log("sql执行异常:", e)
        connection.rollback()

    connection.close()


def find_todo_tags(done):
    connection = get_con()
    cursor = connection.cursor()

    sql = """select name, page_start from tags where done = %s """ % done

    cursor.execute(sql)
    data = cursor.fetchall()
    connection.close()

    return data


def has_tag(tag):
    connection = get_con()
    cursor = connection.cursor()

    sql = """select id from tags where name = "%s" """ % tag

    cursor.execute(sql)
    data = cursor.fetchall()
    connection.close()

    return len(data) > 0
