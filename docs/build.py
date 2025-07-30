from typing import TypeVar
languages = ['en', 'zh']
versions = ['1.0', '2.0']
Language = TypeVar('Language')
Version = TypeVar('Version')



def _single_doxygen_generator(language: Language, version: Version):
    # inject parameter into doxygen file
    ...


def _doxygen_automation_builder(_languages: list[Language], _versions: list[Version]):
    for _lan in _languages:
        ... # create folder if not exists
        for _ver in _versions:
            ... # also, create folder if not exists
            print(f'-- message: now generating v{_ver} in {_lan}...')
            _single_doxygen_generator(_lan, _ver)


if __name__ == '__main__':
    _doxygen_automation_builder(languages, versions)
