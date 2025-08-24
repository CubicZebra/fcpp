from typing import TypeVar, Optional
from pathlib import Path
import numpy as np
import os
import json
import shutil
import re
import subprocess
sep = os.path.sep
Language = TypeVar('Language')
Version = TypeVar('Version')
_get_root_path_list = (lambda : (Path(__file__).__str__()).split(sep)[:-2])
_root_path_list = _get_root_path_list()
_pair_capture = {
    'h': 'c',
    'c': 'h',
    'hpp': 'cpp',
    'cpp': 'hpp'
}


def _get_root_path() -> str:
    return sep.join(_get_root_path_list())


def _inherit_root_metadata():
    with open(_get_root_path() + sep + 'metadata.json', 'r', encoding='utf-8') as f:
        _meta = json.load(f)
    return _meta


_hit_com_tag = re.compile(r" \* @")
_hit_lang_tag = re.compile(rf"( \* @[a-z]+).*\[({'|'.join(_inherit_root_metadata().get('doc_doxygen_languages'))})] ")
_hit_free_tag = re.compile(r" \* [^@]+")
_hit_file_doc = re.compile(r"\n?/\*!(.|\n)*@file(.|\n)*@defgroup")
_hit_since_command = re.compile(r"\n?/\*\*(.|\n)*@since ")
language_map = {'en': 'English', 'zh': 'Chinese', 'jp': 'Japanese'}


def _no_recursive_clean_img(x: str):
    if os.path.exists(x):
        for f in os.listdir(x):
            os.remove(x + sep + f)


def _idx_slicer(x: np.ndarray) -> list[list[int]]:
    res, _in_selection = [], False
    for i, v in enumerate(x):
        if not (v[0] == True and v[1] == True and v[2] == False):
            if v[0] == True and v[1] == False and v[2] == False:
                _in_selection = False
            if _in_selection:
                res[-1].append(i)
        else:
            res.append([i])
            _in_selection = True
    return res


def _determine_sub_groups(x: list[list[int]], languages: list[str],
                          _regex_ref: list[list[Optional[re.Match]]]) -> tuple[dict[str, list[int]], list[int]]:
    res = {k: [] for k in languages}
    for _set in x:
        _match = _regex_ref[_set[0]][1]
        res[_match.group(2)].extend(_set)
    return res, [_[0] for _ in x]


def _language_filter(lines: list[str], langs: list[str], lang_tag: Language) -> list[str]:

    container = []
    _refs = [[_hit_com_tag.match(l), _hit_lang_tag.match(l), _hit_free_tag.match(l)] for l in lines]
    _refs_bool = np.array([[j is not None for j in i] for i in _refs])
    _idx_sets = _idx_slicer(_refs_bool)
    _lang_involved_lines, _lang_tag_hit_line = _determine_sub_groups(_idx_sets, langs, _refs)
    _all_lang_involved_lines = []

    for k, v in _lang_involved_lines.items():
        _all_lang_involved_lines.extend(v)

    for i, l in enumerate(lines):
        if i not in _all_lang_involved_lines:
            container.append(l)
        else:
            if i in _lang_involved_lines[lang_tag]:

                if i in _lang_tag_hit_line:
                    _sp = _refs[i][1].regs[2][1]
                    container.append(l[:(_sp-4)] + l[_sp + 1:])
                else:
                    container.append(l)

    return container


def _clean_doxygen_build(root: str):
    for f in os.listdir(root):
        full_path = root + sep + f
        if os.path.isdir(full_path):
            if f.startswith('_'):  # clean temporary folders
                shutil.rmtree(full_path)
            else:
                _clean_doxygen_build(full_path)
        elif f == 'Doxyfile.in':  # clean generated Doxyfile
            os.remove(full_path)


def _file_collector(folders: list[str], obj: list[str]) -> list[tuple[str, str]]:
    res = []
    for folder in folders:
        entry = Path(folder)
        for _obj in obj:
            res.extend(list(entry.rglob(f"*.{_obj}")))
    return [(os.path.dirname(str(file)), os.path.basename(str(file))) for file in res]


def _ver_should_include(x: str, ref_ver: str) -> bool:
    _x, _r = [int(_) for _ in x.split('.')], [int(_) for _ in ref_ver.split('.')]
    while len(_x) < 3:
        _x.append(0)
    while len(_r) < 3:
        _r.append(0)
    res = True  # for all equal
    for a, b in zip(_x, _r):
        if a < b:
            return True
        elif a > b:
            return False
        else:  # equal
            continue
    return res


def _ver_filter(x: list[str], ver: str) -> tuple[list[str], str]:
    x = (''.join(x)).split('\n\n\n')
    container, _need_append_end, file_ver = [], False, ''
    for i, block in enumerate(x):  # x[0] for import declaration
        if _hit_file_doc.match(block):
            if '@since ' in block:
                file_ver = block.split('@since ')[1].split(' ')[0].strip()
            container.append(block+'\n//! @{')
            _need_append_end = True
        elif _match := _hit_since_command.match(block):
            _obj_ver = block[_match.regs[1][0]:].split('@since ')[1].split(' ')[0]  # version getter
            if _ver_should_include(_obj_ver, ver):
                container.append(block)
        else:
            container.append(block)
    if _need_append_end:
        container.append('//! @}\n')
    return container, file_ver


def _generate_docs_index(languages: list[str], versions: list[str], lib: str) -> str:
    lang_display = {
        'en': ('English', '🇬🇧'),
        'zh': ('中文', '🇨🇳'),
    }

    version_groups = ""
    for version in sorted(versions, reverse=True):
        group = f'    <!-- 版本 {version} -->\n'
        group += f'    <div class="version-group">\n'
        group += f'      <h2 class="version-title">Version {version}</h2>\n'
        group += f'      <ul class="lang-links">\n'

        for lang in languages:
            lang_name, flag = lang_display.get(lang, (lang.capitalize(), ""))
            link_path = f"./{lang}/v{version}/build_sub/html/index.html"
            display_text = f"{flag} {lang_name} - Version {version}"
            group += f'        <li>\n'
            group += f'          <a href="{link_path}">\n'
            group += f'            {display_text}\n'
            group += f'          </a>\n'
            group += f'        </li>\n'

        group += f'      </ul>\n'
        group += f'    </div>\n'
        version_groups += group

    html_content = f'''
    <!DOCTYPE html>
    <html lang="zh">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <title>文档导航 - 多语言多版本</title>
      <style>
        body {{
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          background-color: #f4f6f9;
          color: #333;
          margin: 0;
          padding: 40px;
        }}
        .container {{
          max-width: 800px;
          margin: auto;
          background-color: white;
          padding: 30px;
          border-radius: 12px;
          box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
        }}
        h1 {{
          text-align: center;
          color: #2c3e50;
          margin-bottom: 30px;
          font-weight: 600;
        }}
        .version-group {{
          margin-bottom: 30px;
        }}
        .version-title {{
          font-size: 1.5em;
          color: #2980b9;
          border-bottom: 2px solid #3498db;
          padding-bottom: 8px;
          margin-bottom: 15px;
          display: inline-block;
        }}
        .lang-links {{
          list-style: none;
          padding: 0;
        }}
        .lang-links li {{
          margin: 12px 0;
        }}
        .lang-links a {{
          display: block;
          padding: 14px 20px;
          background-color: #ecf0f1;
          color: #2c3e50;
          text-decoration: none;
          border-radius: 8px;
          font-size: 1.1em;
          transition: all 0.3s ease;
          border-left: 4px solid #3498db;
        }}
        .lang-links a:hover {{
          background-color: #3498db;
          color: white;
          transform: translateX(6px);
          border-left-color: #f39c12;
        }}
        footer {{
          text-align: center;
          margin-top: 40px;
          color: #7f8c8d;
          font-size: 0.9em;
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <h1>📄 {lib}项目文档导航</h1>
    
    {version_groups}
        <footer>
          &copy; 2025 {lib}项目文档中心. All rights reserved.
        </footer>
      </div>
    </body>
    </html>
    '''

    return html_content


def _capture_escape_files(x: list[str]) -> list[str]:
    _tmp = [_.split('.') for _ in x]
    _suffix = [_pair_capture.get(_[1]) for _ in _tmp]
    _tmp1 = [v1[0] + '.' + v2 for v1, v2 in zip(_tmp, _suffix)]
    return list(set(x + _tmp1))


