"""Plot decision boundaries for several scikit-learn classifiers.

This script is a consolidated version of ``decisionboundary.ipynb``. By
default it writes one PNG per classifier to ``decision_boundary_outputs``.
Use ``--show`` to display figures interactively.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy.random import normal as rnorm
from numpy.random import seed
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression, Perceptron
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


plt.rcParams["font.size"] = 16


def make_linear_data(n: int = 50, random_seed: int = 100) -> pd.DataFrame:
    """Create a two-class dataset that is roughly linearly separable."""
    seed(random_seed)

    p1 = pd.DataFrame(
        np.hstack(
            (
                rnorm(loc=2.0, scale=0.5, size=(n, 1)),
                rnorm(loc=2.0, scale=0.5, size=(n, 1)),
            )
        ),
        columns=["x", "y"],
    )
    p1["label"] = 0

    p2 = pd.DataFrame(
        np.hstack(
            (
                rnorm(loc=1.0, scale=0.5, size=(n, 1)),
                rnorm(loc=1.0, scale=0.5, size=(n, 1)),
            )
        ),
        columns=["x", "y"],
    )
    p2["label"] = 1

    return pd.concat([p1, p2], ignore_index=True)


def make_xor_data(n: int = 50) -> pd.DataFrame:
    """Create a two-class XOR-pattern dataset."""
    p1 = pd.DataFrame(
        np.hstack(
            (
                rnorm(loc=1.0, scale=1.0, size=(n, 1)),
                rnorm(loc=1.0, scale=1.0, size=(n, 1)),
            )
        ),
        columns=["x", "y"],
    )
    p1["label"] = 0

    p2 = pd.DataFrame(
        np.hstack(
            (
                rnorm(loc=-1.0, scale=1.0, size=(n, 1)),
                rnorm(loc=1.0, scale=1.0, size=(n, 1)),
            )
        ),
        columns=["x", "y"],
    )
    p2["label"] = 1

    p3 = pd.DataFrame(
        np.hstack(
            (
                rnorm(loc=-1.0, scale=1.0, size=(n, 1)),
                rnorm(loc=-1.0, scale=1.0, size=(n, 1)),
            )
        ),
        columns=["x", "y"],
    )
    p3["label"] = 0

    p4 = pd.DataFrame(
        np.hstack(
            (
                rnorm(loc=1.0, scale=1.0, size=(n, 1)),
                rnorm(loc=-1.0, scale=1.0, size=(n, 1)),
            )
        ),
        columns=["x", "y"],
    )
    p4["label"] = 1

    return pd.concat([p1, p2, p3, p4], ignore_index=True)


def plot_result(
    ax: plt.Axes,
    clf,
    clf_name: str,
    df: pd.DataFrame,
    colorize: bool = False,
) -> None:
    """Fit a classifier and plot its decision boundary on ``ax``."""
    x = df[["x", "y"]]
    y = df["label"]
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.4, random_state=40
    )
    n_classes = len(y.unique())

    if colorize:
        cmap = plt.cm.RdBu
        plot_colors = "rbym"
    else:
        cmap = plt.cm.Greys
        plot_colors = "wkym"
    plot_markers = "o^v*"
    plot_step = 0.02

    x_min, x_max = x.iloc[:, 0].min() - 0.5, x.iloc[:, 0].max() + 0.5
    y_min, y_max = x.iloc[:, 1].min() - 0.5, x.iloc[:, 1].max() + 0.5
    xx, yy = np.meshgrid(
        np.arange(x_min, x_max, plot_step),
        np.arange(y_min, y_max, plot_step),
    )

    clf.fit(x_train, y_train)
    score = clf.score(x_test, y_test)

    grid = pd.DataFrame({"x": xx.ravel(), "y": yy.ravel()})
    z = clf.predict(grid).reshape(xx.shape)
    ax.contourf(xx, yy, z, cmap=cmap, alpha=0.5)

    for class_index, class_color, marker in zip(
        range(n_classes), plot_colors, plot_markers
    ):
        class_points = x[y == class_index]
        ax.scatter(
            class_points.x,
            class_points.y,
            facecolor=class_color,
            edgecolor="k",
            label=class_index,
            marker=marker,
            s=80,
        )

    ax.text(
        xx.max() - 0.3,
        yy.min() + 0.3,
        ("%.2f" % score).lstrip("0"),
        size=15,
        horizontalalignment="right",
    )
    ax.set_title(clf_name)


def build_classifiers() -> list[tuple[str, object]]:
    """Return the classifiers used in the original notebook."""
    return [
        ("Perceptron", Perceptron(max_iter=1000)),
        ("LogisticRegression", LogisticRegression()),
        ("k-NN", KNeighborsClassifier(3)),
        ("Decision Tree", DecisionTreeClassifier(random_state=1)),
        ("Random Forest", RandomForestClassifier(random_state=1)),
        ("SVM (linear)", SVC(kernel="linear")),
        ("SVM (RBF)", SVC(kernel="rbf")),
        (
            "NN",
            MLPClassifier(
                solver="lbfgs",
                alpha=0.01,
                hidden_layer_sizes=(5, 2),
                random_state=1,
            ),
        ),
        ("GBDT", GradientBoostingClassifier(random_state=1)),
    ]


def save_classifier_plot(
    name: str,
    clf,
    linear_data: pd.DataFrame,
    xor_data: pd.DataFrame,
    output_dir: Path,
    show: bool,
) -> Path:
    """Create side-by-side linear and XOR plots for a classifier."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), constrained_layout=True)
    plot_result(axes[0], clf, name, linear_data, colorize=True)
    plot_result(axes[1], clf, f"{name} (XOR)", xor_data, colorize=True)

    filename = (
        name.lower()
        .replace(" ", "_")
        .replace("(", "")
        .replace(")", "")
        .replace("-", "nn")
    )
    output_path = output_dir / f"{filename}.png"
    fig.savefig(output_path, dpi=150)

    if show:
        plt.show()
    else:
        plt.close(fig)

    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot decision boundaries for multiple classifiers."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("decision_boundary_outputs"),
        help="Directory where PNG files are written.",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Display figures interactively after saving them.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    linear_data = make_linear_data()
    xor_data = make_xor_data()

    for name, clf in build_classifiers():
        output_path = save_classifier_plot(
            name,
            clf,
            linear_data,
            xor_data,
            args.output_dir,
            args.show,
        )
        print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
