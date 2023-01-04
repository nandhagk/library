from mypyguiplusultra.tools import Config, build, clean, config_constants
from pathlib import Path
import runpy
import click

@click.command()
@click.option('--c', is_flag=True)
@click.option('--b', is_flag=True)
@click.option('--r', is_flag=True)
@click.option('-conf', type=click.Path(file_okay=True, dir_okay=False, readable=True, writable=True))
def main(c, b, r, conf):
    if conf is None:conf = "mypyguiplusultra.config.json"

    with Config(conf) as config:
        if c:
            clean(config)
        if b:
            build(config)
    if r:
        with Config(conf) as config:
            import sys
            xs = Path(config[config_constants.SRC_DIRECTORY])
            sys.path.append(xs.parent.as_posix())
            sys.argv.clear()
            sys.argv.append(xs.parent.as_posix())
            sys.argv.append("run")
            runpy.run_module(xs.name)

main()
