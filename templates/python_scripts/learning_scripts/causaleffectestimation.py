"""Consolidated Python script for ``all.ipynb``.

The notebook demonstrates causal effect estimation, hypothesis testing, and
basic A/B-test monitoring. This script runs the examples end to end and saves
plots to ``all_outputs`` by default.
"""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats
import statsmodels.stats.proportion
from statsmodels.stats.weightstats import CompareMeans, DescrStatsW
import statsmodels.tools.print_version


def save_or_show(fig: plt.Figure, output_path: Path, show: bool) -> None:
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    print(f"Wrote {output_path}")
    if show:
        plt.show()
    else:
        plt.close(fig)


def plot_causal_effect_examples(output_dir: Path, show: bool) -> None:
    x = pd.date_range(dt.datetime(2017, 3, 1), dt.datetime(2017, 4, 1))
    y = np.random.randn(len(x)) * 20 + 1000
    y2 = np.random.randn(len(x)) * 20 + 1000
    y_change = list(np.zeros(int(len(x) / 2))) + list(
        np.ones(int(len(x) / 2)) + 200
    )

    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(x, y + y_change)
    ax.set_ylim(700, 1500)
    ax.set_xlabel("Time")
    ax.set_xlim(x[0], x[-1])
    ax.set_ylabel("Average Revenue/User")
    ax.plot(
        [dt.datetime(2017, 3, 16), dt.datetime(2017, 3, 16)],
        [0, 2000],
        "b--",
        label="Release date",
    )
    ax.legend(loc="upper left")
    save_or_show(fig, output_dir / "causal_effect_treatment_only.png", show)

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(7, 4))
    ax1.plot([dt.datetime(2017, 3, 16), dt.datetime(2017, 3, 16)], [0, 2000], "b--")
    ax1.plot(x, y + y_change, "r-", label="Treatment")
    ax1.set_ylim(700, 1500)
    ax1.legend(loc="upper left")

    ax2.plot(x, y2, "r-", label="Control")
    ax2.plot([dt.datetime(2017, 3, 16), dt.datetime(2017, 3, 16)], [0, 2000], "b--")
    ax2.set_ylim(700, 1500)
    ax2.set_xlabel("Time")
    ax2.set_xlim(x[0], x[-1])
    ax2.legend(loc="upper left")
    fig.text(
        0.04,
        0.5,
        "Average Revenue/User",
        va="center",
        rotation="vertical",
        fontsize=12,
    )
    save_or_show(fig, output_dir / "causal_effect_treatment_control.png", show)


def plot_coin_test(output_dir: Path, show: bool) -> None:
    heads = np.arange(0, 21)
    probabilities = scipy.stats.binom.pmf(heads, 20, 0.5)

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.bar(heads, probabilities)
    ax.set_xlabel("Number of heads")
    ax.set_ylabel("Probability")
    save_or_show(fig, output_dir / "coin_binomial_distribution.png", show)

    p_value = pd.DataFrame({"heads": heads, "probability": probabilities}).query(
        "heads >= 15"
    )["probability"].sum()
    print(p_value)
    print(f"{p_value:,.4f}")


def calc_err(data: dict[str, float]) -> float:
    p = data["p"]
    n = data["n_observation"]
    return float(np.sqrt(p * (1 - p) / n))


def calc_combined_err(
    sample_a: dict[str, float], sample_b: dict[str, float], alpha: float
) -> float:
    p_a = sample_a["p"]
    n_a = sample_a["n_observation"]
    p_b = sample_b["p"]
    n_b = sample_b["n_observation"]
    z = scipy.stats.norm.ppf(1 - alpha / 2)
    return float(z * np.sqrt(p_a * (1 - p_a) / n_a + p_b * (1 - p_b) / n_b))


def calc_diff_confidence_interval(
    sample_a: dict[str, float], sample_b: dict[str, float], alpha: float
) -> tuple[float, float]:
    err = calc_combined_err(sample_a, sample_b, alpha)
    diff = sample_a["p"] - sample_b["p"]
    return (diff - err, diff + err)


def compare_retention_rates(output_dir: Path, show: bool) -> None:
    sample_a = {"n_success": 40, "n_observation": 205, "p": 40 / 205}
    sample_b = {"n_success": 62, "n_observation": 290, "p": 62 / 290}

    print(
        f"Sample A: size={sample_a['n_observation']}, "
        f"converted={sample_a['n_success']}, mean={sample_a['p']:.3f}"
    )
    print(
        f"Sample B: size={sample_b['n_observation']}, "
        f"converted={sample_b['n_success']}, mean={sample_b['p']:.3f}"
    )

    x = np.linspace(0, 1, 200)
    y_a = scipy.stats.norm.pdf(x, sample_a["p"], calc_err(sample_a))
    y_b = scipy.stats.norm.pdf(x, sample_b["p"], calc_err(sample_b))

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(x, y_a, label="Sample A")
    ax.plot(x, y_b, label="Sample B")
    ax.legend(loc="best")
    ax.set_xlabel("Retention rate")
    ax.set_ylabel("Likelihood")
    save_or_show(fig, output_dir / "retention_rate_likelihoods.png", show)

    _, p_value, _, _ = scipy.stats.chi2_contingency(
        [
            [sample_a["n_success"], sample_a["n_observation"] - sample_a["n_success"]],
            [sample_b["n_success"], sample_b["n_observation"] - sample_b["n_success"]],
        ]
    )
    print(p_value)
    print(calc_diff_confidence_interval(sample_a, sample_b, alpha=0.05))


