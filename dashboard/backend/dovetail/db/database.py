##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import logging
import functools

from threading import local

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from contextlib import contextmanager
from dovetail.db import exception
from dovetail.db import models

ENGINE = None
SESSION = sessionmaker(autocommit=False, autoflush=False)
SCOPED_SESSION = None
SESSION_HOLDER = local()

SQLALCHEMY_DATABASE_URI = "mysql://root:%s@localhost:3306/dovetail" % ('root')


def init(database_url=None):
    """Initialize database.

    :param database_url: string, database url.
    """
    global ENGINE
    global SCOPED_SESSION
    if not database_url:
        database_url = SQLALCHEMY_DATABASE_URI
    logging.info('init database %s', database_url)
    print("database init %s" % database_url)
    ENGINE = create_engine(
        database_url, convert_unicode=True,
        poolclass=StaticPool
    )
    SESSION.configure(bind=ENGINE)
    SCOPED_SESSION = scoped_session(SESSION)
    models.BASE.query = SCOPED_SESSION.query_property()


def in_session():
    """check if in database session scope."""
    bool(hasattr(SESSION_HOLDER, 'session'))


@contextmanager
def session(exception_when_in_session=True):
    """database session scope.

    To operate database, it should be called in database session.
    If not exception_when_in_session, the with session statement support
    nested session and only the out most session commit/rollback the
    transaction.
    """
    if not ENGINE:
        init()

    nested_session = False
    if hasattr(SESSION_HOLDER, 'session'):
        if exception_when_in_session:
            logging.error('we are already in session')
            raise exception.DatabaseException('session already exist')
        else:
            new_session = SESSION_HOLDER.session
            nested_session = True
            logging.log(
                logging.DEBUG,
                'reuse session %s', nested_session
            )
    else:
        new_session = SCOPED_SESSION()
        setattr(SESSION_HOLDER, 'session', new_session)
        logging.log(
            logging.DEBUG,
            'enter session %s', new_session
        )
    try:
        yield new_session
        if not nested_session:
            new_session.commit()
    except Exception as error:
        if not nested_session:
            new_session.rollback()
            logging.error('failed to commit session')
        logging.exception(error)
        if isinstance(error, IntegrityError):
            for item in error.statement.split():
                if item.islower():
                    object = item
                    break
            raise exception.DuplicatedRecord(
                '%s in %s' % (error.orig, object)
            )
        elif isinstance(error, OperationalError):
            raise exception.DatabaseException(
                'operation error in database'
            )
        elif isinstance(error, exception.DatabaseException):
            raise error
        else:
            raise exception.DatabaseException(str(error))
    finally:
        if not nested_session:
            new_session.close()
            SCOPED_SESSION.remove()
            delattr(SESSION_HOLDER, 'session')
        logging.log(
            logging.DEBUG,
            'exit session %s', new_session
        )


def current_session():
    """Get the current session scope when it is called.

       :return: database session.
       :raises: DatabaseException when it is not in session.
    """
    try:
        return SESSION_HOLDER.session
    except Exception as error:
        logging.error('It is not in the session scope')
        logging.exception(error)
        if isinstance(error, exception.DatabaseException):
            raise error
        else:
            raise exception.DatabaseException(str(error))


def run_in_session(exception_when_in_session=True):
    """Decorator to make sure the decorated function run in session.

    When not exception_when_in_session, the run_in_session can be
    decorated several times.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                my_session = kwargs.get('session')
                if my_session is not None:
                    return func(*args, **kwargs)
                else:
                    with session(
                        exception_when_in_session=exception_when_in_session
                    ) as my_session:
                        kwargs['session'] = my_session
                        return func(*args, **kwargs)
            except Exception as error:
                logging.error(
                    'got exception with func %s args %s kwargs %s',
                    func, args, kwargs
                )
                logging.exception(error)
                raise error
        return wrapper
    return decorator


@run_in_session()
def create_db(session=None):
    """Create database."""
    models.BASE.metadata.create_all(bind=ENGINE)
    print('create_db')


def drop_db():
    """Drop database."""
    models.BASE.metadata.drop_all(bind=ENGINE)
