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

(TODO)

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
