# anchorfix

[![PyPI - Version](https://img.shields.io/pypi/v/anchorfix.svg)](https://pypi.org/project/anchorfix)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/anchorfix.svg)
![Last Commit](https://img.shields.io/github/last-commit/heiwa4126/anchorfix)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

HTML アンカーを連番 ID に変換し、内部リンクを自動更新するツール

## インストール

uv を使用する場合:

```bash
uv add anchorfix
```

pip を使用する場合:

```bash
pip install anchorfix
```

## 使用方法

```bash
anchorfix <htmlfile> [--prefix PREFIX]
```

### 基本的な使用例

デフォルトのプレフィックス 'a' を使用:

```bash
anchorfix input.html
```

カスタムプレフィックスを指定:

```bash
anchorfix input.html --prefix sec
```

出力をファイルにリダイレクト:

```bash
anchorfix input.html > output.html
```

### コマンドラインオプション

ヘルプ表示:

```bash
anchorfix --help
```

出力例:

```
usage: anchorfix [-h] [--prefix PREFIX] [--version] htmlfile

HTMLアンカーを連番IDに変換

positional arguments:
  htmlfile         入力HTMLファイルパス

options:
  -h, --help       show this help message and exit
  --prefix PREFIX  アンカーIDのプレフィックス (デフォルト: a)
  -V, --version    バージョン情報を表示
```

バージョン表示:

```bash
anchorfix --version
```

または:

```bash
anchorfix -V
```

## 仕様

### 目的

HTML で編集できる CMS において、ヘッダテキストに基づいたアンカー ID は内部リンクが正しく動作しないことがあります。anchorfix は、これらのアンカーを `#a0001` のような連番形式に変換することで、内部リンクを確実に機能させます。

要は Markdown を HTML に変換した後に使うフィルターです。

### 入出力

- **入力**: 単一の HTML ファイルパス(コマンドライン引数)
- **出力**: 変換された HTML を標準出力(stdout)に出力

### 処理対象

以下の HTML 要素を処理します:

- `<h1>` - `<h6>` タグの `id` 属性
- `<a>` タグの `name` 属性

### 変換ルール

1. **連番形式**: `{prefix}0001`, `{prefix}0002`, ... (4 桁の連番、0001 から開始)
2. **既存アンカーの上書き**: 既存の`id`/`name`属性値は全て上書き
3. **内部リンク更新**: 同一ファイル内の`<a href="#...">`を自動更新
4. **外部リンク保持**: `<a href="other.html#anchor">`のような外部参照は変更しない

### CMS 互換性 - アンカー正規化

CMS が生成する HTML では、`href`属性と`id`属性のアンカーテキストに不一致が生じることがあります。anchorfix は、内部リンクのマッチングを行う際に以下の正規化処理を適用します:

1. **URL デコード**: `%XX`形式のパーセントエンコーディングをデコード
2. **特殊文字の除去**: 以下の文字を削除
   - 括弧: `()（）`
   - コロン: `:`
   - 引用符: `""\'\''`(ASCII/Unicode の両方)
   - スラッシュ: `/`
   - 疑問符: `?`
3. **空白の正規化**: 連続する空白文字を 1 つの半角スペースにまとめる

**例:**

```html
<!-- 変換前: hrefとidの不一致 -->
<a href="#sigstore">Sigstore(シグストア) とは何か</a>
<h2 id="sigstore%28%E3%82%B7%E3%82%B0%E3%82%B9%E3%83%88%E3%82%A2%29-%E3%81%A8%E3%81%AF%E4%BD%95%E3%81%8B">
  <!-- 変換後: 両方とも同じアンカーIDに -->
  <a href="#a0001">Sigstore(シグストア) とは何か</a>
  <h2 id="a0001"></h2>
</h2>
```

この正規化により、以下のような一般的な CMS の不一致パターンに対応できます:

- `補足-` vs `補足:-` (コロンの有無)
- `cosign` vs `"cosign"` (引用符の有無)
- `pypitestpypi` vs `pypi/testpypi` (スラッシュの有無)
- `なぜ` vs `なぜ?` (疑問符の有無)

### エラー処理

- **ファイル読み込みエラー**: 例外をスロー
- **重複 ID 検出**: 同じ`id`値が複数存在する場合、行番号と具体的な ID 値を含む例外をスロー
- **不完全な HTML**: `<body>`の中身のみのような不完全な HTML も許容

### サンプル

詳細なサンプルは `examples/` ディレクトリを参照してください:

- `examples/basic_input.html` / `examples/basic_expected.html` - 基本的な変換例
- `examples/incomplete_input.html` / `examples/incomplete_expected.html` - 不完全な HTML
- `examples/mixed_links_input.html` / `examples/mixed_links_expected.html` - 外部リンク混在
- `examples/duplicate_id_input.html` - 重複 ID エラーケース

## 技術仕様

- **HTML パーサー**: BeautifulSoup4
- **CLI ライブラリ**: argparse (標準ライブラリ)
- **入力エンコーディング**: UTF-8 を想定し自動判定
- **出力エンコーディング**: UTF-8 固定
- **HTML フォーマット**: 元のインデント・改行は保持しない

## 開発者向け

### セットアップ

```bash
uv sync
```

### タスク実行

```bash
# テスト実行
# テストは `examples/` ディレクトリのサンプルファイルを直接参照します
poe test

# リント・型チェック
poe check
poe mypy

# フォーマット
poe format

# 全チェック実行&ビルド&スモークテスト
poe build
```

### Property-Based Testing

このプロジェクトでは、Hypothesis を使用した基本的な Property-Based Testing(PBT)を採用しています。

#### テスト対象プロパティ

1. **一意性**: 生成されたアンカー ID はすべて一意
2. **形式正確性**: すべてのアンカー ID が`{prefix}\d{4}`形式に一致
3. **内部リンク整合性**: `<a href="#...">`が変換後のアンカー ID と正しく対応

#### Hypothesis コード例

```python
from hypothesis import given, strategies as st
from anchorfix import process_html

@given(st.text(min_size=1, max_size=10))
def test_anchor_uniqueness(prefix):
    """生成されたアンカーIDが一意であることを検証"""
    html = "<h2 id='a'>A</h2><h2 id='b'>B</h2>"
    result = process_html(html, prefix=prefix)
    # アンカーIDを抽出して一意性を確認
    # ...

@given(st.text(min_size=1, max_size=10))
def test_anchor_format(prefix):
    """アンカーIDが正しい形式であることを検証"""
    html = "<h2 id='test'>Test</h2>"
    result = process_html(html, prefix=prefix)
    # 正規表現で形式を確認: {prefix}\d{4}
    # ...
```

## ライセンス

MIT
