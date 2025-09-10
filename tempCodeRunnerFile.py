from flask import Flask, render_template, request, redirect, url_for,session
from geopy.geocoders import Nominatim
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import folium
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo
from bson import ObjectId
from werkzeug.utils import secure_filename
import os
import pickle
import jsonify
from pymongo import MongoClient
import plotly.express as px
import plotly
import plotly.figure_factory as ff
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import requests
import datetime
from dotenv import load_dotenv
import google.generativeai as genai  # Import the Gemini library
from gtts import gTTS
import asyncio
import string
from folium.plugins import FastMarkerCluster
from datetime import datetime
import crops
import random
sns.set()

app = Flask(__name__)
CORS(app)