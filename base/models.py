from django.db import models as m

from uuid import uuid4

class Customer(m.Model):

    uid = m.UUIDField(default = uuid4)

    website_type = m.TextField(null = True)
    name = m.TextField(null = True)
    email = m.TextField(null = True)
    phone = m.TextField(null = True)

    sent_at = m.DateTimeField(auto_now_add = True)
    updated_at = m.DateTimeField(auto_now = True)

    def __str__(self):

        return self.name

class ButtonClick(m.Model):
    
    uid = m.UUIDField(default = uuid4)

    clicked_at = m.DateTimeField(auto_now_add = True)

    def __str__(self):

        return self.clicked_at