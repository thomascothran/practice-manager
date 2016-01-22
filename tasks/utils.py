from .models import Context

def get_users_contexts(user):
        """
        Pass this function a user object, and it will return a query object of
        all the user's contexts. This is primarily used by views to generate
        forms dynamically with these options.
        """
        users_contexts = Context.objects.filter(user=user)
        return users_contexts