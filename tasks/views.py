from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.db.models import Q

from .models import Task, Project, Context
from .forms import TaskFilter
from .utils import apply_filters_from_task_filter


import logging

# LOGGING SETTINGS

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of tasks/views.py')

# Create your views here.


@login_required()
def IndexView(request):
    """
    This class is the homepage that shows all projects and tasks
    together on one page.
    """
    logging.info('Entered IndexView in tasks/views.py')
    logging.info('request.method is %s' % str(request.method))

    # Set user's default task_list
    task_list = Task.objects.filter(
        Q(status='pending'),
        Q(created_by=request.user) | Q(assigned_to=request.user) | Q(supervisor=request.user)
    )
    task_list = task_list.order_by('-updated_date')
    # Set user's default project list
    project_list = Project.objects.filter(
        Q(status='pending'),
        Q(created_by=request.user) | Q(assigned_to=request.user) | Q(supervisor=request.user)
    )
    project_list = project_list.order_by('-created_date')

    # Filter task list if the form
    if request.method != "POST":
        logging.debug('No post data. Returning all tasks and projects.')

        # Dynamically Generate Task Filter
        task_filter = TaskFilter(request_user=request.user)

        # Set context to be sent to the template
        context = {'task_list': task_list, 'project_list': project_list, 'task_filter': task_filter}
        return render(request, 'tasks/index.html', context)

    else:
        # TO DO: Filter for context, status
        post_data = TaskFilter(request.POST, request_user=request.user)
        # Dynamically generate task_filter
        task_filter = TaskFilter(request_user=request.user)
        logging.debug('Created dict for post data. Dict is %s' % post_data)

        # Test whether form data is valid, if so filter
        if post_data.is_valid():
            logging.debug('Post data valid. About to set filters')
            cleaned_data = post_data.cleaned_data
            # Get task and project list by applying filters

            (task_list, project_list) = apply_filters_from_task_filter(     # Use multiple assignment trick
                requesting_user=request.user,
                post_dict=cleaned_data
            )

            # Set context to be passed to render
            context = {'task_filter': task_filter,
                       'task_list': task_list,
                       'project_list': project_list,
            }
            # Return HttpResponse
            return render(request, 'tasks/index.html', context)
        else:
            # The form did not validate.Return default task list,
            # along with bound task filter which should show errors
            context = {
                'task_filter': task_filter,
                'task_list': task_list,
                'project_list': project_list,
            }
            return render(request, 'tasks/index.html', context)


class TaskDetailView(UserPassesTestMixin, DetailView):

    model = Task
    template_name = 'tasks/task_detail.html'

    def test_func(self):
        """
        Test to ensure that user is authorized to view the task
        """
        # If the user is not active, they don't get access
        if not self.request.user.is_active:
            return False
        # Check to see if users should have access to teh task detail
        else:
            return any(
                        [
                            # Allow our staff to have access
                            self.request.user.is_superuser,
                            self.request.user.is_staff,
                            # Allow related users to have access
                            self.request.user == self.get_object().created_by,
                            self.request.user in list(self.get_object().assigned_to.all()),
                            self.request.user == self.get_object().supervisor,
                            self.request.user in list(self.get_object().viewers.all()),
                        ]
            )



class TaskCreate(PermissionRequiredMixin, CreateView):
    """
    This should allow you to create tasks
    """
    permission_required = 'tasks.can_add_task'
    template_name = 'tasks/add-task.html'
    model = Task
    fields = ['name', 'related_projects', 'due_date', 'context',
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
    fields = ['status', 'name', 'related_projects', 'context',
              'due_date', 'notes', 'assigned_to', 'supervisor', 'related_cases', 'related_persons']


class ProjectDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'tasks.can_add_task'
    model = Project
    template_name = 'tasks/project_detail.html'


class ProjectCreate(PermissionRequiredMixin, CreateView):
    """
    Create a project with this view
    """
    permission_required = 'tasks.can_add_task'

    template_name = 'tasks/add-project.html'
    model = Project
    fields = ['name', 'purpose', 'vision', 'big_steps', 'context',
              'due_date', 'under_projects', 'status', 'assigned_to', 'supervisor', 'related_cases', 'related_persons']

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
              'due_date', 'under_projects', 'created_by',
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
        # Ensure user is not inactive
        if not self.request.user.is_active:
            return False
        # If user is active, ensure they are the user for the context
        else:
            return self.request.user == context_object.user