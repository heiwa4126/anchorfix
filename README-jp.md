# whoruv

[![PyPI - Version](https://img.shields.io/pypi/v/whoruv.svg)](https://pypi.org/project/whoruv)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/whoruv.svg)
![Last Commit](https://img.shields.io/github/last-commit/heiwa4126/whoruv)
[![PyPI - License](https://img.shields.io/pypi/l/whoruv.svg)](https://opensource.org/licenses/MIT)

## 概要

[Astral の uv](https://docs.astral.sh/uv/) で、
`uvx` や
`uv tool install` でインストール&実行されたときの、

- Python のバージョンと、
- Python の実行ファイルのパスと、
- スクリプト自身のパス

を表示するパッケージ。

uv の
`--python`
オプションの効果などを知るために作成した。

## 実行例

```console
$ uvx whoruv

Installed 1 package in 3ms
Python Version: 3.12.12 (main, Oct 28 2025, 12:10:49) [Clang 20.1.4 ]
Executable Path: /home/user1/.cache/uv/archive-v0/VEm-1_LGBHubU7SZHYbs2/bin/python
Script Path: /home/user1/.cache/uv/archive-v0/VEm-1_LGBHubU7SZHYbs2/lib/python3.12/site-packages/whoruv/whoruv.py

$ uvx --python 3.10 whoruv

Installed 1 package in 3ms
Python Version: 3.10.12 (main, Aug 15 2025, 14:32:43) [GCC 11.4.0]
Executable Path: /home/user1/.cache/uv/archive-v0/Vcsgj4kD85VznE7HmFNsb/bin/python
Script Path: /home/user1/.cache/uv/archive-v0/Vcsgj4kD85VznE7HmFNsb/lib/python3.10/site-packages/whoruv/whoruv.py

$ uv tool install whoruv && whoruv

Resolved 1 package in 1ms
Installed 1 package in 3ms
 + whoruv==0.0.1
Installed 1 executable: whoruv
Python Version: 3.12.12 (main, Oct 28 2025, 12:10:49) [Clang 20.1.4 ]
Executable Path: /home/user1/.local/share/uv/tools/whoruv/bin/python
Script Path: /home/user1/.local/share/uv/tools/whoruv/lib/python3.12/site-packages/whoruv/whoruv.py

$ uv tool install --python 3.10 whoruv && whoruv

Ignoring existing environment for `whoruv`: the requested Python interpreter does not match the environment interpreter
Resolved 1 package in 1ms
Installed 1 package in 4ms
 + whoruv==0.0.1
Installed 1 executable: whoruv
Python Version: 3.10.12 (main, Aug 15 2025, 14:32:43) [GCC 11.4.0]
Executable Path: /home/user1/.local/share/uv/tools/whoruv/bin/python
Script Path: /home/user1/.local/share/uv/tools/whoruv/lib/python3.10/site-packages/whoruv/whoruv.py
```

## 開発

### セットアップ

```bash
uv sync
```

### タスク実行

```bash
# テスト実行
poe test

# リント・フォーマット
poe check
poe format

# 型チェック
poe mypy

# 全チェック実行
poe before
```

### 開発要件

- Python >= 3.12
- uv

## ライセンス

MIT
