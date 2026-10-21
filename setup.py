import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tunning.
build_exe_options = {"packages": ["os"], "includes": ["tkinter", "math", "matplotlib", "ttkbootstrap"]}

# GUI applications require a different base on Windows (the default is for
# a console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Tcc_Victor_Failton",
    version="0.1",
    description="Tcc!",
    options={"build_exe": build_exe_options},
    executables=[Executable("Tcc.py", base=base)]
)


