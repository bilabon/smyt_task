#!/usr/bin/env python

import os
import sys
import modelish.args as m_args
from yaml import load
from modelish.generate import DEFAULT_GRAMMARISH, simple_quote
from smyt_task import settings

APPS_DIR = settings.root('apps')
HELP = "usage:  modelish <source.yml> [--grammar=<grammar.yml> --extra-grammar"
"=<grammar.yml>]"


def simple_error(m):
    sys.stderr.write(m + '\n')
    sys.stderr.write(HELP + '\n')
    sys.exit(1)


def generate_source(source, grammar=DEFAULT_GRAMMARISH):
    global models_py, name_model
    models_py = "from django.db import models\n\n"
    name_models = []
    indent = 0

    def add_line(s):
        global models_py
        models_py += "{}{}\n".format(' ' * 4 * indent, s)
    for model, info in source.items():
        add_line("\nclass {}(models.Model):".format(model))
        indent += 1
        name_models.append(model)
        try:
            docs = info.pop('doc')
            add_line('''"""{}"""'''.format(docs))
            models_py += '\n'
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
            models_py = models_py.rstrip(',\n)')
            models_py += ')\n'
            indent -= 1
        indent -= 1

    # Create text for admin.py
    admin_py = []
    admin_py.append('from django.contrib import admin')
    admin_py.append('from .models import {}\n\n'.format(', '.join(name_models)))
    for name in name_models:
        admin_py.append("admin.site.register({})".format(name))
    admin_py = '\n'.join(admin_py)

    return models_py, admin_py


def rel(*x):
    return os.path.normpath(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), *x),
    )


def main():
    if not m_args.files:
        simple_error('no source yaml file provided')
    if len(m_args.files) > 1:
        simple_error('more than one file provided')
    f = m_args.files[0]
    if not os.path.exists(f):
        simple_error('no such file: {}'.format(f))

    model_source = load(open(f))

    grammar = DEFAULT_GRAMMARISH
    if '--grammar' in m_args.assignments:
        f = m_args.assignments['--grammar']
        if not os.path.exists(f):
            simple_error('no such file: {}'.format(f))
        grammar = load(open(f))
    extra_grammar = {}
    if '--extra-grammar' in m_args.assignments:
        f = m_args.assignments['--extra-grammar']
        if not os.path.exists(f):
            simple_error('no such file: {}'.format(f))
        extra_grammar = load(open(f))
        grammar.update(extra_grammar)

    models_py, admin_py = generate_source(model_source, grammar)

    print '############ FILE data/models.py ############\n', models_py
    print '############ FILE data/admin.py ############\n', admin_py

    var = raw_input("Press <y> to replace files or <n> to cancel.\n")
    if var is 'y':
        for name in ['admin.py', 'models.py']:
            with open(APPS_DIR + '/data/' + name, 'w') as s_file:
                if 'admin' in name:
                    s_file.write(admin_py)
                else:
                    s_file.write(models_py)

if __name__ == '__main__':
    main()
