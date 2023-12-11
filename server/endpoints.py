"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from http import HTTPStatus

from flask import Flask, request
from flask_restx import Resource, Api, fields

import werkzeug.exceptions as wz

import data.categories as categ
import data.users as users
import data.nutrition as nutrition
import data.ems as ems

app = Flask(__name__)
api = Api(app)

DELETE = 'delete'
DEFAULT = 'Default'
MENU = 'menu'
MAIN_MENU_EP = '/MainMenu'
MAIN_MENU_NM = "Welcome to Jack-of-All-Trades!"
HELLO_EP = '/hello'
HELLO_RESP = 'hello'
CATEGORIES_EP = '/categories'
DEL_CATEGORY_EP = f'{CATEGORIES_EP}/{DELETE}'

CATEGORIES_MENU_EP = '/category_menu'
CATEGORIES_MENU_NM = 'Category Menu'
CATEGORY_ID = 'Category ID'

NUTRITION = 'nutrition'
NUTRITION_EP = '/categories/nutrition'
NUTRITION_MENU_EP = '/nutrition_menu'
DEL_SECTION_EP = f'{NUTRITION_EP}/{DELETE}'

EMS = "emergencyMedicalServices"
EMS_EP = '/categories/emergency_medical_services'
EMS_MENU_EP = '/emergency_medical_services_menu'

USERS = 'users'
USERS_EP = '/users'
USER_MENU_EP = '/user_menu'
USER_MENU_NM = 'User Menu'
TYPE = 'Type'
DATA = 'Data'
TITLE = 'Title'
RETURN = 'Return'


@api.route(HELLO_EP)
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {HELLO_RESP: 'world'}


@api.route('/endpoints')
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    def get(self):
        """
        The `get()` method will return a list of available endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}


@api.route(f'{MAIN_MENU_EP}')
class MainMenu(Resource):
    """
    This will deliver our main menu.
    """
    def get(self):
        """
        Gets the main category menu.
        """
        return {TITLE: MAIN_MENU_NM,
                DEFAULT: 2,
                'Choices': {
                    '1': {'url': '/', 'method': 'get',
                          'text': 'List Available Characters'},
                    '2': {'url': '/',
                          'method': 'get', 'text': 'List Active Categories'},
                    '3': {'url': f'{USERS_EP}',
                          'method': 'get', 'text': 'List Users'},
                    '4': {'url': '/',
                          'method': 'get', 'text': 'Illustrating a Point!'},
                    'X': {'text': 'Exit'},
                }}


@api.route(f'{USER_MENU_EP}')
class UserMenu(Resource):
    """
    This will deliver our user menu.
    """
    def get(self):
        """
        Gets the user menu.
        """
        return {
                   TITLE: USER_MENU_NM,
                   DEFAULT: '0',
                   'Choices': {
                       '1': {
                            'url': '/',
                            'method': 'get',
                            'text': 'Get User Details',
                       },
                       '0': {
                            'text': 'Return',
                       },
                   },
               }


user_information = api.model('NewUser', {
    users.EMAIL: fields.String,
    users.USERNAME: fields.String,
    users.PASSWORD: fields.String,
    users.FIRSTNAME: fields.String,
    users.LASTNAME: fields.String,
    users.PHONE: fields.Integer,

})


@api.route(f'{USERS_EP}')
class Users(Resource):
    """
    This class supports fetching a list of all users.
    """
    @api.expect(user_information)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Found')
    def delete(self):
        """
        This method deletes user by name.
        """
        username = request.json[users.USERNAME]
        try:
            deleted_user = users.delete_user(username)
            return {USERS: deleted_user}

        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')

    def get(self):
        """
        This method returns all users.
        """
        return {
            TYPE: DATA,
            TITLE: 'ALL USERS',
            DATA: users.get_all_users(),
            MENU: USER_MENU_EP,
            RETURN: MAIN_MENU_EP,
        }

    @api.expect(user_information)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        This method posts new user.
        """
        email = request.json[users.EMAIL]
        username = request.json[users.USERNAME]
        password = request.json[users.PASSWORD]
        first_name = request.json[users.FIRSTNAME]
        last_name = request.json[users.LASTNAME]
        phone = request.json[users.PHONE]

        try:
            new_user = users.create_user(email, username,
                                         password, first_name,
                                         last_name, phone)

            return {USERS: new_user}

        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{DEL_CATEGORY_EP}/<name>')
