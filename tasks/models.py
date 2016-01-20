from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from case_manager.models import Case
from people_and_property.models import Person

# from people_and_property.models import person

import uuid

# CONSTANTS

CONTEXTS = (
    ('@work', '@work'),
    ('@home', '@home'),
    ('@town', '@town'),
    ('@philosophy', '@philosophy'),
)

PRIORITIES = (
    ('1-Now', '1-Now'),
    ('2-Next', '2-Next'),
    ('3-Soon', '3-Soon'),
    ('4-Later', '4-Later'),
    ('5-Even Later', '5-Even Later'),
    ('6-Someday/Maybe', '6-Someday/Maybe'),
    ('7-Waiting', '7-Waiting'),
    ('8-In Queu', '8-In Queau'),
    ('9-On Hold', '9-On Hold'),
)

STATUSES = (
    ('pending', 'pending'),
    ('complete', 'complete')
)


# CLASSES
class Project(models.Model):
    """
    Project is for any multi-step thing that needs to be done. Tasks
    will be associated with it.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=200)

    purpose = models.TextField(blank=True)
    """What is my purpose with this task?"""

    vision = models.TextField(blank=True)
    """Vision refers to what the task will look like when successfully
    completed"""

    big_steps = models.TextField(blank=True)
    """What are the big steps (not task-level steps) that need to be
    completed? Maybe split this out into a new class, similar to tasks"""

    created_by = models.ForeignKey(User, related_name='project_created_by', limit_choices_to={'is_staff': True})
    assigned_to = models.ForeignKey(User, related_name='project_assigned_to', limit_choices_to={'is_staff': True})
    """assigned_to refers to the person currently working on task"""
    supervisor = models.ForeignKey(User, related_name='project_supervisor', limit_choices_to={'is_staff': True})
    """ Supervisor refers to the person responsible for ensuring the
    task is complete"""
    status = models.CharField(max_length=30, choices=STATUSES, default='pending')
    """Status will be either 'pending' or 'complete'"""
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    context = models.CharField(max_length=50, choices=CONTEXTS)
    priority = models.CharField(max_length=50, choices=PRIORITIES)
    due_date = models.DateTimeField(blank=True, null=True)
    related_project = models.ForeignKey("self", blank=True, null=True)
    """under_project links to the project over this project, making this
    project a sub project of another project"""

    # Foreign fields relating to other apps
    related_cases = models.ManyToManyField(Case, related_name='projects_rel_to_case')
    related_persons = models.ManyToManyField(Person, related_name='projects_rel_to_person')

    def __str__(self):
        return self.name




class Task(models.Model):
    """
    A task is a one step item that needs to be done that may or may not be
    associated with a project.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, related_name='task_created_by', limit_choices_to={'is_staff': True})
    assigned_to = models.ForeignKey(User, related_name='task_assigned_to', limit_choices_to={'is_staff': True})
    """assigned_to refers to the person currently working on task"""
    supervisor = models.ForeignKey(User, related_name='task_supervisor', limit_choices_to={'is_staff': True})
    """ Supervisor refers to the person responsible for ensuring the
    task is complete"""
    status = models.CharField(max_length=30, choices=STATUSES, default='pending')
    """Status will be either 'pending' or 'complete'"""
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    context = models.CharField(max_length=50, choices=CONTEXTS)
    priority = models.CharField(max_length=50, choices=PRIORITIES)
    due_date = models.DateTimeField(blank=True, null=True)
    related_project = models.ForeignKey(Project, blank=True, null=True)
    notes = models.TextField(blank=True)

    # Relations to other apps
    related_cases = models.ManyToManyField(Case, related_name='tasks_rel_to_case')
    related_persons = models.ManyToManyField(Person, related_name='tasks_rel_to_person')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('task_manager:task_detail', kwargs={'pk': self.pk})

