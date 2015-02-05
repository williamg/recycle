# Recycle

Recycle is a glorified copy-paste utility for managing commonly-used templates
and boilerplate. After creating a template once, you can save it with recycle
for use in the future. Recycle can manage templates for single files or
even entire directory structures.

## Installation
Recycle can be installed with pip:

    pip install recycle

Or by cloning the repo and running

    python setup.py install

## Usage

### Recycling 101

To save some files for later use, simply run

    re new NAME_OF_TEMPLATE LOCATION/OF/FILES

So for example

    re new MathHomework ~/homework.tex

Would save the file `homework.tex` under the name "MathHomework"
Similarly,

    re new WebApp ~/WebAppTemplate/

Would save the directory `~/WebAppTemplate` under the name "WebApp" Recycle also supports globbing which is cool.

**NOTE**: If you try to same something using a name that has already been
assigned, you will be prompted to overwrite the existing files.
This will completely replace the existing saved files.

### Reusing

To use an existing template, run

    re use NAME_OF_TEMPLATE

This will copy all of the files associated with that name to the current directory.
For example, to create a new web app one might use

    re use WebApp

Boom! All your files are magically there. You can get started on the fun stuff. If your template happens to include
a file or directory that already exists in the directory you're trying to use it in, Recycle will ask if you want to
skip that file or directory or overwrite the one that exists.

### Listing Saved Files

You can list all the templates you have with

    re list

No explanation needed, hopefully

### Deleting Templates

You can delete a template with

    re delete NAME

As expected, this is permanent and cannot be undone.

### Changing Recycle Directory
You can change where recycle stores your templates by setting the `RECYCLE_TEMPLATE_DIR`
environmental variable. The default is `~/.recycle/`. You can view the currently used directory
with

    re location


## Changelog
- **v1.1.0** Added support for globbing and configuring the recycle directory.
- **v1.0.0** Initial release of Recycle

## Contributors
Special thanks to all those who have contributed to this project!
- [@ctk3b](http://github.com/ctk3b)
- [@jonesetc](http://github.com/jonesetc)

## Contributing

Feel free to contribute. All I ask is that you adhere to the existing style,
which, thanks to @ctk3b now conforms to the PEP8 guidelines. All pull requests should
be based on the 'master' branch.

===

Developed by William Ganucheau. Released under the MIT License.
