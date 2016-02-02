from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django import forms

from .models import Task, Project, Context
from .forms import TaskFilter
from .utils import get_users_contexts

import logging

# LOGGING SETTINGS

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of tasks/views.py')

# Create your views here.


@permission_required('tasks.can_add_task')
def IndexView(request):
    """
    This class is the homepage that shows all projects and tasks
    together on one page.
    """
    logging.debug('Entered IndexView in tasks/views.py')
    logging.debug('request.method is %s' % str(request.method))

    # Dynamically Generate Task Filter
    task_filter = TaskFilter(user=request.user)

    # Filter task list if the form
    if request.method != "POST":
        logging.debug('No post data. Returning all tasks and projects.')

        # TO DO: Filter task list down to show only tasks created by,
        # assigned to, or supervised by the current user

        task_list = Task.objects.filter(
            Q(status='pending'),
            Q(created_by=request.user) | Q(assigned_to=request.user) | Q(supervisor=request.user)
        )
        task_list = task_list.order_by('-updated_date')

        # Filter task list down to show only projects created by,
        # assigned to, or supervised by the current user
        project_list = Project.objects.filter(
            Q(status='pending'),
            Q(created_by=request.user) | Q(assigned_to=request.user) | Q(supervisor=request.user)
        )
        project_list = project_list.order_by('-created_date')

        # Set context to be sent to the template
        context = {'task_list': task_list, 'project_list': project_list, 'task_filter': task_filter}
        return render(request, 'tasks/index.html', context)

    else:
        # TO DO: Filter for context, priority, status
        post_data = TaskFilter(request.POST)
        logging.debug('Created dict for post data.')

        # Test whether form data is valid, if so filter
        if post_data.is_valid():
            logging.debug('Post data valid. About to set filters')

            # Set filters
            priority_filter = post_data.cleaned_data['priority_filter']
            context_filter = post_data.cleaned_data['context_filter']
            status_filter = post_data.cleaned_data['status_filter']
            type_filter = post_data.cleaned_data['item_filter']
            role_filter = post_data.cleaned_data['role_filter']
            logging.debug('Filter variables assigned. About to apply filters')

            # Set initial task and project lists
            logging.debug('Created task list and project list variables. Assigned all'
                          + 'objects to them')

            # Set initial task and project lists, limiting them to what the user is allowed
            # to see
            task_list = Task.objects.filter(
                Q(created_by=request.user) | Q(assigned_to=request.user) | Q(supervisor=request.user)
            )
            project_list = Task.objects.filter(
                Q(created_by=request.user) | Q(assigned_to=request.user) | Q(supervisor=request.user)
            )

            # Apply context, priority, and status filters to projects
            logging.debug('About to apply type filters.')
            if type_filter == 'both':
                logging.debug('type_filter is both. About to apply context, priority,' +
                              ' and status filters to both tasks and projects')
                task_list = task_list.filter(priority=priority_filter,
                                                 context=context_filter,
                                                 status=status_filter)
                project_list = project_list.filter(priority=priority_filter,
                                                 context=context_filter,
                                                 status=status_filter)
                logging.debug('Set context, priority, and status filters to ' +
                              'task and project lists. About to apply role filters')
                # Apply role filters
                if role_filter == 'created_by':
                    logging.debug('created_by role filter selected. Applying to tasks' +
                                  'and projects')
                    task_list = task_list.filter(created_by=request.user)
                    project_list = project_list.filter(created_by=request.user)
                elif role_filter == 'supervisor':
                    logging.debug('supervisor role_filter selected. About to apply to ' +
                                  'tasks and projects')
                    task_list = task_list.filter(supervisor=request.user)
                    project_list = project_list.filter(supervisor=request.user)
                elif role_filter == 'assigned_to':
                    logging.debug('assigned_to role filter selected. About to apply to ' +
                                  'both tasks and projects')
                    task_list = task_list.filter(supervisor=request.user)
                    project_list = project_list.filter(supervisor=request.user)

            if type_filter == 'project':
                logging.debug('type_filter set to project. Setting task_list to none.')
                task_list = None
                logging.debug('About to filter projects for context, priority, and status.')
                project_list = Project.objects.filter(priority=priority_filter,
                                                 context=context_filter,
                                                 status=status_filter)
                # Apply role filters
                logging.debug('About to apply role filters')
                if role_filter == 'created_by':
                    logging.debug('role_filter set to created_by. About to filter projects.')
                    project_list = project_list.filter(created_by=request.user)
                elif role_filter == 'supervisor':
                    logging.debug('role_filter set to supervisor. About to filter projects')
                    project_list = project_list.filter(supervisor=request.user)
                elif role_filter == 'assigned_to':
                    logging.debug('role_filter set to assigned_to. About to filter projects.')
                    project_list = project_list.filter(supervisor=request.user)
            if type_filter == 'task':
                logging.debug('type_filter set to task. Setting project_list to None')
                logging.debug('Filtering task_list for context, priority, and status')
                task_list = task_list = Task.objects.filter(priority=priority_filter,
                                                 context=context_filter,
                                                 status=status_filter)
                project_list = None
                # Apply role filters
                logging.debug('About to apply role filters')
                if role_filter == 'created_by':
                    logging.debug('role_filter set to created_by. Filtering tasks')
                    task_list = task_list.filter(created_by=request.user)
                elif role_filter == 'supervisor':
                    logging.debug('role_filter set to supervisor. Filtering tasks')
                    task_list = task_list.filter(supervisor=request.user)
                elif role_filter == 'assigned_to':
                    logging.debug('role_filter set to assigned_to. Filtering tasks')
                    task_list = task_list.filter(supervisor=request.user)
            # List Notifications
            notifications = [('FILTERS: Context: %s | Priority: %s | Status: %s | Type: %s | Role: %s'
                             % (context_filter, priority_filter, status_filter, type_filter, role_filter))]
            ''' Notifications put in a list so that multiple notifications can be displayed '''
            # Create Context
            context = {'task_list': task_list,
                       'project_list': project_list,
                       'task_filter': task_filter,
                       'notifications': notifications}
            # Return HttpResponse
            return render(request, 'tasks/index.html', context)
        # TO DO: Need to return form with input data if it is not validated


