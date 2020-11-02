import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'cs-udacity.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'shop'

# AuthError Exception


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header


def get_token_auth_header():
    if 'Authorization' not in request.headers:
        return AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header is malformed'
        }, 401)
    auth_header = request.headers.get('Authorization')
    if auth_header.split(' ')[0] != 'Bearer':
        return AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header is malformed'
        }, 401)
    jwt_token = auth_header.split(' ')[1]
    return jwt_token


def check_permissions(permission, payload):
    if payload is None:
        raise AuthError({
                'code': 'invalid_token',
                'description': 'There is no token provided'
            }, 401)
    if 'permissions' not in payload:
        raise AuthError({
                'code': 'invalid_token',
                'description': 'Invalid token.\
                 User is not assigned to roles or permissions'
            }, 401)
    if permission not in payload['permissions']:
        raise AuthError({
                'code': 'not_authorized',
                'description': 'Not Authorized.\
                                User is not authorized to perform this action'
            }, 401)  ''' I expected it to be 403
                    but it failed in postman collection runner test !'''
    return True


def verify_decode_jwt(token):
    # GET THE PUBLIC KEY FROM AUTH0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    try:
        # GET THE DATA IN THE HEADER
        unverified_header = jwt.get_unverified_header(token)

        # CHOOSE OUR KEY
        rsa_key = {}
        if 'kid' not in unverified_header:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Authorization malformed.'
            }, 401)

        for key in jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }

        # Finally, verify!!!
        if rsa_key:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload

    except jwt.ExpiredSignatureError:
        raise AuthError({
            'code': 'token_expired',
            'description': 'Token expired.'
        }, 401)

    except jwt.JWTClaimsError:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Incorrect claims.\
                            Please, check the audience and issuer.'
        }, 401)

    except jwt.JWTError:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Unable to parse authentication token.'
        }, 401)
    except Exception:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Unable to parse authentication token.'
        }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            if check_permissions(permission, payload):
                return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator
