import re
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from anchorfix import DuplicateIdError, process_html, process_html_file


class TestProcessHtml:
    """process_html関数のテスト"""

    def test_basic_conversion(self):
        """基本的なアンカー変換"""
        html = '<h2 id="intro">Intro</h2><h3 id="detail">Detail</h3>'
        result = process_html(html, prefix="a")

        soup = BeautifulSoup(result, "html.parser")
        assert soup.find("h2")["id"] == "a0001"
        assert soup.find("h3")["id"] == "a0002"

    def test_internal_links_update(self):
        """内部リンクの更新"""
        html = """
        <h2 id="section1">Section 1</h2>
        <a href="#section1">Go to Section 1</a>
        <h2 id="section2">Section 2</h2>
        <a href="#section2">Go to Section 2</a>
        """
        result = process_html(html, prefix="a")

        soup = BeautifulSoup(result, "html.parser")
        links = soup.find_all("a", href=True)
        assert links[0]["href"] == "#a0001"
        assert links[1]["href"] == "#a0002"

    def test_external_links_preserved(self):
        """外部リンクが保持されることを確認"""
        html = """
        <h2 id="intro">Intro</h2>
        <a href="other.html#section">External page</a>
        <a href="https://example.com#anchor">External site</a>
        <a href="#intro">Internal link</a>
        """
        result = process_html(html, prefix="a")

        soup = BeautifulSoup(result, "html.parser")
        links = soup.find_all("a", href=True)
        assert links[0]["href"] == "other.html#section"  # 外部リンク保持
        assert links[1]["href"] == "https://example.com#anchor"  # 外部リンク保持
        assert links[2]["href"] == "#a0001"  # 内部リンク更新

    def test_url_encoded_anchors(self):
        """URLエンコードされたアンカーの変換(CMSで壊れたリンクのケース)"""
        html = """
        <h2 id="sigstore(%E3%82%B7%E3%82%B0%E3%82%B9%E3%83%88%E3%82%A2)-%E3%81%A8%E3%81%AF">Header</h2>
        <a href="#sigstore%E3%82%B7%E3%82%B0%E3%82%B9%E3%83%88%E3%82%A2-%E3%81%A8%E3%81%AF">Link</a>
        """
        result = process_html(html, prefix="a")

        soup = BeautifulSoup(result, "html.parser")
        # h2のidが変換されていることを確認
        assert soup.find("h2")["id"] == "a0001"
        # リンクが正しく更新されていることを確認(正規化により一致)
        assert soup.find("a", href=True)["href"] == "#a0001"

    def test_custom_prefix(self):
        """カスタムプレフィックスの使用"""
        html = '<h2 id="test">Test</h2>'
        result = process_html(html, prefix="sec")

        soup = BeautifulSoup(result, "html.parser")
        assert soup.find("h2")["id"] == "sec0001"

    def test_sequential_numbering(self):
        """連番の正確性"""
        html = """
        <h1 id="h1">H1</h1>
        <h2 id="h2">H2</h2>
        <h3 id="h3">H3</h3>
        <h4 id="h4">H4</h4>
        <h5 id="h5">H5</h5>
        <h6 id="h6">H6</h6>
        """
        result = process_html(html, prefix="a")

        soup = BeautifulSoup(result, "html.parser")
        assert soup.find("h1")["id"] == "a0001"
        assert soup.find("h2")["id"] == "a0002"
        assert soup.find("h3")["id"] == "a0003"
        assert soup.find("h4")["id"] == "a0004"
        assert soup.find("h5")["id"] == "a0005"
        assert soup.find("h6")["id"] == "a0006"

    def test_anchor_name_attribute(self):
        """aタグのname属性の処理"""
        html = '<a name="old-anchor">Anchor</a>'
        result = process_html(html, prefix="a")

        soup = BeautifulSoup(result, "html.parser")
        assert soup.find("a")["name"] == "a0001"

    def test_duplicate_id_detection(self):
        """重複IDの検出"""
        html = """
        <h2 id="duplicate">First</h2>
        <h2 id="duplicate">Second</h2>
        """
        with pytest.raises(DuplicateIdError) as exc_info:
            process_html(html, prefix="a")

        assert "duplicate" in str(exc_info.value)
        assert exc_info.value.id_value == "duplicate"

    def test_incomplete_html(self):
        """不完全なHTML（bodyタグなし）の処理"""
        html = '<h2 id="test">Test</h2><p>Content</p>'
        result = process_html(html, prefix="a")

        soup = BeautifulSoup(result, "html.parser")
        assert soup.find("h2")["id"] == "a0001"

    def test_empty_html(self):
        """空のHTMLの処理"""
        html = ""
        result = process_html(html, prefix="a")
        assert result == ""

    def test_no_anchors(self):
        """アンカーがないHTMLの処理"""
        html = "<p>No anchors here</p>"
        result = process_html(html, prefix="a")
        assert "<p>No anchors here</p>" in result

    def test_anchor_id_format(self):
        """生成されるアンカーIDの形式確認"""
        html = '<h2 id="test">Test</h2>'
        result = process_html(html, prefix="xyz")

        soup = BeautifulSoup(result, "html.parser")
        anchor_id = soup.find("h2")["id"]
        # prefix + 4桁の数字
        assert re.match(r"^xyz\d{4}$", anchor_id)

    def test_overwrite_existing_anchors(self):
        """既存のアンカーIDの上書き"""
        html = """
        <h2 id="old-id-1">Header 1</h2>
        <h2 id="old-id-2">Header 2</h2>
        """
        result = process_html(html, prefix="a")

        soup = BeautifulSoup(result, "html.parser")
        headers = soup.find_all("h2")
        assert headers[0]["id"] == "a0001"
        assert headers[1]["id"] == "a0002"
        # 古いIDが残っていないことを確認
        assert "old-id-1" not in result
        assert "old-id-2" not in result


