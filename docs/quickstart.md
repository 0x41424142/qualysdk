# Getting Started

There are a few ways to get started with ```qualysdk```:

## Installing From PyPI

For the latest (hopefully stable) version, you can install from PyPI:

```bash
pip install qualysdk
```

### Upgrading the SDK

There are two ways to upgrade the SDK from PyPI:

#### Using Pip

```bash
pip install --upgrade qualysdk
```

#### Using qualysdk-updater

```qualysdk-updater``` is a CLI tool that is installed alongside the SDK. It can be used to check for updates and install them.

```bash
usage: qualysdk-updater [-h] [-v] [-c] [-i] [-y]

Check for and install updates for qualysdk

options:
  -h, --help     show this help message and exit
  -v, --version  Display the current version of qualysdk
  -c, --check    Check if a new version of qualysdk is available
  -i, --install  Install the latest version of qualysdk
  -y, --yes      Bypass the confirmation prompt when installing
```

To bypass the confirmation prompt when installing, use the `-y` flag.

```bash
qualysdk-updater -i -y
```

## Installing From GitHub (Bleeding Edge)

If you want the latest and greatest, you can install from GitHub:

### Installing with Poetry

```bash
git clone https://github.com/0x41424142/qualysdk.git
cd qualysdk
poetry shell #if you want to use a venv
poetry install
```

### Installing with Pip

```bash
git clone https://github.com/0x41424142/qualysdk.git
cd qualysdk
pip install .
```
