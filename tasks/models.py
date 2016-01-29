from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from case_manager.models import Case
from people_and_property.models import Person

import uuid

# CONSTANTS

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
    assigned_to = models.ManyToManyField(User, related_name='project_assigned_to', limit_choices_to={'is_staff': True})
    """assigned_to refers to the person currently working on task"""
    supervisor = models.ForeignKey(User, related_name='project_supervisor', limit_choices_to={'is_staff': True})
    """ Supervisor refers to the person responsible for ensuring the
    task is complete"""
    viewers = models.ManyToManyField(User,
                                     verbose_name='Who can view this project?',
                                     help_text='Who has permission to see this project?')
    status = models.CharField(max_length=30, choices=STATUSES, default='pending')
    """Status will be either 'pending' or 'complete'"""
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    under_projects = models.ManyToManyField("self",
                                            blank=True,
                                            symmetrical=False,
                                            related_name='subordinate_projects')
    """under_projects links to any projects over this project, making this
    project a sub project of another project"""
    level = models.CharField(help_text=('Level refers to how high level a project is, between 1 and 3. A Level 1 ') +
                                       ('project would be something like "start a marketing business", while ') +
                                       ('Level 3 would be something like design a poster.'),
                             choices=(
                                 ('1', 'Level 1'),
                                 ('2', 'Level 2'),
                                 ('3', 'Level 3'),
                             ),
                             max_length=10,
                             default='3',
    )

    # Foreign fields relating to other apps
    related_cases = models.ManyToManyField(Case, related_name='projects_rel_to_case')
    related_persons = models.ManyToManyField(Person, related_name='projects_rel_to_person')

    def __str__(self):
        return self.name

    # TO DO: Set an absolute url



class Task(models.Model):
    """
    A task is a one step item that needs to be done that may or may not be
    associated with a project.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, related_name='task_created_by', limit_choices_to={'is_staff': True})
    assigned_to = models.ManyToManyField(User, related_name='task_assigned_to', limit_choices_to={'is_staff': True})
    """assigned_to refers to the person currently working on task"""
    supervisor = models.ForeignKey(User, related_name='task_supervisor', limit_choices_to={'is_staff': True})
    """ Supervisor refers to the person responsible for ensuring the
    task is complete"""
    viewers = models.ManyToManyField(User,
                                     related_name='tasks_user_can_view',
                                     verbose_name='Users who can view',
                                     help_text='Who do you want to be able to observe this task?')
    status = models.CharField(max_length=30, choices=STATUSES, default='pending')
    """Status will be either 'pending' or 'complete'"""
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    related_projects = models.ManyToManyField(Project, blank=True)
    notes = models.TextField(blank=True)

    # Relations to other apps
    related_cases = models.ManyToManyField(Case, related_name='tasks_rel_to_case')
    related_persons = models.ManyToManyField(Person, related_name='tasks_rel_to_person')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('task_manager:task_detail', kwargs={'pk': self.pk})


class Context(models.Model):
    """
    The purpose of Context is to allow users to assign their own context to
    a project or task. Each user, even if they are looking at the "same" task,
    will see their own context. For example, if the assigned user as @work
    but the supervisor has @office, each will see their respective context.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, default='@work')
    description = models.TextField(max_length=200, blank=True)
    user = models.ForeignKey(User, related_name='task_contexts')
    projects = models.ManyToManyField(Project, related_name='context_for_project')
    tasks = models.ManyToManyField(Task, related_name='context_for_task')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('task_manager:context_detail', kwargs={'pk': self.pk})