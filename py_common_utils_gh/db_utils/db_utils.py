from sqlalchemy import engine, text, create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from contextlib import contextmanager

class SqlAlchemySessionManager:
    """
    Class that stores multiple sql alchemy sessionmaker templates with an associated name in a list. Useful for apps
    that interact with multiple different databases or with one database but different parameters in some places.

    Keyword Args:
        db_url (str): url of database that the session template will be binded to 
        template_name (str): name of the session template that will be created       

    Raises:
        Exception: generic exception that is reraised. Will automatically rollback session

    Yields:
        [session]: sql alchemy session object
    """
    Sessions = []

    @contextmanager
    def session_scope(self, **kwargs): 
        if 'template_name' not in kwargs:
            raise TypeError("Missing mandatory template_name argument.")
        
        session_tpl = None
        session_tpl_tuple = next((x for x in SqlAlchemySessionManager.Sessions if x[0] == kwargs['template_name']), None)
        if session_tpl_tuple is None:
            if 'db_url' not in kwargs:
                raise TypeError("db_url argument must be provided if the session template does not already exist.")
            SqlAlchemySessionManager.Sessions.append((kwargs['template_name'], sessionmaker(bind=create_engine(kwargs['db_url']))))
            session_tpl = SqlAlchemySessionManager.Sessions[-1][1]
        else:
            session_tpl = session = session_tpl_tuple[1]

        session = session_tpl()
        try:
            yield session
            session.commit()
        except Exception as gen_ex:
            session.rollback()
            raise gen_ex
        finally:
            session.close()



"""def list_element_exists_in_sql_table(conn, table_name, col_name, elements):
    truth_serie = pd.Series()


    cur.execute(
    sql.SQL("insert into {} values (%s, %s)")
        .format(sql.Identifier('my_table')),
    [10, 20])

    for elem in elements:
        #stmt = text("SELECT :col_name FROM :table_name WHERE :col_name = :elem LIMIT 1")
        stmt = text("SELECT :col_name FROM :table_name WHERE :col_name = :elem LIMIT 1")
        stmt = stmt.bindparams(col_name=col_name, table_name=table_name, elem=elem)
        result = conn.execute(stmt).first()
        if result is not None:
            truth_serie.loc[truth_serie.index.max()+1] = elem
    
    return truth_serie"""

"""if __name__ == "__main__":
    try:
        db_url = "postgresql://postgres:navo1234@localhost:5432/test_db_utils"
        engine = create_engine(db_url, echo=False)
        with engine.connect() as conn:
            #set up
            conn.execute(text("INSERT INTO test_table_one (ticker) VALUES ('msft')"))
            conn.execute(text("INSERT INTO test_table_one (ticker) VALUES ('aapl')"))
            conn.execute(text("INSERT INTO test_table_one (ticker) VALUES ('nflx')"))
            conn.execute(text("INSERT INTO test_table_one (ticker) VALUES ('twtr')"))
            conn.execute(text("INSERT INTO test_table_one (ticker) VALUES ('fb')"))

            serie = pd.Series(['msft', 'nflx', 'aapl', 'twtr', 'fb', 'chgg', 'fsly'])
            serie_exist = list_element_exists_in_sql_table(conn, 'test_table_one', 'ticker', serie)
            
            print(serie_exist)

            #cleanup
            conn.execute(text("DELETE FROM test_table_one"))
    except Exception as gen_ex:
        print(str(gen_ex))"""
        