"""
Make the pictures the tutorial and the README show, from a checkout of Alto.

The tutorial page includes `docs/assets/img/plugin-harpsichord-intervals.png`, `-parts.png` and `-lesson.png` with Alto's
`shot.html`, so those names must stay as they are. Each comes in a light and a dark theme (`-dark.png`). The README shows the
same three, and `readme/harpsichord-sound.png` as well, which only the README uses and the docs website never publishes.

Run it from the root of this repository, with Alto's own environment, and point it at the Alto checkout:

    QT_QPA_PLATFORM=offscreen /path/to/alto/.venv/bin/python scripts/screenshots.py --alto /path/to/alto

It uses a made-up profile and a temporary settings folder, so it never touches your own history or settings.
"""

from __future__ import annotations

import argparse
import os
import random
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
PACK = HERE / "docs/assets/plugins/harpsichord"
OUT = HERE / "docs/assets/img"
README = HERE / "readme"
THEMES = ("light", "dark")


def capture(theme: str, *, alto: Path) -> None:
    """
    Take the pictures of one theme, in this process.

    Parameters
    ----------
    theme : str
        "light" or "dark".
    alto : Path
        The Alto checkout whose code takes the pictures.
    """
    sys.path.insert(0, str(alto))
    import alto.ui.exercise_view as exercise_view  # noqa: PLC0415
    from PySide6.QtCore import Qt  # noqa: PLC0415
    from PySide6.QtWidgets import QApplication  # noqa: PLC0415

    from alto.exercises import REGISTRY  # noqa: PLC0415
    from alto.exercises.packs import load_packs  # noqa: PLC0415
    from alto.learning import Database, Learner  # noqa: PLC0415
    from alto.ui.app_settings import AppSettingsDialog  # noqa: PLC0415
    from alto.ui.main_window import MainWindow  # noqa: PLC0415
    from alto.ui.store import store  # noqa: PLC0415
    from alto.ui.theme import apply_theme  # noqa: PLC0415

    suffix = "" if theme == "light" else "-dark"
    app = QApplication([])
    apply_theme("studio_dark" if theme == "dark" else "studio")
    original = exercise_view.ExerciseView.__init__
    # The same question every time, so that a new picture differs only where Alto does.
    exercise_view.ExerciseView.__init__ = lambda self, exercise, *, rng=None, parent=None, learner=None: original(
        self,
        exercise,
        rng=random.Random(5),
        parent=parent,
        learner=learner,
    )

    def wait(ms: int = 450) -> None:
        """Keep the application busy for a while, so animations and layout settle."""
        end = time.time() + ms / 1000
        while time.time() < end:
            app.processEvents()

    def save(widget: object, path: Path) -> None:
        """Save a picture of a widget, and check that it came out in the theme that was asked for."""
        wait(250)
        picture = widget.grab()  # type: ignore[attr-defined]
        if (picture.toImage().pixelColor(10, 10).lightness() < 128) != (theme == "dark"):
            raise RuntimeError(f"{path.name} did not render in the {theme} theme.")
        picture.save(str(path.with_name(f"{path.stem}{suffix}.png")), "PNG")

    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        shutil.copytree(PACK, folder / "harpsichord")  # the pack as an editable folder, which Alto loads like an installed one
        if problems := load_packs(folder):
            raise RuntimeError("\n".join(problems))
        db = Database()
        learner = Learner(db, profile=db.add_profile("Ada"))
        store().setValue("ui/sidebarWidth", 290)
        window = MainWindow(learner)
        window.resize(1100, 720)
        window.show()
        wait()
        by_class = {cls.__name__: cls for cls in REGISTRY}
        for name, key in (
            ("plugin-harpsichord-intervals", "pack.harpsichord.intervals-on-two-manuals"),
            ("plugin-harpsichord-parts", "pack.harpsichord.harpsichord-parts"),
        ):
            window.open_exercise(by_class[key])
            wait()
            window.nav.scrollToItem(window._items[by_class[key]], window.nav.ScrollHint.PositionAtCenter)  # noqa: SLF001
            save(window, OUT / name)
        window.open_lessons("pack.harpsichord.intervals-on-the-keys")
        window._lesson_page.view.go(to=1)  # noqa: SLF001
        save(window, OUT / "plugin-harpsichord-lesson")
        dialog = AppSettingsDialog(window, learner=learner)
        dialog.resize(1000, 720)
        dialog.show()
        dialog.categories.setCurrentItem(dialog.categories.findItems("Sound", Qt.MatchFlag.MatchExactly)[0])
        dialog.instruments.select("pack.harpsichord.flemish-harpsichord")
        save(dialog, README / "harpsichord-sound")
        dialog.close()
        window.close()
        db.close()


def main() -> int:
    """
    Make the pictures in both themes, each in its own process with its own throwaway settings.

    Returns
    -------
    int
        0 when every picture was made.
    """
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--alto", type=Path, default=HERE.parent / "alto", help="the Alto checkout (default: ../alto)")
    parser.add_argument("--theme", choices=THEMES, help="make one theme in this process (used by the script itself)")
    args = parser.parse_args()
    alto = args.alto.resolve()
    OUT.mkdir(parents=True, exist_ok=True)
    README.mkdir(parents=True, exist_ok=True)
    if args.theme:
        capture(args.theme, alto=alto)
        return 0
    for theme in THEMES:
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ, XDG_CONFIG_HOME=f"{tmp}/config", XDG_DATA_HOME=f"{tmp}/data")
            env.setdefault("QT_QPA_PLATFORM", "xcb" if os.environ.get("DISPLAY") else "offscreen")
            command = [sys.executable, str(Path(__file__).resolve()), "--theme", theme, "--alto", str(alto)]
            if subprocess.run(command, env=env, cwd=HERE, check=False).returncode:
                return 1
    print(f"wrote 8 pictures to {OUT} and {README}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
