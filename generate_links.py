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


def process_link_group(link_group: goto_pb2.LinkGroup,
                       current_directory: pathlib.Path,
                       link_by_path: Dict[pathlib.Path, str]) -> None:
  """Processes each LinkGroup recursively.

  Args:
    link_group: The LinkGroup to be processed recursively.
    current_directory: The current directory of the links.
    link_by_path: Output parameter mapping path to link.
  """
  logging.info('Processing at: %s', current_directory)

  if link_group.url:
    link_by_path[current_directory / 'index.html'] = link_group.url

  for child_link_group_name, child_link_group in link_group.links_by_group.items(
  ):
    process_link_group(child_link_group,
                       current_directory / child_link_group_name, link_by_path)


def process_config(config: goto_pb2.Config,
                   current_directory: pathlib.Path) -> Dict[pathlib.Path, str]:
  """Processes each LinkGroup in the top level."""
  link_by_path = {}

  process_link_group(config.links, current_directory, link_by_path)

  return link_by_path


def main(argv) -> None:
  del argv  # Unused

  if not _CONFIG_FILE.value:
    raise ValueError('Must provide a config file.')

  config = goto_pb2.Config()
  with open(_CONFIG_FILE.value) as stream:
    text_format.Parse(stream.read(), config)

  logging.info('Processing goto.Config:\n%s', str(config))
  generate_files(process_config(config, pathlib.Path(_OUTPUT_DIRECTORY.value)))


if __name__ == '__main__':
  app.run(main)
