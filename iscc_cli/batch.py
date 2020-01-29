# -*- coding: utf-8 -*-
from os.path import basename, abspath
import click
from tika import detector, parser
import iscc

from iscc_cli import video_id
from iscc_cli.const import SUPPORTED_MIME_TYPES, GMT
from iscc_cli.utils import get_files, mime_to_gmt, get_title, DefaultHelp
from iscc_cli import audio_id, fpcalc


@click.command(cls=DefaultHelp)
@click.argument("path", type=click.Path(exists=True))
@click.option("-r", "--recursive", is_flag=True, help="Recurse into subdirectories.")
@click.option(
    "-g",
    "--guess",
    is_flag=True,
    default=False,
    help="Guess title (first line of text).",
)
def batch(path, recursive, guess):
    """Create ISCC Codes for all files in PATH.

    Example:

      $ iscc batch ~/Documents

    """
    results = []
    for f in get_files(path, recursive=recursive):
        media_type = detector.from_file(f)
        if media_type not in SUPPORTED_MIME_TYPES:
            fname = basename(f)
            click.echo(
                "Unsupported file {} with mime type: {}".format(fname, media_type)
            )
            click.echo(
                "Please request support at https://github.com/iscc/iscc-cli/issues"
            )
            continue

        tika_result = parser.from_file(f)
        title = get_title(tika_result, guess=guess)

        mid, norm_title, _ = iscc.meta_id(title)
        gmt = mime_to_gmt(media_type, file_path=f)
        if gmt == GMT.IMAGE:
            cid = iscc.content_id_image(f)
        elif gmt == GMT.TEXT:
            text = tika_result["content"]
            if not text:
                click.echo("Could not extract text from {}".format(basename(f)))
                continue
            cid = iscc.content_id_text(tika_result["content"])
        elif gmt == GMT.AUDIO:
            if not fpcalc.is_installed():
                fpcalc.install()
            features = audio_id.get_chroma_vector(f)
            cid = audio_id.content_id_audio(features)
        elif gmt == GMT.VIDEO:
            features = video_id.get_frame_vectors(abspath(f))
            cid = video_id.content_id_video(features)

        did = iscc.data_id(f)
        iid, tophash = iscc.instance_id(f)

        if not norm_title:
            iscc_code = "-".join((cid, did, iid))
        else:
            iscc_code = "-".join((mid, cid, did, iid))

        click.echo(
            "ISCC:{iscc_code},{tophash},{fname},{gmt},{title}".format(
                iscc_code=iscc_code,
                tophash=tophash,
                fname=basename(f),
                gmt=gmt,
                title=norm_title,
            )
        )
        results.append(
            dict(
                iscc=iscc_code,
                norm_title=norm_title,
                tophash=tophash,
                gmt=gmt,
                file_name=basename(f),
            )
        )

    return results