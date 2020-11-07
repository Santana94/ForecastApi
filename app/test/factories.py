import factory
import factory.fuzzy as fuzzy

from sqlalchemy import Column, Integer, String, create_engine, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('sqlite://')
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()


class Forecast(Base):
    """ Forecast Model for storing requested forecast information """
    __tablename__ = "forecast"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    city = Column(String(255), nullable=True)
    state = Column(String(255), nullable=True)
    country = Column(String(255), nullable=True)
    date = Column(DateTime, nullable=True)
    rain_probability = Column(Float, nullable=True)
    rain_precipitation = Column(Float, nullable=True)

    def __repr__(self):
        return f"<Forecast '{self.city}' - '{self.id}' >"


Base.metadata.create_all(engine)


class ForecastFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Forecast
        sqlalchemy_session = session

    id = factory.Sequence(lambda n: n)
    city = factory.Faker('name')
    state = factory.Faker('name')
    country = factory.Faker('name')
    rain_probability = fuzzy.FuzzyFloat(1.23)
    rain_precipitation = fuzzy.FuzzyFloat(20.42)
