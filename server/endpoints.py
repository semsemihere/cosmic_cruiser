"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

from flask import Flask, request
from flask_restx import Resource, Api, fields
from flask_cors import CORS


import werkzeug.exceptions as wz

import data.form as login
import data.categories as categ
import data.users as users
import data.nutrition as nutrition
import data.ems as ems
import data.finances as fin

app = Flask(__name__)
api = Api(app)
CORS(app)

NAME = 'name'
SECTIONS = 'sections'
UPDATE = 'update'
DELETE = 'delete'
DEFAULT = 'Default'
MENU = 'menu'
MAIN_MENU_EP = '/MainMenu'
MAIN_MENU_NM = "Welcome to Jack-of-All-Trades!"
HELLO_EP = '/hello'
HELLO_RESP = 'hello'
LOGIN_RESP = "{'login_form': "

CATEGORIES_MENU_NM = 'Category Menu'
CATEGORY_ID = 'Category ID'
CATEGORIES_EP = '/categories'
CATEGORIES_MENU_EP = '/category_menu'
UPDATE_CATEGORY_NAME_EP = f'{CATEGORIES_EP}/{UPDATE}/{NAME}'
UPDATE_CATEGORY_SECTIONS_EP = f'{CATEGORIES_EP}/{UPDATE}/{SECTIONS}'
DEL_CATEGORY_EP = f'{CATEGORIES_EP}/{DELETE}'

NUTRITION = 'nutrition'
NUTRITION_EP = '/categories/nutrition'
NUTRITION_MENU_EP = '/nutrition_menu'
NUTRITION_ARTICLE_MENU_EP = 'nutrition_article_menu'
DEL_NUTRITION_SECTION_EP = f'{NUTRITION_EP}/{DELETE}'

EMS = "emergencyMedicalServices"
EMS_EP = '/categories/emergency_medical_services'
EMS_MENU_EP = '/emergency_medical_services_menu'
EMS_ARTICLE_MENU_EP = 'ems_article_menu'
DEL_EMS_SECTION_EP = f'{EMS_EP}/{DELETE}'

FINANCES = 'finances'
FINANCES_EP = '/categories/finances'
FINANCES_MENU_EP = '/finances_menu'
FINANCES_ARTICLE_MENU_EP = 'finances_article_menu'
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

LOGIN = 'login'
LOGIN_EP = '/login'
LOGIN_FORM = 'login_form'


# Define a new field for login credentials
login_fields = api.model('Login', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
    'role': fields.String(required=True)
})


@api.route(f'{LOGIN_EP}')
class Login(Resource):
    """
    This class handles user authentication.
    """
    def get(sef):
        """
        get returns
        """
        return {LOGIN_FORM: login.get_form()}

    @api.expect(login_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.UNAUTHORIZED, 'Unauthorized')
    def post(self):
        print("Request JSON:", request.json)
        username = request.json['username']
        password = request.json['password']
        role = request.json['role']

        # user = users.exists(username)
        if not username or not password or not role:
            return {'message': 'Info missing'}, HTTPStatus.UNAUTHORIZED

        # user_role = users.login_user(username, password)
        if users.login_user(username, password, role):
            return {'message': 'Login successful'}, HTTPStatus.OK
        else:
            return {'message': 'Invalid info'}, HTTPStatus.UNAUTHORIZED


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


@api.route('/categories/get_article/<articleName>')
class CreateArticle(Resource):
    def get(self, articleName):
        return categ.get_article(articleName)


@api.route('/categories/add_article_to_category/<categoryID>/<articleName>')
class AddArticleToCategory(Resource):
    def get(self, categoryID, articleName):
        return categ.add_article_to_category(categoryID, articleName)


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
        """
        Delete a user by username.
        """
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
    users.ROLE: fields.String
})


@api.route(f'{USERS_EP}')
class Users(Resource):
    """
    This class supports various operations on users, such as
    listing them, and adding a new user.
    """
    def get(self):
        """
        Return all users.
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
        Add a user
        """
        try:
            email = request.json[users.EMAIL]
            username = request.json[users.USERNAME]
            password = request.json[users.PASSWORD]
            first_name = request.json[users.FIRSTNAME]
            last_name = request.json[users.LASTNAME]
            phone = request.json[users.PHONE]
            role = request.json[users.ROLE]

            new_user = users.create_user(email, username,
                                         password, first_name,
                                         last_name, phone, role)

            return {USERS: new_user}

        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{DEL_CATEGORY_EP}/<category_id>')
