"""Djlint tests specific to pyproject.toml configuration.

run::

   pytest tests/test_config/test_blank_lines_before_tag/test_config.py --cov=src/djlint --cov-branch \
          --cov-report xml:coverage.xml --cov-report term-missing

for a single test, run::

   pytest tests/test_config/test_blank_lines_before_tag/test_config.py::test_blank_lines_before_tag_four --cov=src/djlint \
     --cov-branch --cov-report xml:coverage.xml --cov-report term-missing

"""
# pylint: disable=C0116

from click.testing import CliRunner

from src.djlint import main as djlint


def test_blank_lines_before_tag(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint, ["tests/test_config/test_blank_lines_before_tag/html.html", "--check"]
    )

    assert (
        """+{% extends "nothing.html" %}
+
+{% load stuff %}
+{% load stuff 2 %}
+
+{% include "html_two.html" %}
+<div></div>"""
        in result.output
    )
    assert """1 file would be updated.""" in result.output
    assert result.exit_code == 1


def test_blank_lines_before_tag_two(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint,
        ["tests/test_config/test_blank_lines_before_tag/html_two.html", "--check"],
    )
    assert result.exit_code == 0


def test_blank_lines_before_tag_three(runner: CliRunner) -> None:
    # check blocks that do not start on a newline - they should be left as is.
    result = runner.invoke(
        djlint,
        ["tests/test_config/test_blank_lines_before_tag/html_three.html", "--check"],
    )

    assert """0 files would be updated.""" in result.output
    assert result.exit_code == 0


def test_blank_lines_before_tag_four(runner: CliRunner) -> None:
    result = runner.invoke(
        djlint,
        ["tests/test_config/test_blank_lines_before_tag/html_four.html", "--check"],
    )

    assert result.exit_code == 1
    print(result.output)
    assert (
        """ {% block this %}
-{% load i18n %}
+
+    {% load i18n %}
+
 {% endblock this %}
"""
        in result.output
    )


def test_blank_lines_before_tag_five(runner: CliRunner) -> None:
    # something perfect should stay perfect :)
    result = runner.invoke(
        djlint,
        ["tests/test_config/test_blank_lines_before_tag/html_five.html", "--check"],
    )
    assert result.exit_code == 0


def test_blank_lines_before_tag_six(runner: CliRunner) -> None:
    # something perfect should stay perfect :)
    result = runner.invoke(
        djlint,
        ["tests/test_config/test_blank_lines_before_tag/html_six.html", "--check"],
    )
    assert result.exit_code == 0


def test_blank_lines_before_tag_seven(runner: CliRunner) -> None:
    # make sure endblock doesn't pick up endblocktrans :)
    result = runner.invoke(
        djlint,
        ["tests/test_config/test_blank_lines_before_tag/html_seven.html", "--check"],
    )
    assert result.exit_code == 0


def test_blank_lines_before_tag_eight(runner: CliRunner) -> None:
    # check that multiple blank lines are not added
    result = runner.invoke(
        djlint,
        [
            "tests/test_config/test_blank_lines_before_tag/html_eight.html",
            "--preserve-blank-lines",
            "--check",
        ],
    )
    assert result.exit_code == 0
