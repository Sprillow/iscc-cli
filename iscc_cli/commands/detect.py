# -*- coding: utf-8 -*-
import json
import click
import iscc
from iscc_cli.utils import DefaultHelp


@click.command(cls=DefaultHelp)
@click.argument("file", type=click.File("rb"))
@click.pass_context
def detect(ctx, file):
    """Detect mediatype of file."""

    header = file.read(4096)
    file.seek(0)
    result = dict(
        mime_from_name=iscc.mime_from_name(file.name),
        mime_from_data=iscc.mime_from_data(header),
    )

    mg = iscc.mime_guess(file)
    result["mime_guess"] = mg
    result["gmt"] = iscc.mime_to_gmt(mg, file.name)
    result["supported"] = iscc.mime_supported(mg)
    click.echo(json.dumps(result, indent=2))