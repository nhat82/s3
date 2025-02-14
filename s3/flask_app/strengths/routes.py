from ssl import CertificateError
from flask import Blueprint, render_template, url_for, redirect, request, flash
from ..forms import *
from ..models import *
from ..utils import current_time
from flask_visjs import Network
from flask_login import current_user, login_required, login_user, logout_user
from mongoengine.errors import NotUniqueError
from werkzeug.utils import secure_filename

strengths = Blueprint("strengths", __name__)

""" ************ View functions ************ """
@strengths.route('/')
def index():
    if current_user.is_authenticated:
        current_group = current_user.group
        if current_group:
            my_network = current_group.get_network()
            return render_template('index.html', graph=my_network)
        else:
            return render_template("nogroup.html")
    
    return render_template("404.html")

@strengths.route('/class_view')
def class_view():
    if current_user.is_authenticated:
        
        net = Network("500px", "500px")
        # all user nodes
        all_users = User.objects()
        
        for user in all_users:
            for st in user.strengths:
                STRENGTH_COUNT[st] += 1
                ct = STRENGTH_TO_CATAGORY[st]
                if user.username not in STRENGTH_USERS[st]:
                    STRENGTH_USERS[st].append(user.username)
                CATEGORIES_COUNT[ct] += 1
        
        for st, ct in STRENGTH_TO_CATAGORY.items():
            if STRENGTH_COUNT[st] > 0:
                net.add_node(st, 
                            value=STRENGTH_COUNT[st]*1000, 
                            label=st, 
                            title=", ".join(STRENGTH_USERS[st]), 
                            color="#87807f"
                            )
                net.add_node(ct, 
                            value=500, 
                            label=ct, 
                            title=ct, 
                            color=CATAGORY_TO_COLOR[ct]
                            )
                net.add_edge(st, ct, weight=STRENGTH_COUNT[st])
                
        # sorted_strength_count = sorted(STRENGTH_COUNT.items(), key=lambda x: x[1], reverse=True)
        sorted_strength_count = [(strength, count) for strength, count in sorted(STRENGTH_COUNT.items(), key=lambda x: x[1], reverse=True) if count > 0]

        # print(sorted_strength_count)
        
        return render_template('class_view.html', graph=net, sorted_strength_count = sorted_strength_count)
    
    return render_template("404.html")



    
STRENGTH_TO_CATAGORY = {
    "achiever": "executing",
    "arranger": "executing",
    "belief": "executing",
    "consistency": "executing",
    "deliberative": "executing",
    "discipline": "executing",
    "focus": "executing",
    "responsibility": "executing",
    "restorative": "executing",
    
    "activator": "influencing",
    "command": "influencing",
    "communication": "influencing",
    "competition": "influencing",
    "maximizer": "influencing",
    "self-assurance": "influencing",
    "significance": "influencing",
    "woo": "influencing",
    
    "adaptability": "relationship building",
    "connectedness": "relationship building",
    "developer": "relationship building",
    "empathy": "relationship building",
    "harmony": "relationship building",
    "includer": "relationship building",
    "individualization": "relationship building",
    "positivity": "relationship building",
    "relator": "relationship building",
    
    "analytical": "strategic thinking",
    "context": "strategic thinking",
    "futuristic": "strategic thinking",
    "ideation": "strategic thinking",
    "input": "strategic thinking",
    "intellection": "strategic thinking",
    "learner": "strategic thinking",
    "strategic": "strategic thinking"
}

STRENGTH_COUNT = {  
    "achiever": 0, "arranger": 0, "belief": 0, "consistency": 0,  
    "deliberative": 0, "discipline": 0, "focus": 0, "responsibility": 0, "restorative": 0,  
    "activator": 0, "command": 0, "communication": 0, "competition": 0,  
    "maximizer": 0, "self-assurance": 0, "significance": 0, "woo": 0,  
    "adaptability": 0, "connectedness": 0, "developer": 0, "empathy": 0,  
    "harmony": 0, "includer": 0, "individualization": 0, "positivity": 0, "relator": 0,  
    "analytical": 0, "context": 0, "futuristic": 0, "ideation": 0,  
    "input": 0, "intellection": 0, "learner": 0, "strategic": 0  
}

STRENGTH_USERS = {  
    "achiever": [], "arranger": [], "belief": [], "consistency": [],  
    "deliberative": [], "discipline": [], "focus": [], "responsibility": [], "restorative": [],  
    "activator": [], "command": [], "communication": [], "competition": [],  
    "maximizer": [], "self-assurance": [], "significance": [], "woo": [],  
    "adaptability": [], "connectedness": [], "developer": [], "empathy": [],  
    "harmony": [], "includer": [], "individualization": [], "positivity": [], "relator": [],  
    "analytical": [], "context": [], "futuristic": [], "ideation": [],  
    "input": [], "intellection": [], "learner": [], "strategic": []  
}


CATAGORY_TO_COLOR = {
    'executing':"#6A0DAD",
    'influencing':"#FF8C00",
    "relationship building": "#0073CF",
    "strategic thinking": "#2E8B57"
}

CATEGORIES_COUNT = {"executing": 0, 
                "influencing": 0, 
                "relationship building": 0,
                "strategic thinking": 0
            }
