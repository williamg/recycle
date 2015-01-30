#!/usr/bin/env python
import sys, argparse, logging, os, subprocess

# Box syncing
SAVE_DIR = os.path.expanduser("~") + "/.recycle/"

try:
	input = raw_input
except NameError:
	pass

def call_command(command):
	logging.debug("Executing " + command)
	comm = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	return comm.communicate()

def init():
	if not os.path.isdir(SAVE_DIR):
		call_command("mkdir " + SAVE_DIR)

	logging.basicConfig(level = logging.DEBUG,
		format = "%(asctime)s %(levelname)-8s %(message)s",
		datefmt = "%m-%d %H:%M",
		filename = SAVE_DIR + "recycle.log",
		filemode = "w")
	console = logging.StreamHandler()

	# INFO or higher goes to console
	console.setLevel(logging.INFO)
	formatter = logging.Formatter("%(levelname)-8s %(message)s")
	console.setFormatter(formatter)

	logging.getLogger("").addHandler(console)

	logging.debug("Using Python version " + sys.version)

def handleNew(name, files):
	save_path = SAVE_DIR + name

	if os.path.isdir(save_path):
		# Boilerplate with that name already exists
		logging.debug(save_path + " already exists. Asking to overwrite...")

		res = ""
		while res != "y" and res != "n":
			res = input("Template '" + name + "' already exists. "
			            "Do you want to replace its contents? (y/n) ")
			res = res.lower()

		if res == "n":
			logging.debug("Overwrite denied. Aborting")
			return
		else:
			logging.debug("Overwrite approved. Deleting " + save_path)
			call_command("rm -rf " + save_path)

	assert not os.path.isdir(save_path)
	call_command("mkdir -p " + save_path)

	files = os.path.abspath(files)
	logging.debug("Creating new template '" + name + "' from " + files)

	if os.path.isdir(files):
		files += "/*"

	command = "cp -r " + files + " " + save_path
	call_command(command)

	assert os.path.isdir(save_path)
	logging.debug("Boilerplate created!")

def handleUse(name):
	save_path = SAVE_DIR + name

	if os.path.isdir(save_path):
		logging.debug("Using template '" + name + "'")
		command = "cp -r " + save_path + "/*" + " ."
		call_command(command)
	else:
		logging.error("No template with the name '" + name + "'  was found!")

def handleList():
	assert os.path.isdir(SAVE_DIR)

	names = next(os.walk(SAVE_DIR))[1]
	nameCount = len(names)
	idx = 0
	
	for line in names:
		idx += 1

		if line.startswith(SAVE_DIR):
			line = line[len(SAVE_DIR):-1]

		print(line)

def handleDelete(name):
	save_path = SAVE_DIR + name

	if os.path.isdir(save_path):
		logging.debug("Deleting template '" + name + "'")
		command = "rm -r " + save_path
		call_command(command)
	else:
		logging.error("No template with the name '" + name + "'  was found!")

	assert not os.path.isdir(save_path)

def parseargs():
	parser = argparse.ArgumentParser()

	subparsers = parser.add_subparsers()

	new_parser = subparsers.add_parser(
		"new", help="Create a new template or overwrite an existing one")
	new_parser.add_argument(
		"name", type=str, help="The name under which to save this template")
	new_parser.add_argument(
		"files", type=str, help="The file or directory to save as the template")
	new_parser.set_defaults(mode="new")

	use_parser = subparsers.add_parser(
		"use", help="Insert existing template in the current directory")
	use_parser.add_argument(
		"name", type=str, help="The name of the template to use")
	use_parser.set_defaults(mode="use")

	list_parser = subparsers.add_parser(
		"list", help="List the available template")
	list_parser.set_defaults(mode="list")

	delete_parser = subparsers.add_parser(
		"delete", help="Delete a template")
	delete_parser.add_argument(
		"name", type=str, help="The name of the template to delete")
	delete_parser.set_defaults(mode="delete")

	return parser.parse_args()

def main():
	args = parseargs()
	init()

	if args.mode is None:
		logging.error("Mode must be provided. Use --help for more information.")
		return

	if args.mode is "new":
		handleNew(args.name, args.files)
	elif args.mode is "use":
		handleUse(args.name)
	elif args.mode is "list":
		handleList()
	elif args.mode is "delete":
		handleDelete(args.name)
	else:
		logging.error("Invalid mode")

