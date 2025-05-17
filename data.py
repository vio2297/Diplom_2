class ResponseMessages:
    # REGISTRATION
    SUCCESS_REGISTRATION = True
    EXISTING_USER_REGISTRATION = 'User already exists'
    MISSING_DATA_USER_REGISTRATION = 'Email, password and name are required fields'

    #LOGIN
    SUCCESS_LOGIN = True
    WRONG_DATA_LOGIN = 'email or password are incorrect'

    #CREATE ORDER
    NEED_AUTH_FOR_ORDER_CREATION = 'You should be authorised'
    MISSING_INGREDIENTS = 'Ingredient ids must be provided'

    # GET ORDER DATA
    NEED_AUTH_FOR_ORDER_STATUS = 'You should be authorised'
    # USER DATA UPDATES
    NEED_AUTH_FOR_USER_UPDATES = "You should be authorised"
    EXISTING_USER_EMAIL_FOR_UPDATES = "User with such email already exists"



class ResponseStatus:
    OK = 200
    FORBIDDEN = 403
    UNAUTHORIZED = 401
    BAD_REQUEST = 400
    INTERNAL_SERVER_ERROR = 500

class UserData:
    EXISTING_USER_NAME = 'MiMi'
    EXISTING_USER_EMAIL = 'mimi012345@gmail.com'
    EXISTING_USER_PASSWORD = 'MiStar1234'

class IngredientsData:
    VALID_INGREDIENTS = ['60d3b41abdacab0026a733c6','609646e4dc916e00276b2870']
    INVALID_INGREDIENTS = ['0', '1']

