#!/usr/bin/env python
import argparse
import logging
import os
import shutil
import sys
import glob

# Location of saved templates
SAVE_DIR = os.environ.get("RECYCLE_TEMPLATES_DIR", "~/.recycle")

try:
    input = raw_input
except NameError:
    pass

def should_overwrite(typeOfThing, path):
    assert os.path.exists(path)
    nameOfThing = get_name(path)

    logging.debug("{} already exists. Asking to overwrite...".format(path))

    res = ""
    while res != "y" and res != "n":
        prompt = "{0} {1} already exists. Do you want to replace it? " \
                 "(y/n) ".format(typeOfThing, nameOfThing)
        res = input(prompt)
        res = res.lower()

    if res == "y":
        logging.debug("Overwrite approved. Deleting {}".format(path))
        return True
    else:
        logging.debug("Overwrite denied.")
        return False

def copy(contents, dest):
    if not os.path.isdir(dest):
        os.makedirs(dest)

    for obj in contents:
        name = os.path.basename(os.path.normpath(obj))
        destName = os.path.join(dest, name)

        if os.path.exists(destName):
            if should_overwrite("File or directory", destName):
                if os.path.isdir(destName):
                    shutil.rmtree(destName)
                else:
                    os.remove(destName)
            else:
                continue

        assert not os.path.exists(destName)

        if os.path.isdir(obj):
            shutil.copytree(obj, destName)
        elif os.path.isfile(obj):
            shutil.copy(obj, dest)
        else:
            raise IOError("Source doest not exist!")

def get_name(path):
    return os.path.basename(os.path.normpath(path))

def get_save_path(templateName):
    global SAVE_DIR
    return os.path.join(SAVE_DIR, templateName)

def setup_logging():
    global SAVE_DIR

    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s %(levelname)-8s %(message)s",
                        datefmt="%m-%d %H:%M",
                        filename=os.path.join(SAVE_DIR, "recycle.log"),
                        filemode="w")
    console = logging.StreamHandler()

    # INFO or higher goes to console
    console.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)-8s %(message)s")
    console.setFormatter(formatter)

    logging.getLogger("").addHandler(console)

def init():
    global SAVE_DIR

    SAVE_DIR = os.path.expanduser(SAVE_DIR)
    SAVE_DIR = os.path.expandvars(SAVE_DIR)
    SAVE_DIR = os.path.abspath(SAVE_DIR)

    if not os.path.isdir(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    setup_logging()
    logging.debug("Using Python version {}".format(sys.version))

def handle_new(name, files):
    save_path = get_save_path(name)

    fileList = []
    for filename in files:
        fileList += [os.path.abspath(f) for f in glob.glob(filename)]

    # Remove duplicates
    fileList = list(set(fileList))

    if len(fileList) is 0:
        logging.error("No files found matching '{}'".format(files))
        return

    if os.path.isdir(save_path):
        # Boilerplate with that name already exists
        if should_overwrite("Template", save_path):
            handle_delete(name)
        else:
            return

    assert not os.path.isdir(save_path)
    logging.debug("Creating new template '{}' from {}".format(name, files))

    try:
        copy(fileList, save_path)
    except IOError as e:
        logging.error(e.strerror)

    assert os.path.isdir(save_path)
    logging.debug("Boilerplate created!")


def handle_use(name):
    save_path = get_save_path(name)

    if os.path.isdir(save_path):
        logging.debug("Using template '{}'".format(name))

        contents = os.listdir(save_path)
        contentPaths = [os.path.join(save_path, c) for c in contents]

        try:
            copy(contentPaths, os.getcwd())
        except IOError as e:
            logging.error("Your recycle directory doesn't seem to exist...")
    else:
        logging.error("No template with the name '{}' was found!".format(name))


def handle_list():
    global SAVE_DIR
    assert os.path.isdir(SAVE_DIR)

    names = next(os.walk(SAVE_DIR))[1]
    for line in names:
        if line.startswith(SAVE_DIR):
            line = line[len(SAVE_DIR):-1]
        print(line)


def handle_delete(name):
    save_path = get_save_path(name)

    if os.path.isdir(save_path):
        shutil.rmtree(save_path)
    else:
        logging.error("No template with the name '{}'  was found!".format(name))

    assert not os.path.isdir(save_path)


def handle_location():
    global SAVE_DIR

    print(os.path.normpath(SAVE_DIR) + os.sep)


def parseargs():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()

    new_parser = subparsers.add_parser(
        "new", help="Create a new template or overwrite an existing one")
    new_parser.add_argument(
        "name", type=str, help="The name under which to save this template")
    new_parser.add_argument(
        "files", type=str, nargs="+",
        help="The file or directory to save as the template")
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

    location_parser = subparsers.add_parser(
        "location", help="Print the current location of the templates directory")
    location_parser.set_defaults(mode="location")

    return parser.parse_args()


def main():
    args = parseargs()
    init()

    if args.mode is None:
        logging.error("Mode must be provided. Use --help for more information.")
        return

    if args.mode is "new":
        handle_new(args.name, args.files)
    elif args.mode is "use":
        handle_use(args.name)
    elif args.mode is "list":
        handle_list()
    elif args.mode is "delete":
        handle_delete(args.name)
    elif args.mode is "location":
        handle_location()
    else:
        logging.error("Invalid mode")


if __name__ == "__main__":
    main()
