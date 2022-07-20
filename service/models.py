"""
Models for Product

All of the models are stored in this module
"""
import logging

# from wsgiref import validate
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# from tomlkit import integer
logger = logging.getLogger("flask.app")
MIN_PRICE = 10.00
MAX_PRICE = 100.00
MIN_RATE = 0
MAX_RATE = 5
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
    name = db.Column(db.String(63), nullable=False)
    description = db.Column(
        db.String(63), nullable=False, server_default=("unavailable")
    )
    category = db.Column(db.String(63), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    available = db.Column(db.Boolean(), nullable=False, default=False)
    rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Product %r id=[%s]>" % (self.name, self.id)

    def create(self):
        """
        Creates a product to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

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
        }

    def deserialize(self, data: dict):
        """
        Deserializes a product from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.description = data["description"]
            self.category = data["category"]
            if isinstance(data["price"], float):
                if data["price"] >= MIN_PRICE and data["price"] <= MAX_PRICE:
                    self.price = data["price"]
                else:
                    raise DataValidationError(
                        "Invalid range for [price]: " + str(data["price"])
                    )
            else:
                raise DataValidationError(
                    "Invalid type for float [price]: " + str(type(data["price"]))
                )
            if isinstance(data["available"], bool):
                self.available = data["available"]
            else:
                raise DataValidationError(
                    "Invalid type for boolean [available]: "
                    + str(type(data["available"]))
                )
            if isinstance(data["rating"], int):
                if data["rating"] >= MIN_RATE and data["rating"] <= MAX_RATE:
                    self.rating = data["rating"]
                else:
                    raise DataValidationError(
                        "Invalid range for [rating]: " + str(data["rating"])
                    )
            else:
                raise DataValidationError(
                    "Invalid type for [rating]: " + str(type(data["rating"]))
                )
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0])
        except KeyError as error:
            raise DataValidationError("Invalid product: missing " + error.args[0])
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
    def find_by_rating(cls, rating: int) -> list:
        """Returns all Products by their rating

        :param rating: values are [1, 2, 3, 4, 5]
        :type available: int

        :return: a collection of Products with equal or greater rating we want
        :rtype: list

        """
        logger.info("Processing rating query for %s ...", rating)
        return cls.query.filter(cls.rating >= int(rating))
