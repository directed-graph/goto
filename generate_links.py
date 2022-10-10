from typing import Dict

import pathlib

from absl import app
from absl import flags
from absl import logging
from google.protobuf import text_format

import goto_pb2

_CONFIG_FILE = flags.DEFINE_string('config_file', None,
                                   'Textproto containing a goto.Config proto.')

_OUTPUT_DIRECTORY = flags.DEFINE_string(
    'output_directory', 'output', 'Directory to write generated files to.')

_HTML_TEMPLATE = '''<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="refresh" content="0; url='{url}'" />
  </head>
  <body>
    <!-- In case redirect does not work. -->
    <p><a href="{url}">Click</a> to redirect.</p>
  </body>
</html>
'''


def generate_files(link_by_path: Dict[pathlib.Path, str]) -> None:
  """Generates the files for the links given path."""
  for path, link in link_by_path.items():
    logging.info('Generating at: %s -> %s', path, link)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as stream:
      stream.write(_HTML_TEMPLATE.format(url=link))


class GotoProcessor:
  """Processes the given Goto Config into a path to URL mapping."""

  def __init__(self, config: goto_pb2.Config, output_directory: pathlib.Path):
    """Initializes the processor with the Config and path starting point."""
    self.config = config
    self.output_directory = output_directory
    self.link_by_path = {}

  def _process_link_group(self, link_group: goto_pb2.LinkGroup,
                          current_directory: pathlib.Path) -> None:
    """Processes each LinkGroup recursively."""
    logging.info('Processing at: %s', current_directory)

    if link_group.url:
      self.link_by_path[current_directory / 'index.html'] = link_group.url

    for child_link_group_name, child_link_group in link_group.links_by_group.items(
    ):
      self._process_link_group(child_link_group,
                               current_directory / child_link_group_name)

  def process(self) -> Dict[pathlib.Path, str]:
    """Processes the given Config and returns a mapping of path to URL."""
    if not self.link_by_path:
      self._process_link_group(self.config.links, self.output_directory)
    return self.link_by_path


def main(argv) -> None:
  del argv  # Unused

  if not _CONFIG_FILE.value:
    raise ValueError('Must provide a config file.')

  config = goto_pb2.Config()
  with open(_CONFIG_FILE.value) as stream:
    text_format.Parse(stream.read(), config)

  logging.info('Processing goto.Config:\n%s', str(config))
  generate_files(
      GotoProcessor(config, pathlib.Path(_OUTPUT_DIRECTORY.value)).process())


if __name__ == '__main__':
  app.run(main)
