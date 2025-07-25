conan create . -pr:b=default -pr:h=default -s build_type=Debug -s compiler.cppstd=20 --build=missing
doxygen Doxyfile
Remove-Item -Path .\test_package\build -Recurse -Force
Remove-Item -Path .\test_package\CMakeUserPresets.json
conan remove "fcpp/*" --confirm