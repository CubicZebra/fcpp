conan create . -pr:b=default -pr:h=default -s build_type=Debug --build=missing
python .\docs\build.py
Remove-Item -Path .\test_package\build -Recurse -Force
Remove-Item -Path .\test_package\CMakeUserPresets.json
conan remove "fcpp/*" --confirm