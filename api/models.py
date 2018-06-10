from api.app import db
from datetime import datetime
from sqlalchemy.sql import func


class CompanyProfile(db.Model):
    """
    Company Profile model
    """

    __tablename__ = 'company_profiles'

    id = db.Column(db.Integer, primary_key=True)
    company_url = db.Column(db.String(100))
    company_name = db.Column(db.String(200))
    company_email = db.Column(db.String(50))
    company_website = db.Column(db.String(50))
    company_street_address = db.Column(db.String(255))
    company_description = db.Column(db.String(3000))
    country = db.Column(db.String(50))
    industry = db.Column(db.String(100))
    company_phone_number = db.Column(db.JSON)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __repr__(self):
        return 'company_name : {}'.format(self.company_name)


class FinancialSummary(db.Model):
    """
    Financial Summary model
    """

    __tablename__ = 'financial_summaries'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company_profiles.id'))
    capital_currency = db.Column(db.String(50))
    market_cap = db.Column(db.BigInteger)
    par_value = db.Column(db.BigInteger)
    equity = db.Column(db.BigInteger)
    listing_volume = db.Column(db.BigInteger)
    listed_date = db.Column(db.DateTime)
    initial_listed_price = db.Column(db.BigInteger)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    company = db.relationship(
        'CompanyProfile', uselist=False, backref='financial_summary')

    def __repr__(self):
        return 'company_id : {}'.format(self.company_id)
        
