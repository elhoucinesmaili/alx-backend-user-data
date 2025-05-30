#!/usr/bin/env python3
"""BasicAuth class for Basic Authentication"""
import base64
from typing import TypeVar

from models.user import User
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Basic authentication class"""
    
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Extract the Base64 part of the Authorization header"""
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        
        if not authorization_header.startswith('Basic '):
            return None
        
        return authorization_header[6:]
    
    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """Decode a Base64 string"""
        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):
            return None
        
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None
    
    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """Extract user credentials from decoded Base64 string"""
        if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str):
            return None, None
        
        if ':' not in decoded_base64_authorization_header:
            return None, None
        
        # Split on the first colon only
        credentials = decoded_base64_authorization_header.split(':', 1)
        return credentials[0], credentials[1]
    
    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Get User instance from credentials"""
        if user_email is None or not isinstance(user_email, str):
            return None
        
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        
        if not users:
            return None
        
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        
        return user
    
    def current_user(self, request=None) -> TypeVar('User'):
        """Get current user from request"""
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        
        base64_header = self.extract_base64_authorization_header(auth_header)
        if base64_header is None:
            return None
        
        decoded_header = self.decode_base64_authorization_header(base64_header)
        if decoded_header is None:
            return None
        
        email, pwd = self.extract_user_credentials(decoded_header)
        if email is None or pwd is None:
            return None
        
        return self.user_object_from_credentials(email, pwd)
