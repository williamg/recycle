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

Would save all the files and folders within `~/WebAppTemplate` under the name
"WebApp"

**NOTE**: If you try to same something using a name that has already been
assigned, you will be prompted to overwrite the existing files.
This will completely replace the existing saved files.

### Reusing

To use an existing template, run

    re use NAME_OF_TEMPLATE

This will copy all of the files associated with that name to the current directory.
For example, to create a new web app one might use

    mkdir SuperRadWebApp
    cd SuperRadWebApp
    re use WebApp

Boom! All your files are magically there. You can get started on the fun stuff.

### Listing Saved Files

You can list all the templates you have with

    re list

No explanation needed, hopefully

### Deleting Templates

You can delete a template with

    re delete NAME

As expected, this is permanent and cannot be undone.

## Contributing

Feel free to contribute. All I ask is that you adhere to the existing style,
namely, tabs over spaces, and double quotes over single quotes. All pull requests should
be based on the 'dev' branch.

===

Developed by William Ganucheau. Released under the MIT License.