class DeleteCategory(Resource):
    """
    Deletes a category by id.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, category_id):
        """
        Delete a category by id.
        """
        try:
            categ.delete_category(category_id)
            return {category_id: 'Deleted'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


category_fields = api.model('NewCategory', {
    categ.NAME: fields.String,
    categ.CATEGORY_ID: fields.String,
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
        Return all categories.
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


@api.route(f'{UPDATE_CATEGORY_NAME_EP}/<category_id>/<new_category_name>')
class UpdateCategoryName(Resource):
    """
    Updates name of a specific category.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.BAD_REQUEST, 'Bad Request')
    def put(self, category_id, new_category_name):
        """
        Update the name of a category by id
        """
        try:
            categ.update_category_name(category_id, new_category_name)
            return {new_category_name: 'Updated category name'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')
        except Exception as e:
            raise wz.BadRequest(f'failed to update category name: {str(e)}')


@api.route(f'{UPDATE_CATEGORY_SECTIONS_EP}/<category_id>/<new_num_sections>')
class UpdateCategoryNumSections(Resource):
    """
    Updates number of sections under a specific category.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.BAD_REQUEST, 'Bad Request')
    def put(self, category_id, new_num_sections):
        """
        Update the number of sections in a category by id
        """
        try:
            categ.update_category_sections(category_id, new_num_sections)
            return {new_num_sections: 'Updated number of sections'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')
        except Exception as e:
            raise wz.BadRequest(f'failed to update num sections: {str(e)}')


@api.route(f'{DEL_NUTRITION_SECTION_EP}/<nutrition_section_id>')
class DeleteNutritionSection(Resource):
    """
    Delete a nutrition section by id.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, nutrition_section_id):
        """
        Delete a nutrition section by id.
        """
        try:
            nutrition.delete_section(nutrition_section_id)
            return {nutrition_section_id: 'Deleted'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@api.route(
    f'{DEL_NUTRITION_SECTION_EP}/<nutrition_section_id>/<nutrition_article_id>'
)
class DeleteNutritionArticle(Resource):
    """
    Delete a nutrition article by id.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, nutrition_section_id, nutrition_article_id):
        """
        Delete a nutrition article by id.
        """
        try:
            nutrition.delete_article(nutrition_section_id,
                                     nutrition_article_id)
            return {nutrition_article_id: 'Deleted'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


nutrition_article_fields = api.model('NewNutritionArticle', {
    nutrition.ARTICLE_NAME: fields.String,
    nutrition.ARTICLE_ID: fields.String,
    nutrition.ARTICLE_CONTENT: fields.String,
})


nutrition_section_fields = api.model('NewNutritionSection', {
    nutrition.SECTION_NAME: fields.String,
    nutrition.SECTION_ID: fields.String,
    nutrition.ARTICLE_IDS: fields.List(fields.String),
})


@api.route(f'{NUTRITION_EP}')
class NutritionSections(Resource):
    """
    This class supports various operations on nutrition, such as
    listing them, and adding a new nutrition section.
    """
    def get(self):
        """
        Return all nutrition sections.
        """

        return {
            TYPE: DATA,
            TITLE: 'ALL NUTRITION',
            DATA: nutrition.get_sections(),
            MENU: NUTRITION_MENU_EP,
            RETURN: MAIN_MENU_EP,
        }

    @api.expect(nutrition_section_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        Add a nutrition section
        """
        name = request.json[nutrition.SECTION_NAME]
        section_id = request.json[nutrition.SECTION_ID]
        # article = categ.get_article(name)
        # article = {}
        article_ids = []

        print("nutrition", name,  section_id)

        try:
            new_section = nutrition.add_section(name,
                                                section_id,
                                                article_ids)
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
        """
        Update the contents of a nutrition by id.
        """
        try:
            nutrition.update_nutrition_section_content(nutrition_section_id,
                                                       new_content)
            return {nutrition_section_id: 'Updated content'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')
        except Exception as e:
            raise wz.BadRequest(f'failed to update content: {str(e)}')


@api.route(f'{NUTRITION_EP}/<nutrition_section_id>/articles')
class NutritionArticles(Resource):
    """
    This class supports various operations on nutrition, such as
    listing them, and adding a new nutrition section.
    """
    def get(self, nutrition_section_id):
        """
        Return all nutrition articles within a specific section.
        """

        return {
            TYPE: DATA,
            TITLE: 'ALL NUTRITION',
            DATA: nutrition.get_articles(nutrition_section_id),
            MENU: NUTRITION_ARTICLE_MENU_EP,
            RETURN: MAIN_MENU_EP,
        }

    @api.expect(nutrition_article_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self, nutrition_section_id):
        """
        Add a nutrition article to a specific section
        """

        article_name = request.json[nutrition.ARTICLE_NAME]
        article_id = request.json[nutrition.ARTICLE_ID]
        article_content = categ.get_article(article_name)

        try:
            new_article = nutrition.add_article(nutrition_section_id,
                                                article_name,
                                                article_id,
                                                article_content)
            return {NUTRITION: new_article}, HTTPStatus.CREATED

        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{DEL_EMS_SECTION_EP}/<ems_section_id>')
class DeleteEMSSection(Resource):
    """
    Deletes a emergency medical service section by id.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, ems_section_id):
        """
        Delete a emergency medical service section by id.
        """
        try:
            ems.delete_ems_section(ems_section_id)
            return {ems_section_id: 'Deleted'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@api.route(
    f'{DEL_EMS_SECTION_EP}/<ems_section_id>/<ems_article_id>'
)
class DeleteEMSArticle(Resource):
    """
    Delete a ems article by id.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, ems_section_id, ems_article_id):
        """
        Delete a ems article by id.
        """
        try:
            ems.delete_article(ems_section_id,
                               ems_article_id)
            return {ems_article_id: 'Deleted'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


ems_article_fields = api.model('NewEMSArticle', {
    ems.ARTICLE_NAME: fields.String,
    ems.ARTICLE_ID: fields.String,
    ems.ARTICLE_CONTENT: fields.String,
})


ems_section_fields = api.model('NewEMSSection', {
    ems.SECTION_NAME: fields.String,
    ems.SECTION_ID: fields.String,
    ems.ARTICLE_IDS: fields.List(fields.String),
})


@api.route(f'{EMS_EP}')
class EmergencyMedicalServices(Resource):
    """
    This class supports various operations on EMS, such as
    listing them, and adding a new EMS section.
    """
    def get(self):
        """
        Return all emergency medical services sections.
        """
        return {
            TYPE: DATA,
            TITLE: 'ALL EMERGENCY MEDICAL SERVICES',
            DATA: ems.get_ems_sections(),
            MENU: EMS_MENU_EP,
            RETURN: MAIN_MENU_EP,
        }

    @api.expect(ems_section_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        Add a emergency medical service section.
        """

        name = request.json[ems.SECTION_NAME]
        section_id = request.json[ems.SECTION_ID]
        article_ids = []

        try:
            new_section = ems.add_section(name,
                                          section_id,
                                          article_ids)

            return {EMS: new_section}

        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{EMS_EP}/<ems_section_id>/<new_content>')
class UpdateEMSSection(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.BAD_REQUEST, 'Bad Request')
    def put(self, ems_section_id, new_content):
        """
        Update the contents of a emergency medical service by id.
        """
        try:
            ems.update_ems_section_content(ems_section_id, new_content)
            return {ems_section_id: 'Updated content'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')
        except Exception as e:
            raise wz.BadRequest(f'failed to update content: {str(e)}')


@api.route(f'{EMS_EP}/<ems_section_id>/articles')
class EMSArticles(Resource):
    """
    This class supports various operations on ems, such as
    listing them, and adding a new ems section.
    """
    def get(self, ems_section_id):
        """
        Return all ems articles within a specific section.
        """

        return {
            TYPE: DATA,
            TITLE: 'ALL EMERGENCY MEDICAL SERVICES',
            DATA: ems.get_articles(ems_section_id),
            MENU: NUTRITION_ARTICLE_MENU_EP,
            RETURN: MAIN_MENU_EP,
        }

    @api.expect(ems_article_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self, ems_section_id):
        """
        Add a ems article to a specific section
        """

        article_name = request.json[ems.ARTICLE_NAME]
        article_id = request.json[ems.ARTICLE_ID]
        article_content = categ.get_article(article_name)

        try:
            new_article = ems.add_article(ems_section_id,
                                          article_name,
                                          article_id,
                                          article_content)
            return {EMS: new_article}, HTTPStatus.CREATED

        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


# FINANCE #####
# articles_nested = api.model('articles', {
#     'title': fields.String,
#     'content': fields.String
#     },
# )


finance_article_fields = api.model('NewFinanceArticle', {
    nutrition.ARTICLE_NAME: fields.String,
    nutrition.ARTICLE_ID: fields.String,
    nutrition.ARTICLE_CONTENT: fields.String,
})


finance_fields = api.model('NewFinance', {
    fin.SECTION_NAME: fields.String,
    fin.SECTION_ID: fields.String,
    fin.ARTICLE_IDS: fields.List(fields.String),
})


@api.route(f'{DEL_FINANCES_SECTION_EP}/<finance_section_id>')
class DeleteFinancesSection(Resource):
    """
    Delete a section in finance by id.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, finance_section_id):
        """
        Delete a finance section by id.
        """
        try:
            fin.delete_finances_section(finance_section_id)
            return {finance_section_id: 'Deleted'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@api.route(
    f'{DEL_FINANCES_SECTION_EP}/<finances_section_id>/<finances_article_id>'
)
class DeleteFinancesArticle(Resource):
    """
    Delete a finances article by id.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, finances_section_id, finances_article_id):
        """
        Delete a finances article by id.
        """
        try:
            fin.delete_article(finances_section_id,
                               finances_article_id)
            return {finances_article_id: 'Deleted'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@api.route(f'{FINANCES_EP}')
class Finances(Resource):
    """
    This class supports fetching a list of all finance sections.
    """
    def get(self):
        """
        Return all finances sections
        """
        return {
            TYPE: DATA,
            TITLE: 'ALL FINANCES',
            DATA: fin.get_finances_sections(),
            MENU: FINANCES_MENU_EP,
            RETURN: MAIN_MENU_EP,
        }

    @api.expect(finance_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        Add a finance section
        """
        name = request.json[fin.SECTION_NAME]
        section_id = request.json[fin.SECTION_ID]
        # article = categ.get_article(name)
        article = []

        try:
            new_section = fin.add_finances_section(name, section_id, article)

            return {FINANCES: new_section}

        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


# @api.route(f'{FINANCES_EP}/<finance_section>/<finance_section_id>')
# class FinanceSectionArticles(Resource):
#     def get(self, finance_section, finance_section_id):
#         """
#         Return all finances
#         """
#         return {
#             TYPE: DATA,
#             TITLE: 'ALL FINANCES',
#             DATA: fin.exists(finance_section_id),
#             MENU: FINANCES_MENU_EP,
#             RETURN: MAIN_MENU_EP,
#         }


@api.route(f'{FINANCES_EP}/<finance_section>/<finance_section_id>/' +
           '<article_title>/<article_content>')
class UpdateFinanceSection(Resource):
    """
    updates finance section
    """

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.BAD_REQUEST, 'Bad Request')
    def put(self, finance_section, finance_section_id,
            article_title, article_content):
        """
        Update the contents of a finance by id.
        """
        try:
            fin.update_finance_section_article(
                finance_section, finance_section_id,
                article_title, article_content)
            # return {finance_section_id: 'Updated content'}
            return fin.get_finances_sections()
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')
        except Exception as e:
            raise wz.BadRequest(f'failed to update content: {str(e)}')


@api.route(f'{FINANCES_EP}/<finances_section_id>/articles')
class FinancesArticles(Resource):
    """
    This class supports various operations on finances, such as
    listing them, and adding a new finances section.
    """
    def get(self, finances_section_id):
        """
        Return all finances articles within a specific section.
        """

        return {
            TYPE: DATA,
            TITLE: 'ALL FINANCES',
            DATA: fin.get_articles(finances_section_id),
            MENU: FINANCES_ARTICLE_MENU_EP,
            RETURN: MAIN_MENU_EP,
        }

    @api.expect(finance_article_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self, finances_section_id):
        """
        Add a finances article to a specific section
        """

        article_name = request.json[fin.ARTICLE_NAME]
        article_id = request.json[fin.ARTICLE_ID]
        article_content = categ.get_article(article_name)

        try:
            new_article = fin.add_article(finances_section_id,
                                          article_name,
                                          article_id,
                                          article_content)
            return {FINANCES: new_article}, HTTPStatus.CREATED

        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')