class TestProcessHtmlFile:
    """process_html_file関数のテスト"""

    def test_basic_file_processing(self, tmp_path):
        """基本的なファイル処理"""
        input_file = tmp_path / "input.html"
        input_file.write_text(
            '<h2 id="test">Test</h2><a href="#test">Link</a>',
            encoding="utf-8",
        )

        result = process_html_file(input_file, prefix="a")

        soup = BeautifulSoup(result, "html.parser")
        assert soup.find("h2")["id"] == "a0001"
        assert soup.find("a")["href"] == "#a0001"

    def test_file_not_found(self):
        """存在しないファイルの処理"""
        with pytest.raises(FileNotFoundError):
            process_html_file("nonexistent.html")

    def test_utf8_encoding(self, tmp_path):
        """UTF-8エンコーディングのファイル処理"""
        input_file = tmp_path / "utf8.html"
        input_file.write_text(
            '<h2 id="テスト">日本語</h2>',
            encoding="utf-8",
        )

        result = process_html_file(input_file, prefix="a")

        soup = BeautifulSoup(result, "html.parser")
        assert soup.find("h2")["id"] == "a0001"
        assert "日本語" in result


class TestExampleFiles:
    """examplesディレクトリのファイルを使ったテスト"""

    def test_basic_example(self):
        """基本的な変換例のテスト"""
        input_path = (
            Path(__file__).parent.parent.parent / "examples" / "basic_input.html"
        )

        if not input_path.exists():
            pytest.skip("Example files not found")

        result = process_html_file(input_path, prefix="a")

        # BeautifulSoupで結果を解析
        result_soup = BeautifulSoup(result, "html.parser")

        # h1, h2, h3のIDを確認
        assert result_soup.find("h1")["id"] == "a0001"
        assert result_soup.find("h2")["id"] == "a0002"
        assert result_soup.find("h3")["id"] == "a0003"

    def test_incomplete_example(self):
        """不完全なHTMLの例のテスト"""
        input_path = (
            Path(__file__).parent.parent.parent / "examples" / "incomplete_input.html"
        )

        if not input_path.exists():
            pytest.skip("Example files not found")

        result = process_html_file(input_path, prefix="a")

        result_soup = BeautifulSoup(result, "html.parser")
        headers = result_soup.find_all("h2")
        assert headers[0]["id"] == "a0001"
        assert headers[1]["id"] == "a0002"

    def test_mixed_links_example(self):
        """外部リンク混在の例のテスト"""
        input_path = (
            Path(__file__).parent.parent.parent / "examples" / "mixed_links_input.html"
        )

        if not input_path.exists():
            pytest.skip("Example files not found")

        result = process_html_file(input_path, prefix="a")

        soup = BeautifulSoup(result, "html.parser")
        links = soup.find_all("a", href=True)

        # 内部リンクが更新されている
        internal_links = [link for link in links if link["href"].startswith("#")]
        assert all(link["href"].startswith("#a") for link in internal_links)

        # 外部リンクが保持されている
        external_links = [link for link in links if not link["href"].startswith("#")]
        assert any("other.html" in link["href"] for link in external_links)
        assert any("example.com" in link["href"] for link in external_links)

    def test_duplicate_id_example(self):
        """重複IDエラーケースのテスト"""
        input_path = (
            Path(__file__).parent.parent.parent / "examples" / "duplicate_id_input.html"
        )

        if not input_path.exists():
            pytest.skip("Example files not found")

        with pytest.raises(DuplicateIdError) as exc_info:
            process_html_file(input_path, prefix="a")

        assert "duplicate" in str(exc_info.value)
