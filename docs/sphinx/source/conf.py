from pathlib import Path
from datetime import datetime
import numpy as np
import sys
import os
import json
sep = os.path.sep
sys.path.insert(0, os.path.abspath('..'))
_get_root_path_list = (lambda : (Path(__file__).__str__()).split(sep)[:-4])
lang_tag_map = {
    'en': 'en',
    'zh': 'zh_CN',
    'jp': 'ja'
}


def _get_root_path() -> str:
    return sep.join(_get_root_path_list())


def _inherit_root_metadata():
    with open(_get_root_path() + sep + 'metadata.json', 'r', encoding='utf-8') as f:
        _meta = json.load(f)
    return _meta


def _allocate_doc_version(x: str, vers: list[str]):
    _x = np.array([int(_) for _ in x.split('.')])
    _vers = [[a := _.split('.'),
              a.extend(['0' for i in range(3-len(a))]) if len(a) < 3 else a[:3] if len(a) > 3 else a,
              a][-1] for _ in vers]
    _vers = np.array([[int(j) for j in i] for i in _vers])
    options, _distance = [all((_x - _ >= 0)) for _ in _vers], []
    for v1, v2 in zip(_vers, options):
        if not v2:
            _distance.append(3000)  # max distance
        else:
            _distance.append(np.dot(np.abs(_x - v1), np.array([10, 1, 0.1])))  # weight for majors, minors, patches
    return vers[np.argmin(_distance)]


_metadata = _inherit_root_metadata()
project = _metadata.get('name')
copyright = f"{datetime.now().year}, {_metadata.get('team')}"
author = ', '.join([_.split(' <')[0] for _ in _metadata.get('authors')])
release = _metadata.get('version')
version = _allocate_doc_version(release, _metadata.get('doc_versions'))


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
    'sphinx.ext.intersphinx',
]
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# internationalization configuration
languages = [lang_tag_map.get(_) for _ in _metadata.get('doc_languages')]
language = 'zh_CN'  # default language
locale_dirs = ['../locales/']  # translation scripts
gettext_compact = False
gettext_uuid = True


# multi-versions
html_context = {
    'current_version': version,
    'versions': [ ('latest', '/latest/')] + [(f'{_}', f'/{_}/') for _ in _metadata.get('doc_versions')],
}

# html output
html_theme = 'sphinx_rtd_theme'  # use rtd theme
html_static_path = ['_static']
html_logo = '../images/OUT_logo.svg'
html_favicon = '../images/ALL_logo.jpg'
html_css_files = [
    'custom.css',
]
