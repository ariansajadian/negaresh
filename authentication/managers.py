from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, first_name=None, last_name=None, password=None):
        """
        Creates and saves a User with the given email, first_name
        last_name and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        
        if not password:
            raise ValueError("Users must have an password")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_admin(self, email, first_name=None, last_name=None, password=None):
        """
        Creates and saves a admin with the given email
        and password.
        """
        admin_user = self.create_admin(email, first_name=first_name, 
                            last_name=last_name, password=password)

        admin_user.is_admin = True
        admin_user.save(using=self._db)
        return admin_user

    def create_superuser(self, email, first_name=None, last_name=None, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """

        super_user = self.create_admin(email, first_name=first_name, 
                                       last_name=last_name, password=password)
        super_user.is_superuser = True
        super_user.save(using=self._db)
        return super_user