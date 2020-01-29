import os
from tests import ROOT_DIR
from iscc_cli.cli import cli
from click.testing import CliRunner


os.chdir(ROOT_DIR)
r = CliRunner()


def test_gen_no_arg_shows_help():
    result = r.invoke(cli, ["gen"])
    assert result.exit_code == 0
    assert "-t, --title TEXT" in result.output


def test_gen_single_file():
    result = r.invoke(cli, ["gen", "tests/image/demo.jpg"])
    assert result.exit_code == 0
    assert "CC1GG3hSxtbWU-CYDfTq7Qc7Fre-CDYkLqqmQJaQk-CRAPu5NwQgAhv" in result.output


def test_gen_single_guess():
    result = r.invoke(cli, ["gen", "tests/text/demo.doc"])
    assert result.exit_code == 0
    assert "ISCC:CCKzUpp6U5hU7-CTMjk4o5H96BV-CDM6E14HcCZjQ-CR1LUvGDVrWye" in result.output
    result = r.invoke(cli, ["gen", "-g", "tests/text/demo.doc"])
    assert result.exit_code == 0
    assert (
        "ISCC:CCKzUpp6U5hU7-CTMjk4o5H96BV-CDM6E14HcCZjQ-CR1LUvGDVrWye" in result.output
    )


def test_gen_python_call():
    from iscc_cli.gen import gen

    file = open("tests/text/demo.doc")
    result = gen.callback(file, True, "", "", True)
    assert result["iscc"] == "CCKzUpp6U5hU7-CTMjk4o5H96BV-CDM6E14HcCZjQ-CR1LUvGDVrWye"
    assert result["norm_title"] == "demo doc title from metadata"