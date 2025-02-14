from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager
from flask_visjs import Network


@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

class User(db.Document, UserMixin):
    username = db.StringField(unique=True, required=True, min_length=1, max_length=40)
    email = db.EmailField(unique=True, required=True)
    password = db.StringField(required=True)
    group = db.ReferenceField('Group')
    appearances = db.IntField(min_value=0, default=0)
    strengths = db.ListField(db.StringField(min_length=0, max_length=40), default=list)

    # Returns unique string identifying our object
    def get_id(self):
        return self.username
    
    def get_strengths(self):
        return ",".join([s for s in self.strengths])

    def get_attendance_percentage(self):
        total_meets = self.group.meetings if self.group else 1 
        return (self.appearances / total_meets) * 100 if total_meets > 0 else 0
    
        


class Group(db.Document):
    group_name = db.StringField(unique=True, required=True, min_length=1, max_length=40)
    group_members = db.ListField(db.ReferenceField('User'), default=list)
    meetings = db.IntField(min_value=0, default=0)

    def get_edges(self):
        return [(0, i+1, self.group_members[i].appearances) for i in range(len(self.group_members))]
    
    def get_titles(self):
        return [m.strengths for m in self.group_members]

    def get_values(self):
        return [100 for m in self.group_members]
    
    def get_labels(self):
        return [m.username for m in self.group_members]
    
    def get_colors(self):
        return ['blue' for m in self.group_members]
    
    def get_ids(self):
        return [i+1 for i in range(len(self.group_members))]
    
    def get_network(self):
        net = Network("500px", "500px")
        net.add_node(0, value=400, label=self.group_name, color='#dd4b39')
        net.add_nodes(self.get_ids(), value=self.get_values(), title=self.get_titles(), label=self.get_labels(), color=self.get_colors())
        net.add_edges(self.get_edges())
        return net
    



# class Strength(db.Document):
#     strength_name = db.StringField(unique=True, required=True, min_length=1, max_length=40)
#     users = db.ListField(db.ReferenceField('User'), default=list)
