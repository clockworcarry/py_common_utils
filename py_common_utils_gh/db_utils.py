from sqlalchemy import engine, text, create_engine
import pandas as pd

def list_element_exists_in_sql_table(conn, table_name, col_name, elements):
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
    
    return truth_serie

if __name__ == "__main__":
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
        print(str(gen_ex))
        