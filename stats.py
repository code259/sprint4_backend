import json
import os
from urllib.parse import urljoin, urlparse
from flask import abort, redirect, render_template, request, send_from_directory, url_for, jsonify  # import render_template from "public" flask libraries
from flask_login import current_user, login_user, logout_user
from flask.cli import AppGroup
from flask_login import current_user, login_required
from flask import current_app
from werkzeug.security import generate_password_hash
import shutil
from stockfish import Stockfish
import platform
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func


# import "objects" from "this" project
from __init__ import app, db, login_manager  # Key Flask objects 
# API endpoints
from api.user import user_api 
from api.pfp import pfp_api
from api.nestImg import nestImg_api # Justin added this, custom format for his website
from api.post import post_api
from api.channel import channel_api
from api.group import group_api
from api.section import section_api
from api.nestPost import nestPost_api # Justin added this, custom format for his website
from api.messages_api import messages_api # Adi added this, messages for his website
from api.carphoto import car_api
from api.carChat import car_chat_api
from api.personalInfo import student_api
from api.intro import intro_api
from api.vote import vote_api
# database Initialization functions
from model.carChat import CarChat
from model.user import User, initUsers
from model.section import Section, initSections
from model.group import Group, initGroups
from model.channel import Channel, initChannels
from model.post import Post, initPosts
from model.nestPost import NestPost, initNestPosts # Justin added this, custom format for his website
from model.vote import Vote, initVotes
from model.userstats import UserStats, initUserStats


# server only Views

# register URIs for api endpoints
app.register_blueprint(messages_api) # Adi added this, messages for his website
app.register_blueprint(user_api)
app.register_blueprint(pfp_api)
app.register_blueprint(post_api)
app.register_blueprint(channel_api)
app.register_blueprint(group_api)
app.register_blueprint(section_api)
app.register_blueprint(car_chat_api)
# Added new files to create nestPosts, uses a different format than Mortensen and didn't want to touch his junk
app.register_blueprint(nestPost_api)
app.register_blueprint(nestImg_api)
app.register_blueprint(vote_api)
app.register_blueprint(car_api)
app.register_blueprint(student_api)
app.register_blueprint(intro_api)

@app.route('/api/user_stats', methods=['POST'])
def add_user_stats():
    data = request.get_json()
    user_id = data.get('user_id')
    wins = data.get('wins', 0)
    losses = data.get('losses', 0)

    # Check if the user_id already exists in the database
    existing_stats = UserStats.query.filter_by(user_id=user_id).first()
    if existing_stats:
        return jsonify({"error": "User stats for this user_id already exist"}), 400

    # Create a new UserStats object
    new_stats = UserStats(user_id=user_id, wins=wins, losses=losses)

    try:
        # Add the new stats to the session and commit
        db.session.add(new_stats)
        db.session.commit()
        return jsonify({"message": "User stats added successfully", "data": new_stats.read()}), 201
    except Exception as e:
        # Rollback the session in case of an error
        db.session.rollback()
        return jsonify({"error": str(e)}), 400