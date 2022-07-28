"""
Models for Product

All of the models are stored in this module
"""
# from email.policy import default
import logging

# from wsgiref import validate
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# from tomlkit import boolean
# from sqlalchemy import null
# from . import app
# from tomlkit import integer
MIN_PRICE = 10.00
MAX_PRICE = 100.00
MIN_RATE = 0
MAX_RATE = 5
MAX_DESCRIPTION_LENGTH = 63
logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


# def init_db(app):
#     """Initialize the SQLAlchemy app"""
#     Product.init_db(app)
# Defining acceptable input for names and descriptions


# def acceptable_names():
#     return ["shirt", "sweater", "pants", "lounge_wear"]


# def acceptable_description():
#     return ["unavailable", "Relaxed Fit", "Slim Fit"]


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class Product(db.Model):
    """
    Class that represents a product
    """

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False, unique=True)
    description = db.Column(
        db.String(MAX_DESCRIPTION_LENGTH),
        nullable=False,
        server_default=("unavailable"),
    )
    category = db.Column(db.String(63), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    available = db.Column(db.Boolean(), nullable=False, default=False)
    rating = db.Column(db.Float, nullable=True)
    no_of_users_rated = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return "<Product %r id=[%s]>" % (self.name, self.id)

    def create(self):
        """
        Creates a product to the database
        """
        try:
            logger.info("Creating %s", self.name)
            self.id = None  # id must be none to generate next primary key
            db.session.add(self)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            # raise DataValidationError(error.args[0])
            if "UniqueViolation" in error.args[0]:
                raise DataValidationError(f"Error: name {self.name} already exists!")
            elif "NotNullViolation" in error.args[0]:
                raise DataValidationError(f"Error: Some none-null vaiable not provided. {error.args[0]}")
            else:
                raise DataValidationError("Error: Something happened when creating new product.")

    def update(self):
        """
        Updates a Product to the database
        """
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """Removes a product from the data store"""
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self) -> dict:
        """Serializes a product into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "price": self.price,
            "available": self.available,
            "rating": self.rating,
            "no_of_users_rated": self.no_of_users_rated,
        }

    def check_price(self, price):
        if isinstance(price, float) or isinstance(price, int):
            price = float(price)
            if price >= MIN_PRICE and price <= MAX_PRICE:
                self.price = price
            else:
                raise DataValidationError("Invalid range for [price]: " + str(price))
        else:
            raise DataValidationError(
                "Invalid type for float [price]: " + str(type(price))
            )

    def check_available(self, available):
        if isinstance(available, bool):
            self.available = available
        else:
            raise DataValidationError(
                "Invalid type for boolean [available]: " + str(type(available))
            )

    def check_rating(self, rating):
        if rating is not None:
            if isinstance(rating, float) or isinstance(rating, int):
                rating = float(rating)
                if rating >= MIN_RATE and rating <= MAX_RATE:
                    self.rating = rating
                else:
                    raise DataValidationError(
                        "Invalid range for [rating]: " + str(rating)
                    )
            else:
                raise DataValidationError(
                    "Invalid type for [rating]: " + str(type(rating))
                )
        else:
            self.rating = None

    def check_no_of_users_rated(self, no_of_users_rated):
        if isinstance(no_of_users_rated, int):
            if no_of_users_rated >= 0:
                self.no_of_users_rated = no_of_users_rated
            else:
                raise DataValidationError(
                    "Invalid Range for [no_of_users_rated]: "
                    + str(no_of_users_rated)
                )
        else:
            raise DataValidationError(
                "Invalid Type for [no_of_users_rated]: "
                + str(type(no_of_users_rated))
            )

    def check_name(self, name):
        if not isinstance(name, str):
            raise TypeError
        else:
            self.name = name

    def check_description(self, description):
        if not isinstance(description, str):
            raise TypeError
        else:
            self.description = description

    def check_category(self, category):
        if not isinstance(category, str):
            raise TypeError
        else:
            self.category = category

    def deserialize(self, data: dict):
        """
        Deserializes a product from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            if "name" in data:
                self.check_name(data["name"])
            if "description" in data:
                self.check_description(data["description"])
            if "category" in data:
                self.check_category(data["category"])
            if "price" in data:
                self.check_price(data["price"])
            if "available" in data:
                self.check_available(data["available"])
            if "rating" in data:
                self.check_rating(data["rating"])
            if "no_of_users_rated" in data:
                self.check_no_of_users_rated(data["no_of_users_rated"])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Product: body of request contained bad or no data - "
                "Error message: " + str(error)
            )
        return self

    ##################################################
    # CLASS METHODS
    ##################################################
    @classmethod
    def init_db(cls, app: Flask):
        """Initializes the database session

        :param app: the Flask app
        :type data: Flask

        """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """Returns all of the products in the database"""
        logger.info("Processing all products")
        return cls.query.all()

    @classmethod
    def find(cls, product_id: int):
        """Find a Product by it's id

        :param product_id: the id of the Product to find
        :type product_id: int

        :return: an instance with the product_id, or 404_NOT_FOUND if not found
        :rtype: Product

        """
        logger.info("Processing lookup for id %s ...", product_id)
        return cls.query.get(product_id)

    @classmethod
    def find_or_404(cls, product_id: int):
        """Find a Product by it's id
        :param product_id: the id of the Pet to find
        :type product_id: int
        :return: an instance with the product_id, or 404_NOT_FOUND if not found
        :rtype: Product
        """
        logger.info("Processing lookup or 404 for id %s ...", product_id)
        return cls.query.get_or_404(product_id)

    @classmethod
    def find_by_name(cls, name: str) -> list:
        """Returns all products with the given name
        Args:
        name (string): the name of the products you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_rating(cls, rating: float) -> list:
        """Returns all Products by their rating

        :param rating: ratings can be inrange from [1,5]
        :type available: float

        :return: a collection of Products with equal or greater rating we want
        :rtype: list

        """
        logger.info("Processing rating query for %s ...", rating)
        return cls.query.filter(cls.rating >= rating)

    @classmethod
    def find_by_category(cls, category: str) -> list:
        """Returns all of the Products in a category

        :param category: the category of the Products you want to match
        :type category: str

        :return: a collection of Products in that category
        :rtype: list

        """
        logger.info("Processing category query for %s ...", category)
        return cls.query.filter(cls.category == category)

    @classmethod
    def find_by_price(cls, price: float) -> list:
        """Returns all Products by their price

        :param price: values are float number
        :type available: float

        :return: a collection of Products with equal or less price we want
        :rtype: list

        """
        logger.info("Processing price query for %s ...", price)
        return cls.query.filter(cls.price <= price)

    @classmethod
    def find_by_availability(cls) -> list:
        """Returns all the products that are currently available

        Returns:
            list: returns the list of currently available products
        """
        logger.info("Processing availability query")
        return cls.query.filter(cls.available)
