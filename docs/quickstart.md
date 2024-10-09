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

# Example output:
🟧 An update is available!
📅 Latest Version: vX.X.X
📅 Release Date: 2024-10-09T12:00:00
✅ MD5: e15ebb2b077d07eb9a646a5425aafef4
✅ BLAKE2b_256: a6a21a9c9cb35fc8c8cad440b1e5873f82894b093dd5d0d2c532704b5e0b0ba6
✅ SHA256: d069561f1f82537e858de32375c239c12cad4bb68ca996f9902f92d48aae490e
🐈 GitHub Release Notes: https://github.com/0x41424142/qualysdk/releases/tag/vX.X.X
🐍 PyPI Page: https://pypi.org/project/qualysdk/X.X.X/ 
⬆️  Installing vX.X.X...
...
✅ qualysdk has been updated to vX.X.X

# Confirm with the version flag or check flag:
qualysdk-updater -v
>>>Qualysdk version currently installed: vX.X.X

qualysdk-updater -c
>>>✅ qualysdk is up to date (vX.X.X)
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
