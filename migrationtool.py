#!/usr/bin/env python3

import glob
import os
from settings import INSTALLED_APPS
import re
from pathlib import Path

pattern = '../**/models'

appsdir = '..'

needs_migrations = []
needs_init = []
installed_apps = []
apps = {}

class App:
	def __init__(self, name):
		self.name = name
		self.needs_migration = False
		self.needs_init = False
		self.migrations = []
		self.valid = True
		


def getApps():
	for fname in os.listdir(appsdir):
		if fname in INSTALLED_APPS:
			app = App(fname)
			apps[app.name] = app
			installed_apps.append(fname)



def checkMigrations():
	
	for app in apps:
		app = apps[app]
		migration_found = False
		init_found = False


		dir  = f'{appsdir}/{app.name}/'
		app.dir = dir
		pattern = f'{dir}**'
		for fname in glob.glob(pattern, recursive=False):
			folder = re.sub(dir,'',fname)
			if os.path.isdir(fname):
				if folder == 'migrations':
					migration_found = True
					pattern2 = f'{dir}migrations/**'
					for fname in glob.glob(pattern2, recursive=False):
						file = re.sub(f'{dir}migrations/','',fname)
						if file == '__init__.py':
							init_found = True
						elif file != '__pycache__':
							app.migrations.append(file)
		if not migration_found:
			app.needs_migration = True
			app.valid = False
		if not init_found:
			app.needs_init = True
			app.valid = False		


			
def getDetails():
	for app in apps:
		print("\n")

		app = apps[app]
		print("name:", app.name)
		print("needs_migration:", app.needs_migration)
		print("needs_init:", app.needs_init)
		print("valid:", app.valid)
		print("dir:", app.dir)
		print("Migrations:")
		print(app.migrations)
		for migration in app.migrations:
			print(migration)
		

def fixMigrations():
	for app in apps:
		app = apps[app]
		if not app.valid:
			mode = 0o666
			migration_dir = f'{app.dir}migrations'
			if app.needs_migration:
				print("Making Dir")
				os.makedirs(migration_dir,mode)
			if app.needs_init:
				print("Creating Init")
				try:
					open(f"{migration_dir}/__init__.py", "a").close()
				except PermissionError:
					print(f"Permission Error: writing empty __init__.py file in {migration_dir}\nTry Running as Root")
				


def main():
	getApps()
	# for app in apps:
	# 	print(app)
	

	checkMigrations()
	getDetails()
	fixMigrations()


# checkMigrations(apps)
main()


