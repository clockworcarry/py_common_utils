from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *
from sqlalchemy.schema import *
from db_utils import *
import pytest

meta = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
      })

Base = declarative_base(metadata=meta)

class TestTableOne(Base):
    __tablename__ = 'test_table_one'

    id = Column(Integer, primary_key=True)
    ticker = Column(String(5), nullable=False, unique=True)

class TestTableThree(Base):
    __tablename__ = 'test_table_three'

    id = Column(Integer, primary_key=True)
    age = Column(Integer)

def test_sql_alch_session_manager():
    manager = SqlAlchemySessionManager()

    with pytest.raises(Exception) as execinfo: 
        with manager.session_scope() as session:
            pass
    
    assert str(execinfo.typename) == 'TypeError'
    assert execinfo.value.args[0] == 'Missing mandatory template_name argument.'

    
    with pytest.raises(Exception) as execinfo: 
        with manager.session_scope(db_url='postgresql://postgres:navo1234@localhost:5432/test_db_utils') as session:
            pass

    assert str(execinfo.typename) == 'TypeError'
    assert execinfo.value.args[0] == 'Missing mandatory template_name argument.'

    
    with pytest.raises(Exception) as execinfo: 
        with manager.session_scope(template_name='basic') as session:
            pass

    assert str(execinfo.typename) == 'TypeError'
    assert execinfo.value.args[0] == 'db_url argument must be provided if the session template does not already exist.'

    
    with manager.session_scope(db_url='postgresql://postgres:navo1234@localhost:5432/test_db_utils', template_name='basic') as session:
        session.query(TestTableOne).delete()
        session.commit()
        obj = TestTableOne(ticker='NVDA')
        session.add(obj)

    
    with manager.session_scope(template_name='basic') as session:
        db_obj = session.query(TestTableOne).all()
        assert len(db_obj) == 1
        assert db_obj[0].ticker == 'NVDA'

    #will return same session as before even if diff url specified because tpl name si the same
    with manager.session_scope(db_url='postgresql://postgres:navo1234@localhost:5432/test_db_utils2', template_name='basic') as session:
        db_obj = session.query(TestTableOne).all()
        assert len(db_obj) == 1
        assert db_obj[0].ticker == 'NVDA'

    
    with manager.session_scope(db_url='postgresql://postgres:navo1234@localhost:5432/test_db_utils2', template_name='new') as session:
        db_obj = session.query(TestTableThree).all()
        assert len(db_obj) == 0


    with manager.session_scope(template_name='new') as session:
        session.query(TestTableThree).delete()
        session.commit()
        obj = TestTableThree(age=20, id=1)
        session.add(obj)

    with manager.session_scope(template_name='new') as session:
        db_obj = session.query(TestTableThree).all()
        assert len(db_obj) == 1
        assert db_obj[0].age == 20

    #recheck all good still
    with manager.session_scope(template_name='basic') as session:
        db_obj = session.query(TestTableOne).all()
        assert len(db_obj) == 1
        assert db_obj[0].ticker == 'NVDA'