class TaskDetailView(DetailView):

    model = Task
    template_name = 'tasks/task_detail.html'



class TaskCreate(PermissionRequiredMixin, CreateView):
    """
    This should allow you to create tasks
    """
    permission_required = 'tasks.can_add_task'
    template_name = 'tasks/add-task.html'
    model = Task
    fields = ['name', 'related_projects', 'due_date',
              'notes', 'status', 'assigned_to', 'supervisor', 'related_cases', 'related_persons']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(PermissionRequiredMixin, UpdateView):
    """
    This should allow you to update tasks
    """
    permission_required = 'tasks.can_add_task'
    template_name = 'tasks/update-task.html'
    model = Task
    fields = ['status', 'name', 'related_projects',
              'due_date', 'notes', 'assigned_to', 'supervisor', 'related_cases', 'related_persons']


class ProjectDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'tasks.can_add_task'
    model = Project
    template_name = 'tasks/project-detail.html'


class ProjectCreate(PermissionRequiredMixin, CreateView):
    """
    Create a project with this view
    """
    permission_required = 'tasks.can_add_task'

    template_name = 'tasks/add-project.html'
    model = Project
    fields = ['name', 'purpose', 'vision', 'big_steps',
              'due_date', 'related_projects', 'status', 'assigned_to', 'supervisor', 'related_cases', 'related_persons']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(ProjectCreate, self).form_valid(form)


class ProjectUpdate(PermissionRequiredMixin, UpdateView):
    """
    This will be used to view and update projects
    """
    permission_required = 'tasks.can_add_task'
    template_name = 'tasks/update-project.html'
    model = Project
    context_object_name = 'project'
    fields = ['name','status', 'purpose', 'vision', 'big_steps',
              'due_date', 'related_projects', 'created_by',
              'assigned_to', 'supervisor', 'related_cases', 'related_persons']


    def get_context_data(self, **kwargs):
        '''
        This pulls in related tasks to display them as links.
        '''
        # Call base implementation first to get a context
        context = super(ProjectUpdate, self).get_context_data(**kwargs)
        # TO DO: Add in querysets of related tasks
        context['related_tasks'] = Task.objects.filter(related_projects__id=self.object.id)
        return context


@permission_required('tasks.can_change_context')
def Settings(request):
    """
    This just returns the settings page for the user of the task manager
    """
    return render(request, 'tasks/settings.html')


class ContextTagCreate(PermissionRequiredMixin, CreateView):
    """
    This allows users with permissions to create tags to create their own
    tags for contexts
    """

    permission_required = 'tasks.can_add_context'
    template_name = 'tasks/context-create.html'
    model = Context
    context_object_name = 'context'
    fields = ['name', 'description']

    # Add in the user as the creator of the tag object
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ContextTagCreate, self).form_valid(form)


class ContextTagDetail(UserPassesTestMixin, DetailView):
    """
    This page allows users to view particular tags in detail.
    """
    model = Context
    context_object_name = 'context'
    template_name = 'tasks/context_detail.html'


    def test_func(self):
        """
        This test ensure that the active user (in request.user) is the
        same as the user who owns the tag. self.request.user is the user
        currently browsing the site, and self.object.user is the
        context.user
        """
        logging.debug('Entered test_func in ContextTagDetail view')
        logging.debug('self.request.user is %s' % self.request.user)
        context_object = self.get_object()
        return self.request.user == context_object.user