class AutomationDoc:

    _root = _get_root_path()
    _images_source = sep.join(_root_path_list + ['docs', 'images'])
    _doxygen_root = sep.join(_root_path_list + ['docs', 'doxygen'])
    _images_doxygen_destination = sep.join(_root_path_list + ['docs', 'doxygen', 'images'])
    _images_sphinx_destination = sep.join(_root_path_list + ['docs', 'sphinx', 'images'])

    def __init__(self):
        self.meta = _inherit_root_metadata()
        self._copy_images_for_doxygen_and_sphinx()
        self.doxygen_automation()

    def doxygen_automation(self):
        self._doxygen_scripts_from_sources_to_langs()
        self._doxygen_scripts_from_langs_to_vers()
        self._doxygen_config_injection()
        self._doxygen_config_execution()
        self._doxygen_export_navigation()
        self._doxygen_build_clean()

    def _copy_images_for_doxygen_and_sphinx(self):
        # # customize prefix syntax here
        # # IN: => doxygen; OUT: => sphinx; ALL: => both

        # clean if exists
        _no_recursive_clean_img(self._images_doxygen_destination)
        _no_recursive_clean_img(self._images_sphinx_destination)

        # copy images to proper sub-doc systems
        for img in os.listdir(self._images_source):
            _f = self._images_source + sep + img
            if img.startswith('IN'):
                shutil.copy2(_f, self._images_doxygen_destination + sep + img)
            elif img.startswith('OUT'):
                shutil.copy2(_f, self._images_sphinx_destination + sep + img)
            else:  # both
                shutil.copy2(_f, self._images_doxygen_destination + sep + img)
                shutil.copy2(_f, self._images_sphinx_destination + sep + img)

    def _doxygen_scripts_from_sources_to_langs(self):

        # remove if exists
        _build_folder = self._doxygen_root + sep + 'build'
        if 'build' in os.listdir(self._doxygen_root):
            for _f in os.listdir(_build_folder):  # clean build folder (save isolated files for sub-git)
                _tmp = _build_folder + sep + _f
                if os.path.isdir(_tmp):
                    shutil.rmtree(_tmp)
        else:  # make folders
            os.mkdir(_build_folder)

        for _lang in self.meta.get('doc_doxygen_languages'):
            _lang_folder = _build_folder + sep + _lang
            os.mkdir(_lang_folder)
            os.mkdir(_lang_folder + sep + f'_{_lang}_docstrings')
            for _ver in self.meta.get('doc_doxygen_versions'):
                os.mkdir(_lang_folder + sep + f'v{_ver}')

        # move filtered docstring files
        _files = _file_collector([self._root + sep + _ for _ in self.meta.get('doc_doxygen_folders')],
                                 self.meta.get('doc_doxygen_suffix'))
        for (k, v) in _files:
            _f = k + sep + v
            with open(_f, 'r', encoding='utf-8') as f:
                _tmp = f.readlines()
            for _lang in self.meta.get('doc_doxygen_languages'):
                _tmp_filtered = _language_filter(_tmp, self.meta.get('doc_doxygen_languages'), _lang)

                with open(_build_folder + sep + _lang + sep + f'_{_lang}_docstrings' + sep + v,
                          'w', encoding='utf-8') as f:
                    f.write(''.join(_tmp_filtered))

    def _doxygen_scripts_from_langs_to_vers(self):

        _build_folder = self._doxygen_root + sep + 'build'
        for _lang in self.meta.get('doc_doxygen_languages'):
            _f_out = _build_folder + sep + _lang
            for _ver in self.meta.get('doc_doxygen_versions'):
                _f_in = _f_out + sep + f'v{_ver}'
                _docstrings = f'_{_lang}_v{_ver}_docstrings'

                if _docstrings in os.listdir(_f_in):  # remove if exists
                    shutil.rmtree(_docstrings)

                _f_final = _f_in + sep + _docstrings
                os.mkdir(_f_final)

                should_be_escape = []
                for file in os.listdir(_r := _f_out + sep + f'_{_lang}_docstrings'):
                    with open(_r + sep + file, 'r', encoding='utf-8') as f:
                        _tmp = f.readlines()

                    _tmp, _file_ver = _ver_filter(_tmp, _ver)
                    if _file_ver:
                        if not _ver_should_include(_file_ver, _ver):
                            should_be_escape.append(file)

                    with open(_f_final + sep + file, 'w', encoding='utf-8') as f:
                        f.write('\n\n\n'.join(_tmp))

                _escape_files = _capture_escape_files(should_be_escape)  # remove unmatched version files
                for file in os.listdir(_r := _f_out + sep + f'_{_lang}_docstrings'):
                    if file in _escape_files:
                        os.remove(_f_final + sep + file)

    def _doxygen_config_injection(self):

        with open(self._root + sep + 'Doxyfile', 'r', encoding='utf-8') as f:
            _meta_config = ''.join(f.readlines())

        _meta_config = _meta_config.replace("%LIB_NAME%", self.meta.get('name'))
        _meta_config = _meta_config.replace("%PATTERNS%",
                                            ' '.join([f'*.{_}' for _ in self.meta.get('doc_doxygen_suffix')]))
        _meta_config = _meta_config.replace("%GRAPHVIZ_BIN%", self.meta.get('graphviz_bin'))

        _build_folder = self._doxygen_root + sep + 'build'
        for _lang in self.meta.get('doc_doxygen_languages'):
            _f_out = _build_folder + sep + _lang
            for _ver in self.meta.get('doc_doxygen_versions'):
                _f_in = _f_out + sep + f'v{_ver}'
                _meta = _meta_config.replace("%LAN%", _lang)
                _meta = _meta.replace("%VER%", _ver)
                _meta = _meta.replace("%FULL_LAN%", language_map.get(_lang))

                with open(_f_in + sep + 'Doxyfile.in', 'w', encoding='utf-8') as f:
                    f.write(_meta)

    def _doxygen_config_execution(self):

        _build_folder = self._doxygen_root + sep + 'build'
        for _lang in self.meta.get('doc_doxygen_languages'):
            _f_out = _build_folder + sep + _lang
            for _ver in self.meta.get('doc_doxygen_versions'):
                _f_in = _f_out + sep + f'v{_ver}'

                result = subprocess.run(
                    ["doxygen", "./Doxyfile.in"],
                    cwd=Path(_f_in),
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    print(f"Documentation of [{_lang}, v{_ver}] successfully generated")
                else:
                    print(f"Documentation of [{_lang}, v{_ver}] in {_f_in} was generated failed")
                    print(result.stderr)

    def _doxygen_export_navigation(self):
        _tmp = _generate_docs_index(self.meta.get('doc_doxygen_languages'), self.meta.get('doc_doxygen_versions'),
                                    self.meta.get('name'))
        with open(self._doxygen_root + sep + 'build' + sep + 'docs.html', 'w', encoding='utf-8') as f:
            f.write(_tmp)

    def _doxygen_build_clean(self):
        _clean_doxygen_build(self._doxygen_root + sep + 'build')

    @staticmethod
    def _call_syntax_suggestion():
        _content = """
        ============================= Syntax Guide =============================
        1. one functional unit(single f.hpp without f.cpp, or a pair of f.hpp
           and f.cpp), share one namespace;
        2. multi-lined /*! ... */ for file-level docstring, @file followed by
           @defgroup command must be include (only once), with format 
           '@defgroup tag alias'; the alias must strictly match the namespace 
           of current functional unit;
        3. no need to include '@{' and '@}' for group domain, the build system
           can automatically process;
        4. three wrap lines to physically separate global object in file;
        5. multi-lined /** ... */ for global object level documenting, @since
           must be included when create;
        6. internalization support is available, use [lang] to note; no [lang]
           component is of global;
        7. images can be stored in ./docs/_images, prefix 'IN_' for doxygen
           system, 'OUT_' for sphinx system, and 'ALL_' for both;
        8. ./include/dox/ for .dox files, syntax use multi-lined /*! ... */
           commands;
        9. ./include/dox/demos/ for demos, *.dox for tutorial files with
           pure /*! ... @example ... */ inside; and *.cxx for example files;
        ============================== Guide Over ==============================
        """
        print(_content)


if __name__ == '__main__':
    A = AutomationDoc()
