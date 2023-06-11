import shutil
from pathlib import Path

import toml

assert Path.cwd() == Path(__file__).parent.parent


class UnsupportedPath(Exception):
    """
    Raised when a path is neither a directory nor a file,
    nor a symbolic link pointing to them.
    """


def main() -> None:

    index: dict[str, list[dict[str, str]]] = toml.load('index.toml')

    for category, configs in index.items():

        cat_dir = Path('src') / category
        if not cat_dir.is_dir():
            continue

        for config in configs:

            from_ = cat_dir / config['name']
            if not from_.exists():
                continue

            to = Path(config['to']).expanduser()
            to.parent.mkdir(parents=True, exist_ok=True)

            # `to.is_symlink()` is for the symlink that points to
            # a non-existing directory or file
            if to.is_dir() or to.is_file() or to.is_symlink():
                backup = Path('backup') / category / config['name']
                backup.parent.mkdir(parents=True, exist_ok=True)
                if backup.is_dir():
                    shutil.rmtree(backup)
                elif backup.exists():
                    backup.unlink()
                to.rename(backup)
            elif to.exists():
                raise UnsupportedPath(
                    f'{to} is neither a directory nor a file, '
                    f'nor a symbolic link pointing to them.'
                )

            to.symlink_to(from_.resolve())


if __name__ == '__main__':
    main()
