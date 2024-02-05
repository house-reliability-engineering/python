"""Testing the style of the code."""

import contextlib
import os
import pathlib
import re
import types
from typing import ClassVar, Sequence, Tuple

import black
import click
import isort.main
import pycodestyle
import pylint.lint


class TestStyle:
    """Testing the style of the package and tests code."""

    modules: ClassVar[Sequence[types.ModuleType]]

    @property
    def _paths(self) -> Tuple[str]:
        return tuple(str(pathlib.Path(m.__file__).parent) for m in self.modules)

    def test_isort(self):
        """Checks imports order with isort."""
        try:
            isort.main.main(
                [
                    "--check-only",
                    # otherwise it fights with black over
                    # an empty line in imports of this file
                    "--ignore-whitespace",
                    "--line-length",
                    str(black.DEFAULT_LINE_LENGTH),
                    *self._paths,
                ]
            )
        except SystemExit as e:
            self.assertEqual(e.code, 0)

    def test_pylint(self):
        """Checks style with pylint."""
        with open(
            os.devnull, "w", encoding="utf-8"
        ) as devnull, contextlib.redirect_stdout(devnull):
            run = pylint.lint.Run(
                self._paths,
                exit=False,
            )
            self.assertEqual(run.linter.generate_reports(), 10.0)

    def test_black(self):
        """Checks formatting with black."""
        ctx = click.Context(click.Command("test"))
        with self.assertRaises(click.exceptions.Exit) as e:
            ctx.invoke(
                black.main,
                check=True,
                include=re.compile(r"\.py$"),
                quiet=True,
                src=self._paths,
                target_version=[],
                enable_unstable_feature=[],
            )
        self.assertEqual(e.exception.exit_code, 0)

    def test_pycodestyle(self):
        """Checks PEP8 compliance with pycodestyle."""
        option_parser = pycodestyle.get_parser()
        option_parser.set_default(
            "max_line_length",
            black.DEFAULT_LINE_LENGTH,
        )
        style_guide = pycodestyle.StyleGuide(
            parser=option_parser,
            paths=[*self._paths],
        )
        report = style_guide.check_files()
        self.assertEqual(report.total_errors, 0)