class DelCategory(Resource):
    """
    Deletes a category by name.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, name):
        """
        Deletes a category by name.
        """
        try:
            categ.delete_category(name)
            return {name: 'Deleted'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


category_fields = api.model('NewCategory', {
    categ.NAME: fields.String,
    categ.CATEGORY_ID: fields.Integer,
    categ.NUM_SECTIONS: fields.Integer,
})


nutrition_fields = api.model('NewNutrition', {
    nutrition.NAME: fields.String,
    nutrition.SECTION_ID: fields.Integer,
    nutrition.ARTICLE: fields.Raw,
})

ems_fields = api.model('NewEMS', {
    ems.EMS_SECTION_NAME: fields.String,
    ems.EMS_SECTION_ID: fields.Integer,
    ems.EMS_ARTICLES: fields.String,
})


@api.route(f'{CATEGORIES_EP}')
class Categories(Resource):
    """
    This class supports various operations on games, such as
    listing them, and adding a game.
    """
    def get(self):
        """
        This method returns all categories.
        """
        return {
            TYPE: DATA,
            TITLE: 'Current Categories',
            DATA: categ.get_categories(),
            MENU: CATEGORIES_MENU_EP,
            RETURN: MAIN_MENU_EP,
        }

    @api.expect(category_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        Add a category.
        """
        name = request.json[categ.NAME]
        category_id = request.json[categ.CATEGORY_ID]
        num_sections = request.json[categ.NUM_SECTIONS]
        try:
            new_id = categ.add_category(
                name, category_id, num_sections)
            if new_id is None:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {CATEGORY_ID: new_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{NUTRITION_EP}')
class Nutrition(Resource):
    """
    This class supports fetching a list of all nutrition sections.
    """
    def get(self):
        """
        This method returns all nutrition.
        """
        return {
            TYPE: DATA,
            TITLE: 'ALL NUTRITION',
            DATA: nutrition.get_sections(),
            MENU: NUTRITION_MENU_EP,
            RETURN: MAIN_MENU_EP,
        }

    @api.expect(nutrition_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        This method posts new nutrition.
        """

        name = request.json[nutrition.NAME]
        section_id = request.json[nutrition.SECTION_ID]
        article = request.json[nutrition.ARTICLE]

        try:
            new_section = nutrition.add_section(name, section_id, article)

            return {NUTRITION: new_section}

        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{DEL_SECTION_EP}/<name>')
class DeleteSection(Resource):
    """
    Deletes a section in nutrition by name.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, name):
        """
        Deletes a section by name.
        """
        try:
            nutrition.delete_section(name)
            return {name: 'Deleted'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@api.route(f'{EMS_EP}')
class EmergencyMedicalServices(Resource):
    """
    This class supports fetching a list of all EMS sections.
    """
    def get(self):
        """
        This method returns all emergency medical services.
        """
        return {
            TYPE: DATA,
            TITLE: 'ALL EMERGENCY MEDICAL SERVICES',
            DATA: ems.get_ems_sections(),
            MENU: EMS_MENU_EP,
            RETURN: MAIN_MENU_EP,
        }

    @api.expect(ems_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        This method posts new ems.
        """

        name = request.json[ems.EMS_SECTION_NAME]
        section_id = request.json[ems.EMS_SECTION_ID]
        article = request.json[ems.EMS_ARTICLES]

        try:
            new_section = ems.add_ems_section(name, section_id, article)

            return {EMS: new_section}

        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')
