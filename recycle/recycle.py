#!/usr/bin/env python
import argparse
import logging
import os
import shutil
import sys

# Location of saved templates
SAVE_DIR = os.path.expanduser("~") + "/.recycle/"

try:
    input = raw_input
except NameError:
    pass


def init():
    if not os.path.isdir(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s %(levelname)-8s %(message)s",
                        datefmt="%m-%d %H:%M",
                        filename=SAVE_DIR + "recycle.log",
                        filemode="w")
    console = logging.StreamHandler()

    # INFO or higher goes to console
    console.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)-8s %(message)s")
    console.setFormatter(formatter)

    logging.getLogger("").addHandler(console)
    logging.debug("Using Python version " + sys.version)


def handle_new(name, files):
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
            handle_delete(name)

    assert not os.path.isdir(save_path)

    files = os.path.abspath(files)
    logging.debug("Creating new template '" + name + "' from " + files)

    if os.path.isdir(files):
        shutil.copytree(files, save_path)
    elif os.path.isfile(files):
        os.makedirs(save_path)
        shutil.copy(files, save_path)
    else:
        logging.error("Source '" + files + "' not found!")
        return

    assert os.path.isdir(save_path)
    logging.debug("Boilerplate created!")


def handle_use(name):
    save_path = SAVE_DIR + name

    if os.path.isdir(save_path):
        logging.debug("Using template '" + name + "'")

        contents = os.listdir(save_path)
        for obj in contents:
            path = os.path.join(save_path, obj)

            if os.path.isdir(path):
                dest = os.path.join(os.getcwd(), obj)
                shutil.copytree(path, dest)
            elif os.path.isfile(path):
                shutil.copy(path, os.getcwd())
            else:
                logging.debug("Skipping template content '" + path + "'")
    else:
        logging.error("No template with the name '" + name + "'  was found!")


def handle_list():
    assert os.path.isdir(SAVE_DIR)

    names = next(os.walk(SAVE_DIR))[1]
    idx = 0

    for line in names:
        idx += 1

        if line.startswith(SAVE_DIR):
            line = line[len(SAVE_DIR):-1]

        print(line)


def handle_delete(name):
    save_path = SAVE_DIR + name

    if os.path.isdir(save_path):
        shutil.rmtree(save_path)
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
        handle_new(args.name, args.files)
    elif args.mode is "use":
        handle_use(args.name)
    elif args.mode is "list":
        handle_list()
    elif args.mode is "delete":
        handle_delete(args.name)
    else:
        logging.error("Invalid mode")


if __name__ == "__main__":
    main()
