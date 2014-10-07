#!/usr/bin/env python

import os
import sys
import re
import modelish.args as m_args
from yaml import load
from modelish.generate import DEFAULT_GRAMMARISH, simple_quote
from smyt_task import settings

HELP = "usage:  modelish <source.yml>"


def simple_error(m):
    sys.stderr.write(m + '\n')
    sys.stderr.write(HELP + '\n')
    sys.exit(1)


def generate_source(source, grammar=DEFAULT_GRAMMARISH):
    """Generating text for admin.py and models.py"""

    global models_py
    models_py = []
    name_models = []
    models_py.append("from django.db import models\n")

    indent = 0

    def add_line(s):
        global models_py
        models_py.append("{}{}\n".format(' ' * 4 * indent, s))

    for model, info in source.items():
        add_line("\n\nclass {}(models.Model):".format(model))
        indent += 1
        name_models.append(model)
        try:
            docs = info.pop('doc')
            add_line('''"""{}"""'''.format(docs))
            models_py.append('\n')
        except KeyError:
            pass
        for field, fdata in info.items():
            if '-' in field:
                field, the_type = [s.strip() for s in field.split('-')]
            else:
                the_type = fdata.pop('type')
            field_type = grammar['types'][the_type]
            add_line("{} = models.{}(".format(field, field_type))
            indent += 1
            args = fdata.pop('args', [])
            if not isinstance(args, list):
                if ',' in args:
                    args = args.split(',')
                else:
                    args = [args]
            for arg in args:
                add_line('{},'.format(simple_quote(arg)))
            field_info = grammar['defaults'].get(the_type, {}).copy()
            field_info.update(fdata)
            for kwarg, value in field_info.items():
                add_line("{}={},".format(kwarg, simple_quote(value)))
            models_py.append(')\n')
            indent -= 1
        indent -= 1

    # Create text for admin.py
    admin_py = []
    admin_py.append('from django.contrib import admin')
    admin_py.append(
        'from .models import {}\n\n'.format(', '.join(name_models))
    )
    for name in name_models:
        admin_py.append("admin.site.register({})".format(name))
    admin_py = '\n'.join(admin_py)

    # Create text for models.py
    models_py = re.sub(',\)|\\n\)|,\\n\)', ')', ''.join(models_py))
    return models_py, admin_py


def main():
    if not m_args.files:
        simple_error('no source yaml file provided')
    if len(m_args.files) > 1:
        simple_error('more than one file provided')
    f = m_args.files[0]
    if not os.path.exists(f):
        simple_error('no such file: {}'.format(f))

    model_source = load(open(f))

    models_py, admin_py = generate_source(model_source, DEFAULT_GRAMMARISH)

    print '############ FILE data/models.py ############\n', models_py
    print '############ FILE data/admin.py ############\n', admin_py

    var = raw_input("Press <y> to replace files or <n> to cancel.\n")
    apps_dir = settings.root('apps')
    if var is 'y':
        for name in ['admin.py', 'models.py']:
            with open(apps_dir + '/data/' + name, 'w') as s_file:
                if 'admin' in name:
                    s_file.write(admin_py)
                else:
                    s_file.write(models_py)

if __name__ == '__main__':
    main()
