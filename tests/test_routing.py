import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RoutingTests(unittest.TestCase):
    def test_entrypoints_prefer_mcp(self):
        paths = [ROOT / 'README.md', ROOT / 'AGENTS.md', ROOT / 'docs/agent-entry.md', ROOT / 'protocols/UE5.4.md']
        paths += list((ROOT / 'harness-prompts').glob('*.md'))
        for path in paths:
            with self.subTest(path=path.name):
                text = path.read_text(encoding='utf-8')
                self.assertIn('EngineWire MCP', text)
                self.assertIn('Remote Execution', text)
                self.assertNotIn('install_bridge', text)
                self.assertNotIn('toolbar-button-ue5.4.md', text)

    def test_no_button_distribution(self):
        for name in ['templates/ue5.4', 'scripts/windows/install_bridge.ps1', 'scripts/mac/install_bridge.sh', 'docs/toolbar-button-ue5.4.md']:
            self.assertFalse((ROOT / name).exists(), name)

    def test_local_markdown_links_resolve(self):
        for path in ROOT.rglob('*.md'):
            if '.git' in path.parts:
                continue
            for target in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
                if '://' in target or target.startswith('#'):
                    continue
                self.assertTrue((path.parent / target.split('#')[0]).exists(), f'{path}: {target}')

    def test_compile_helpers_keep_actual_target(self):
        for name in ['scripts/windows/compile_editor_win64.bat', 'scripts/mac/compile_editor_arm64.sh']:
            self.assertIn('EDITOR_TARGET', (ROOT / name).read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
