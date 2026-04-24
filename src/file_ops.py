# Proxy that explicitly loads 'os' and 'shutil' from the Python stdlib and re-exports
# a small set of filesystem utilities used across the project.
import importlib
import importlib.util
import sysconfig
from pathlib import Path as _Path


def _load_stdlib(name):
    stdlib_path = _Path(sysconfig.get_paths()['stdlib'])
    module_file = stdlib_path / (name + '.py')
    package_init = stdlib_path / name / '__init__.py'
    if package_init.exists():
        spec = importlib.util.spec_from_file_location(f"_stdlib_{name}", str(package_init))
    elif module_file.exists():
        spec = importlib.util.spec_from_file_location(f"_stdlib_{name}", str(module_file))
    else:
        return importlib.import_module(name)

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

_os = _load_stdlib('os')
_shutil = _load_stdlib('shutil')

# Re-export commonly used functions
makedirs = _os.makedirs
listdir = _os.listdir
exists = _os.path.exists
isfile = _os.path.isfile
join = _os.path.join
abspath = _os.path.abspath
basename = _os.path.basename

# shutil operations
copy2 = _shutil.copy2
move = _shutil.move

# Expose path module for callers who prefer to use it
path = _os.path

__all__ = [
    'makedirs', 'listdir', 'exists', 'isfile', 'join', 'abspath', 'basename',
    'copy2', 'move', 'path'
]
