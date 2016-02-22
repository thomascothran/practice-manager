from django.db.models import Q
from .models import Task

import logging

# LOGGING SETTINGS

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of tasks/utils.py')

def apply_filters_from_task_filter(requesting_user, post_dict):
    """
    This function applies the filters from the task filter,
    and returns a list of task and project objects.

    requesting_user: the request.user (the user who is making the view request)
    post_dict: dict is a diction of the cleaned post data
    """
    # First, let's handle the tasks
    if not (post_dict['item_filter'] == 'project'):
        # The requesting user just wants projects. Don't
        # return any tasks
        filtered_tasks = None
    else:
        # Tasks are requested. First, query tasks that requesting_user
        # related to.
        if post_dict['role_filter'] == 'any':
            # If the requesting_user wants tasks in which he has any role,
            # get all tasks in which he has a role
            filtered_tasks = Task.objects.filter(
                Q(created_by=requesting_user) | Q(assigned_to=requesting_user) | Q(supervisor=requesting_user)
            )
        elif post_dict['role_filter'] == 'created_by':
            # User just wants tasks he created
            filtered_tasks = Task.objects.filter(
                Q(created_by=requesting_user)
            )
        elif post_dict['role_filter'] == 'supervisor':
            filtered_tasks = Task.objects.filter(
                Q(supervisor=requesting_user)
            )
        else:
            # This covers post_dict['role_filter'] == 'assigned_to':
            # as well as anything forgotton
            filtered_tasks = Task.objects.filter(
                Q(assigned_to=requesting_user)
            )

        # Now, we will apply the status filter
        if post_dict['status_filter'] == 'any':
            # Any status ok. Don't filter.
            pass
        elif post_dict['status_filter'] == 'pending':
            filtered_tasks = filtered_tasks.filter(status='pending')
        elif post_dict['status_filter'] == 'complete':
            filtered_tasks = filtered_tasks.filter(status='complete')

        # Now we apply the context filter
        if post_dict['context_filter'] != '' or post_dict['context_filter'] != None:
            logging.debug('Context filter selected')
            context_filter = post_dict['context_filter']
            logging.debug('Context filter set to %s' % context_filter)
            filtered_tasks = filtered_tasks.filter(contexts=context_filter)
        else:
            # No context filter selected, so don't apply a filter
            pass

    # TO DO: Filter projects.
    # For now, just return all projects as though there are no matches
    filtered_projects = None

    # Return list of filtered tasks and filtered projects
    return (
        filtered_tasks,
        filtered_projects
    )
