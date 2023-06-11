import shutil
from pathlib import Path

import toml

assert Path.cwd() == Path(__file__).parent.parent


class UnsupportedPath(Exception):
    """
    Raised when a path is neither a file nor a directory,
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
            if to.exists():
                if not to.is_file() and not to.is_dir():
                    raise UnsupportedPath(
                        f'{to} is neither a file nor a directory, '
                        f'nor a symbolic link pointing to them.'
                    )
                backup = Path('_backup') / category / config['name']
                backup.parent.mkdir(parents=True, exist_ok=True)
                if backup.is_file():
                    backup.unlink()
                elif backup.is_dir():
                    shutil.rmtree(backup)
                to.rename(backup)
            to.symlink_to(from_.resolve())


if __name__ == '__main__':
    main()
