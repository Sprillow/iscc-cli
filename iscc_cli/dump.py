# -*- coding: utf-8 -*-
import shutil

import click
import mobi
from click import UsageError
from tika import parser, detector
from iscc_cli.utils import DefaultHelp
from iscc_cli.const import SUPPORTED_MIME_TYPES
import json


@click.command(cls=DefaultHelp)
@click.argument("file", type=click.File("rb"))
@click.option(
    "-s", "--strip", type=click.INT, default=0, help="Strip content to first X chars."
)
@click.option("-m", "--meta", is_flag=True, default=False, help="Dump metadata only.")
@click.option("-c", "--content", is_flag=True, default=False, help="Dump content only.")
def dump(file, strip, meta, content):
    """Dump Tika extraction results for FILE."""

    media_type = detector.from_file(file.name)
    if media_type not in SUPPORTED_MIME_TYPES:
        click.echo("Unsupported media type {}.".format(media_type))
        click.echo("Please request support at https://github.com/iscc/iscc-cli/issues")

    if media_type == "application/x-mobipocket-ebook":
        tempdir, epub_filepath = mobi.extract(file.name)
        tika_result = parser.from_file(epub_filepath)
        shutil.rmtree(tempdir)
    else:
        tika_result = parser.from_file(file.name)

    if all([meta, content]):
        raise UsageError("Use either --meta or --content for selective output.")

    if strip:
        tika_result["content"] = tika_result.get("content", "")[:strip]

    if meta:
        click.echo(json.dumps(tika_result.get("metadata", ""), indent=2))
    elif content:
        click.echo(json.dumps(tika_result.get("content", ""), indent=2))
    else:
        click.echo(json.dumps(tika_result, indent=2))
