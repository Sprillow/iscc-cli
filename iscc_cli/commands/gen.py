# -*- coding: utf-8 -*-
import os
import click
import json
import iscc
from iscc_cli.utils import DefaultHelp
from loguru import logger as log
from iscc.wrappers import decompose


@click.command(cls=DefaultHelp)
@click.argument("file", type=click.File("rb"))
@click.option("-t", "--title", type=click.STRING, help="Title for Meta-Code.")
@click.option("-e", "--extra", type=click.STRING, help="Extra text for Meta-Code.")
@click.pass_context
def gen(ctx, file, title, extra):
    """Generate ISCC Code for FILE."""

    log.info(f"processing: {os.path.basename(file.name)}")
    filesize = os.path.getsize(file.name)
    if not filesize:
        raise click.BadParameter("Cannot proccess empty file: {}".format(file.name))

    try:
        result = iscc.code_iscc(
            file,
            title=title,
            extra=extra,
            all_granular=ctx.obj.granular,
            all_preview=ctx.obj.preview,
            text_store=ctx.obj.store_text,
        )
    except ValueError as e:
        raise click.ClickException(e)

    if ctx.obj.store:
        ctx.obj.index.add(result)

    if ctx.obj.unpack:
        components = decompose(result["iscc"])
        decomposed = "-".join([c.code for c in components])
        result["iscc"] = decomposed

    click.echo(json.dumps(result, indent=2))
