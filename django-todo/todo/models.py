"""
todo app models goes here.
"""
from django.db import models
from django.conf import settings
from django.urls import reverse


class TodoList(models.Model):
    """
    A class that represents a user's todo list.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=120)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}, created: {}, modified: {}'.format(
            self.name,
            self.created,
            self.modified
        )

    @property
    def items(self):
        for todo_list_item_object in TodoListItem.objects.filter(todo_list=self):
            yield todo_list_item_object

    @property
    def completed(self):
        """
        Checks if all items for self are checked.

        :return: True if all are True, False otherwise.
        """
        return all((todo_list_item.done for todo_list_item in self.items))

    def get_absolute_url(self):
        return reverse('todo:list-detail', kwargs={'todo_list_id': self.id})


class TodoListItem(models.Model):
    """
    A class which objects represent todo list items.
    """
    todo_list = models.ForeignKey(TodoList)
    title = models.CharField(max_length=150)
    text = models.TextField(blank=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        return '{} from {} is {}'.format(self.title, self.todo_list.name, 'done' if self.done else 'undone')

    def get_absolute_url(self):
        return reverse(
            'todo:list-item-detail',
            kwargs={'todo_list_id': self.todo_list.id, 'todo_list_item_id': self.id}
        )