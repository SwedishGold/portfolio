"""Offline checks for the public portfolio, not for the products it describes."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import copy
import importlib.util
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('portfolio_build', ROOT / 'tools' / 'build.py')
BUILD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILD)


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = []
        self.links = []
        self.resources = []
        self.scripts = 0
        self.details = 0
        self.langs = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a' and 'href' in attrs:
            self.links.append(attrs['href'])
        if tag in {'img', 'script', 'iframe', 'video', 'audio', 'source', 'link'}:
            self.resources.append(attrs.get('src', attrs.get('href', '')))
        self.scripts += tag == 'script'
        self.details += tag == 'details'
        if 'lang' in attrs:
            self.langs.append(attrs['lang'])


class PortfolioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = json.loads((ROOT / 'cases.json').read_text(encoding='utf-8'))
        cls.html = (ROOT / 'index.html').read_text(encoding='utf-8')
        cls.page = Page(cls.html)

    def test_all_six_retained_cases_present(self):
        self.assertEqual({c['id'] for c in self.cases}, {
            'hope', 'museum', 'mellumo', 'codex-weekly',
            'dust-lord', 'hermes-wrist'})
        self.assertEqual(len(self.cases), 6)

    def test_retired_case_is_absent_from_current_publication(self):
        expected = {c['id'] + '.md' for c in self.cases}
        self.assertEqual({p.name for p in (ROOT / 'cases').glob('*.md')}, expected)
        for path in [ROOT / 'cases.json', ROOT / 'index.html', ROOT / 'README.md']:
            self.assertNotIn('strawberrai', path.read_text(encoding='utf-8').lower())

    def test_recruiter_entry_points_are_prioritized(self):
        self.assertEqual([c['id'] for c in self.cases[:2]], ['hope', 'dust-lord'])
        self.assertIn('lokala AI-lösningar', self.html)
        self.assertIn('kunskapsbanker', self.html)

    def test_external_targets_match_current_curated_work(self):
        actual = {link for link in self.page.links if urlsplit(link).scheme}
        self.assertEqual(actual, {
            'https://github.com/SwedishGold/portfolio',
            'https://github.com/SwedishGold/dustlord',
            'https://www.linkedin.com/in/andreas-hillborgh-51581371/'})

    def test_unique_cases_and_html_ids(self):
        self.assertEqual(len({c['id'] for c in self.cases}), len(self.cases))
        self.assertEqual(len(set(self.page.ids)), len(self.page.ids))
        self.assertEqual(self.page.details, len(self.cases))

    def test_each_case_has_role_evidence_limitations_and_english(self):
        for c in self.cases:
            with self.subTest(case=c['id']):
                for key in ['role', 'evidence', 'limits', 'english', 'approach', 'problem']:
                    self.assertGreater(len(c[key]), 40, key)
                self.assertEqual(len(c['flow']), 4)
                self.assertGreater(len(c['tech']), 0)

    def test_no_automatic_remote_resources_or_script(self):
        self.assertEqual(self.page.resources, [])
        self.assertEqual(self.page.scripts, 0)
        self.assertNotRegex(self.html, r'(?i)@import|url\s*\(')

    def test_html_links_and_fragments_resolve(self):
        for link in self.page.links:
            parts = urlsplit(link)
            if parts.scheme or parts.netloc:
                self.assertEqual(parts.scheme, 'https')
                continue
            path = (ROOT / unquote(parts.path)).resolve() if parts.path else ROOT / 'index.html'
            self.assertTrue(path.is_relative_to(ROOT), link)
            self.assertTrue(path.is_file(), link)
            if parts.fragment and path == ROOT / 'index.html':
                self.assertIn(parts.fragment, self.page.ids)

    def test_markdown_local_links_resolve(self):
        paths = [ROOT / 'README.md', *sorted((ROOT / 'cases').glob('*.md'))]
        for path in paths:
            text = path.read_text(encoding='utf-8')
            for link in re.findall(r'\]\(([^)]+)\)', text):
                parts = urlsplit(link)
                if parts.scheme or parts.netloc or not parts.path:
                    continue
                target = (path.parent / unquote(parts.path)).resolve()
                self.assertTrue(target.is_relative_to(ROOT), link)
                self.assertTrue(target.is_file(), f'{path.name}: {link}')

    def test_generated_outputs_match_sources(self):
        for relative, text in BUILD.build_outputs(self.cases).items():
            self.assertEqual((ROOT / relative).read_text(encoding='utf-8'), text, relative)

    def test_text_is_escaped_not_rendered_as_markup(self):
        cases = copy.deepcopy(self.cases)
        cases[0]['summary'] = '<script>alert("not executable")</script>'
        html = BUILD.build_outputs(cases)['index.html']
        self.assertIn('&lt;script&gt;', html)
        self.assertEqual(Page(html).scripts, 0)

    def test_public_copy_has_no_local_paths_or_private_network(self):
        text = json.dumps(self.cases, ensure_ascii=False)
        self.assertNotRegex(text, r'/Users/|/home/|192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+')
        self.assertIn('sv', self.page.langs)
        self.assertIn('en', self.page.langs)


if __name__ == '__main__':
    unittest.main()
