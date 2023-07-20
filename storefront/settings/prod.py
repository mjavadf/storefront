from .common import *
import environ
import os

# env
env = environ.Env()
environ.Env.read_env()

SECRET_KEY = env("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = []