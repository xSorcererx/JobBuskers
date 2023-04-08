from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _


class CustomUserManager(BaseUserManager):
    # user creation
    def create_user(self, email, password, name, phone, location, user_type, **other_fields):
        if not email:
            raise ValueError(_('Email Not Found'))

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone=phone,
            location=location,
            user_type=user_type,          
            **other_fields
        )

        user.set_password(password)
        user.is_active=True
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, name, phone, location, user_type, *args, **kwargs):
        if not email:
            raise ValueError(_('Email Not Found'))
        
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            name=name,
            phone=phone,
            location=location,
        )
        user.is_superuser = True
        user.is_staff = True
        user.user_type = '1'
        user.is_active = True
        user.is_verified = True
        user.save(using=self._db)

        return user

    def create_company(self, email, password=None, user_type=None):
        if not email:
            raise ValueError(_('Email Not Found'))

        company = self.model(
            email=self.normalize_email(email),
        )

        company.set_password(password)
        company.user_type = 2
        company.save(using=self._db)
        return company
    
    
    def create_candidate(self, email, password=None, user_type=None):
        if not email:
            raise ValueError(_('Email Not Found'))

        company = self.model(
            email=self.normalize_email(email),
        )

        company.set_password(password)
        company.user_type = 3
        company.save(using=self._db)
        return company

    def get_name(self):
        return self.name