def plot_false_positive_examples(output_dir: Path, show: bool) -> None:
    np.random.seed(34)
    mu = 0.5
    sample = list(scipy.stats.bernoulli.rvs(mu, size=20))
    p_value_history = []

    for _ in range(200):
        _, p_value = scipy.stats.ttest_1samp(sample[-20:], 0.5)
        p_value_history.append(p_value)
        sample.append(scipy.stats.bernoulli.rvs(mu))

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(p_value_history)
    ax.set_xlabel("Test Epoch")
    ax.set_ylabel("p-value")
    save_or_show(fig, output_dir / "rolling_p_values.png", show)

    np.random.seed(31)
    max_sample = 3_000_000
    sample_a = scipy.stats.bernoulli.rvs(0.451, size=max_sample)
    sample_b = scipy.stats.bernoulli.rvs(0.452, size=max_sample)
    p_values = []
    sample_sizes = np.arange(1000, max_sample, 5000)

    for sample_size in sample_sizes:
        _, p_value = scipy.stats.ttest_ind(
            sample_a[:sample_size], sample_b[:sample_size], equal_var=False
        )
        p_values.append(p_value)

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(sample_sizes, p_values)
    ax.set_xlabel("Sample size")
    ax.set_ylabel("p-value")
    save_or_show(fig, output_dir / "sample_size_p_values.png", show)


@np.vectorize
def calc_confidence_interval(n_success: int, n_observed: int) -> tuple[float, float]:
    return statsmodels.stats.proportion.proportion_confint(
        n_success, n_observed, alpha=0.05, method="wilson"
    )


def _calc_diff_confidence_interval(
    n_success_a: int, n_success_b: int, n_observed: int
) -> tuple[float, float]:
    if n_observed < 10:
        return (1.0, -1.0)
    sample_a = DescrStatsW(
        np.append(np.ones(n_success_a), np.zeros(n_observed - n_success_a))
    )
    sample_b = DescrStatsW(
        np.append(np.ones(n_success_b), np.zeros(n_observed - n_success_b))
    )
    lcb, ucb = CompareMeans(sample_a, sample_b).zconfint_diff(alpha=0.05)
    return float(lcb), float(ucb)


calc_diff_interval_vectorized = np.vectorize(
    _calc_diff_confidence_interval, otypes=[float, float]
)


def plot_ab_test_monitoring(output_dir: Path, show: bool) -> None:
    np.random.seed(4)
    sample_size = 14_000

    control = scipy.stats.binom(1, 0.05).rvs(size=sample_size)
    print("E(Y0) =", np.mean(control))
    treatment = scipy.stats.binom(1, 0.065).rvs(size=sample_size)
    print("E(Y1) =", np.mean(treatment))

    n_observed = np.ones(sample_size).cumsum().astype(int)
    treatment_p = treatment.cumsum() / n_observed
    control_p = control.cumsum() / n_observed

    treatment_lcb, treatment_ucb = calc_confidence_interval(
        treatment.cumsum(), n_observed
    )
    control_lcb, control_ucb = calc_confidence_interval(control.cumsum(), n_observed)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(n_observed, treatment_p, label="Treatment estimate")
    ax.fill_between(
        n_observed, treatment_lcb, treatment_ucb, alpha=0.3, interpolate=True
    )
    ax.plot(n_observed, control_p, linestyle="dashed", label="Control estimate")
    ax.fill_between(n_observed, control_lcb, control_ucb, alpha=0.3, interpolate=True)
    ax.legend(loc="best")
    ax.set_xlim(0, 10000)
    ax.set_xlabel("Observed sample size")
    ax.set_ylabel("E(Y)")
    ax.set_ylim(0.030, 0.08)
    save_or_show(fig, output_dir / "ab_test_group_estimates.png", show)

    diff_interval_lcb, diff_interval_ucb = calc_diff_interval_vectorized(
        treatment.cumsum(), control.cumsum(), n_observed
    )
    diff = treatment_p - control_p

    xmax = 10000
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(n_observed, diff, color="green", label="Treatment effect estimate")
    ax.fill_between(
        n_observed,
        diff_interval_lcb,
        diff_interval_ucb,
        alpha=0.6,
        color="lightgreen",
        interpolate=True,
    )
    ax.hlines([0], 0, xmax, "black")
    ax.hlines(
        [0.015],
        0,
        xmax,
        "green",
        linestyles="dashed",
        label="True treatment effect",
    )
    ax.set_ylim(-0.02, 0.03)
    ax.set_ylabel("Difference in E(Y)")
    ax.set_xlabel("Observed sample size")
    ax.legend(loc="best")
    ax.set_xlim(0, xmax)
    save_or_show(fig, output_dir / "ab_test_effect_estimate.png", show)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run examples from all.ipynb.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("all_outputs"),
        help="Directory where generated figures are written.",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Display plots interactively after saving them.",
    )
    parser.add_argument(
        "--versions",
        action="store_true",
        help="Print statsmodels dependency versions before running examples.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    if args.versions:
        print(statsmodels.tools.print_version.show_versions())

    plot_causal_effect_examples(args.output_dir, args.show)
    plot_coin_test(args.output_dir, args.show)
    compare_retention_rates(args.output_dir, args.show)
    plot_false_positive_examples(args.output_dir, args.show)
    plot_ab_test_monitoring(args.output_dir, args.show)


if __name__ == "__main__":
    main()
