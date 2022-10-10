from typing import Dict

import pathlib
import tempfile

from absl.testing import absltest
from absl.testing import parameterized

import generate_links
import goto_pb2


class GenerateLinksTest(parameterized.TestCase):
  """Unit tests for generate_links."""

  def test_generate_files(self):
    """Ensures specified files are generated with proper content."""
    with tempfile.TemporaryDirectory() as output_path:
      output_directory = pathlib.Path(output_path)
      link_by_path = {
          pathlib.Path(output_directory / 'link_0/index.html'): 'url',
          pathlib.Path(output_directory / 'link_0/link_0/index.html'): 'url_0',
          pathlib.Path(output_directory / 'link_0/link_1/index.html'): 'url_1',
          pathlib.Path(output_directory / 'link_a/link_a/index.html'): 'url_a',
          pathlib.Path(output_directory / 'link_a/link_b/index.html'): 'url_b',
      }
      generate_links.generate_files(link_by_path)
      for path, link in link_by_path.items():
        self.assertTrue(path.exists())
        with open(path) as stream:
          self.assertIn(link, stream.read())

  @parameterized.named_parameters(
      ('with_default_url',
       goto_pb2.Config(
           default_url='default_url',
           links=goto_pb2.LinkGroup(
               url='url_top',
               links_by_group={
                   'link_0':
                       goto_pb2.LinkGroup(
                           url='url',
                           links_by_group={
                               'link_0': goto_pb2.LinkGroup(url='url_0'),
                               'link_1': goto_pb2.LinkGroup(url='url_1'),
                           }),
                   'link_a':
                       goto_pb2.LinkGroup(
                           links_by_group={
                               'link_a': goto_pb2.LinkGroup(url='url_a'),
                               'link_b': goto_pb2.LinkGroup(url='url_b'),
                           }),
               })), {
                   pathlib.Path('/index.html'): 'url_top',
                   pathlib.Path('/link_0/index.html'): 'url',
                   pathlib.Path('/link_0/link_0/index.html'): 'url_0',
                   pathlib.Path('/link_0/link_1/index.html'): 'url_1',
                   pathlib.Path('/link_a/index.html'): 'default_url',
                   pathlib.Path('/link_a/link_a/index.html'): 'url_a',
                   pathlib.Path('/link_a/link_b/index.html'): 'url_b',
               }),
      ('without_default_url',
       goto_pb2.Config(
           links=goto_pb2.LinkGroup(
               url='url_top',
               links_by_group={
                   'link_0':
                       goto_pb2.LinkGroup(
                           url='url',
                           links_by_group={
                               'link_0': goto_pb2.LinkGroup(url='url_0'),
                               'link_1': goto_pb2.LinkGroup(url='url_1'),
                           }),
                   'link_a':
                       goto_pb2.LinkGroup(
                           links_by_group={
                               'link_a': goto_pb2.LinkGroup(url='url_a'),
                               'link_b': goto_pb2.LinkGroup(url='url_b'),
                           }),
               })), {
                   pathlib.Path('/index.html'): 'url_top',
                   pathlib.Path('/link_0/index.html'): 'url',
                   pathlib.Path('/link_0/index.html'): 'url',
                   pathlib.Path('/link_0/link_0/index.html'): 'url_0',
                   pathlib.Path('/link_0/link_1/index.html'): 'url_1',
                   pathlib.Path('/link_a/link_a/index.html'): 'url_a',
                   pathlib.Path('/link_a/link_b/index.html'): 'url_b',
               }),
  )
  def test_process_config(self, config: goto_pb2.Config,
                          expected_link_by_path: Dict[pathlib.Path, str]):
    """Ensures all configs are processed into link_by_path."""
    self.assertEqual(
        generate_links.GotoProcessor(config, pathlib.Path('/')).process(),
        expected_link_by_path)


if __name__ == '__main__':
  absltest.main()
