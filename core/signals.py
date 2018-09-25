"""Signal"""
import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in

import bayou

logger = logging.getLogger(__name__)
User = get_user_model()


def update_user_info(user, save=True):
    """Updates a users email, first_name, and last_name."""
    p = bayou.Person.from_default_services(user.username)

    user.email = p.email if p.email else user.email
    user.first_name = p.first_name if p.first_name else user.first_name
    user.last_name = p.surname if p.surname else user.last_name

    if save:
        user.save()

    return user


def update_user_info_signal(sender, request, user, **kwargs):
    """
    Function to be used as a Django signal receiver to be called when a user
    logs into the site successfully.

    Makes the first user a superuser and everyone a staff.
    """
    # TODO This is an example signal for login and should be replaced or
    # removed before pushing the project to production.
    if user.pk == 1:
        user.is_superuser = True
    user.is_staff = True
    user.save()
    logger.warn(
        "Don't forget to update core/signals.py before "
        'deploying to production.'
    )


user_logged_in.connect(update_user_info_signal, sender=User)
