import json
from os import abort
from flask import request, _request_ctx_stack, abort, jsonify
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = 'fsnd-course.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'every_image'


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():

    header = request.headers.get('Authorization')
    if not header:
        raise AuthError({
            'code': 'no_authorization_header',
            'description': 'request does not contain authorization header'
        }, 401)

    header_content = header.split(' ')

    if len(header_content) != 2 or header_content[0] != 'Bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'authorization header is not formatted properly'
        }, 401)

    return header_content[1]


def check_permissions(permission, payload):

    if 'permissions' not in payload:
        print('no permission in payload')
        raise AuthError({
            'code': 'payload_has_no_permissions',
            'description': 'permissions are not included in the token'
        }, 403)

    # User trying to access unathourized resources
    if permission not in payload['permissions']:
        print('no permission for user')
        raise AuthError(
            {
                'code': 'unathourized_user',
                'description': 'user is not authorized'
            }, 403)

    # User is authorized to access the requested endpoint
    return True


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # we extract the header from the provided token
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}

    # if the token header has no kid we raise an error
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    # we look for the key that matches what was in the token header
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    # in here we decode the jwt based on the that key
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            # if no errors were raised we will return the payload containing the info
            return payload

        # if the token has expired
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)

        # any other exception that me not be caught above we catch it down here
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)

    # could not find the key
    raise AuthError({
        'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
    }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            token = get_token_auth_header()

            payload = verify_decode_jwt(token)

            check_permissions(permission, payload)

            return f(*args, **kwargs)
        return wrapper
    return requires_auth_decorator
