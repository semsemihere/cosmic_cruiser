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
import data.finances as fin

app = Flask(__name__)
api = Api(app)

DELETE = 'delete'
DEFAULT = 'Default'
MENU = 'menu'
MAIN_MENU_EP = '/MainMenu'
MAIN_MENU_NM = "Welcome to Jack-of-All-Trades!"
HELLO_EP = '/hello'
HELLO_RESP = 'hello'

CATEGORIES_MENU_NM = 'Category Menu'
CATEGORY_ID = 'Category ID'
CATEGORIES_EP = '/categories'
CATEGORIES_MENU_EP = '/category_menu'
DEL_CATEGORY_EP = f'{CATEGORIES_EP}/{DELETE}'

NUTRITION = 'nutrition'
NUTRITION_EP = '/categories/nutrition'
NUTRITION_MENU_EP = '/nutrition_menu'
DEL_NUTRITION_SECTION_EP = f'{NUTRITION_EP}/{DELETE}'

EMS = "emergencyMedicalServices"
EMS_EP = '/categories/emergency_medical_services'
EMS_MENU_EP = '/emergency_medical_services_menu'
DEL_EMS_SECTION_EP = f'{EMS_EP}/{DELETE}'

FINANCES = 'finances'
FINANCES_EP = '/categories/finances'
FINANCES_MENU_EP = '/finances_menu'
DEL_FINANCES_SECTION_EP = f'{FINANCES_EP}/{DELETE}'

USERS = 'users'
USERS_EP = '/users'
USER_MENU_EP = '/user_menu'
USER_MENU_NM = 'User Menu'
DEL_USERS_EP = f'{USERS_EP}/{DELETE}'
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


@api.route(f'{DEL_USERS_EP}/<username>')
class DeleteUser(Resource):
    """
    This method deletes user.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, username):
        # This method deletes a user by username.

        try:
            users.delete_user(username)
            return {username: 'Deleted'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


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
    This class supports various operations on users, such as
    listing them, and adding a new user.
    """
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

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        This method posts new user.
        """
        try:
            email = request.json[users.EMAIL]
            username = request.json[users.USERNAME]
            password = request.json[users.PASSWORD]
            first_name = request.json[users.FIRSTNAME]
            last_name = request.json[users.LASTNAME]
            phone = request.json[users.PHONE]

            new_user = users.create_user(email, username,
                                         password, first_name,
                                         last_name, phone)

            return {USERS: new_user}

        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{DEL_CATEGORY_EP}/<name>')
class DeleteCategory(Resource):
    """
    This method deletes a category.
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


@api.route(f'{CATEGORIES_EP}')
class Categories(Resource):
    """
    This class supports various operations on categories, such as
    listing them, and adding a new category.
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


@api.route(f'{DEL_NUTRITION_SECTION_EP}/<nutrition_section_id>')
class DeleteNutritionSection(Resource):
    """
    Deletes a section in nutrition by name.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, nutrition_section_id):
        """
        Deletes a nutrition section by nutrition_section_id.
        """
        try:
            nutrition.delete_section(nutrition_section_id)
            return {nutrition_section_id: 'Deleted'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


nutrition_fields = api.model('NewNutrition', {
    nutrition.NAME: fields.String,
    nutrition.SECTION_ID: fields.String,
    nutrition.ARTICLE: fields.String,
})


@api.route(f'{NUTRITION_EP}')
class Nutrition(Resource):
    """
    This class supports various operations on nutrition, such as
    listing them, and adding a new nutrition section.
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
        This method posts new nutrition section.
        """

        name = request.json[nutrition.NAME]
        section_id = request.json[nutrition.SECTION_ID]
        article = request.json[nutrition.ARTICLE]

        try:
            new_section = nutrition.add_section(name, section_id, article)

            return {NUTRITION: new_section}

        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{NUTRITION_EP}/<nutrition_section_id>/<new_content>')
class UpdateNutritionSection(Resource):
    """
    Updates content of a section in the nutrition category.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.BAD_REQUEST, 'Bad Request')
    def put(self, nutrition_section_id, new_content):

        try:
            nutrition.update_nutrition_section_content(nutrition_section_id,
                                                       new_content)
            return {nutrition_section_id: 'Updated content'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')
        except Exception as e:
            raise wz.BadRequest(f'failed to update content: {str(e)}')
        # new_content = request.json.get('nutritionContent')

        # if new_content is None:
        #     raise wz.BadRequest('need to include content field')

        # try:
        #     nutrition.update_nutrition_section_content(name, new_content)
        #     return {name: 'content updated successfully'}
        # except ValueError as e:
        #     raise wz.NotFound(f'{str(e)}')
        # except Exception as e:
        #     raise wz.BadRequest(f'failed to update content: {str(e)}')


@api.route(f'{DEL_EMS_SECTION_EP}/<ems_section_id>')
class DeleteEMS(Resource):
    """
    Deletes a ems section by id.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, ems_section_id):
        """
        Deletes a ems section by id.
        """
        try:
            ems.delete_ems_section(ems_section_id)
            return {ems_section_id: 'Deleted'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


ems_fields = api.model('NewEMS', {
    ems.EMS_SECTION_NAME: fields.String,
    ems.EMS_SECTION_ID: fields.String,
    ems.EMS_ARTICLES: fields.String,
})


@api.route(f'{EMS_EP}')
class EmergencyMedicalServices(Resource):
    """
    This class supports various operations on EMS, such as
    listing them, and adding a new EMS section.
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


@api.route(f'{EMS_EP}/<ems_section_id>/<new_content>')
class UpdateEMSSection(Resource):
    """
    Updates content of a section in the ems category.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.BAD_REQUEST, 'Bad Request')
    def put(self, ems_section_id, new_content):

        try:
            ems.update_ems_section_content(ems_section_id, new_content)
            return {ems_section_id: 'Updated content'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')
        except Exception as e:
            raise wz.BadRequest(f'failed to update content: {str(e)}')


finance_fields = api.model('NewFinance', {
    fin.FINANCES_NAME: fields.String,
    fin.FINANCES_SECTION_ID: fields.String,
    fin.FINANCES_ARTICLE: fields.String,
})


@api.route(f'{DEL_FINANCES_SECTION_EP}/<finance_section_id>')
class DeleteFinancesSection(Resource):
    """
    Deletes a section in finance by name.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, finance_section_id):
        """
        Deletes a finance section by name.
        """
        try:
            fin.delete_finances_section(finance_section_id)
            return {finance_section_id: 'Deleted'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@api.route(f'{FINANCES_EP}')
class Finances(Resource):
    """
    This class supports fetching a list of all finance sections.
    """
    def get(self):
        """
        This method returns all finance.
        """
        return {
            TYPE: DATA,
            TITLE: 'ALL FINANCE',
            DATA: fin.get_finances_sections(),
            MENU: FINANCES_MENU_EP,
            RETURN: MAIN_MENU_EP,
        }

    @api.expect(finance_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        This method posts new finance.
        """

        name = request.json[fin.FINANCES_NAME]
        section_id = request.json[fin.FINANCES_SECTION_ID]
        article = request.json[fin.FINANCES_ARTICLE]

        try:
            new_section = fin.add_finances_section(name, section_id, article)

            return {FINANCES: new_section}

        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{FINANCES_EP}/<finance_section_id>/<new_content>')
class UpdateFinanceSection(Resource):
    """
    Updates content of a section in the finance category.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.BAD_REQUEST, 'Bad Request')
    def put(self, finance_section_id, new_content):

        try:
            fin.update_finance_section_content(finance_section_id, new_content)
            return {finance_section_id: 'Updated content'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')
        except Exception as e:
            raise wz.BadRequest(f'failed to update content: {str(e)}')
