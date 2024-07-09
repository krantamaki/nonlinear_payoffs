import matplotlib.pyplot as plt
import numpy as np
from option import CallOption, PutOption
from strategy import Butterfly, Condor, CondorChain, StrategyCollection, SineApproximation


lw = 1.5
figsize = (8, 4)


def option_visualisation():

    fig = plt.figure(figsize=figsize)

    long_call = CallOption(110, "long", 1, premium = 10)
    long_call.plot((80, 120), fig=fig, linewidth=lw, label="Long Call ($K = 110$)")
    short_call = CallOption(90, "short", 1, premium = 10)
    short_call.plot((80, 120), fig=fig, linewidth=lw, label="Short Call ($K = 90$)")
    long_put = PutOption(105, "long", 1, premium = 10)
    long_put.plot((80, 120), fig=fig, linewidth=lw, label="Long Put ($K = 105$)")
    short_put = PutOption(95, "short", 1, premium = 10)
    short_put.plot((80, 120), fig=fig, linewidth=lw, label="Short Put ($K = 95$)")

    plt.xlabel("$S$")
    plt.ylabel("Payoff (shifted)")
    plt.tight_layout()
    plt.legend()
    fig.savefig("figures/option_visualisation.pdf")


def strategy_visualisation():

    fig = plt.figure(figsize=figsize)

    butterfly = Butterfly(100, 7.5, 1)
    butterfly.plot((80, 120), fig=fig, linewidth=lw, label="Butterfly ($K = 100$, $d = 7.5$)")
    condor = Condor(90, 7.5, 110, 1)
    condor.plot((80, 120), fig=fig, linewidth=lw, label="Condor ($K_l = 90$, $\delta = 7.5$, $K_u = 110$)")

    plt.xlabel("$S$")
    plt.ylabel("Payoff")
    plt.tight_layout()
    plt.legend()
    fig.savefig("figures/strategy_visualisation.pdf")


def condor_chain_visualisation():

    fig = plt.figure(figsize=figsize)

    condor_chain_1 = CondorChain(2 * np.pi, np.pi / 2, 1, 1, (-3 * np.pi, 3 * np.pi))
    condor_chain_1.plot((-2 * np.pi, 2 * np.pi), fig=fig, linewidth=lw, label=r"Condor chain ($\lambda = 2 \pi$, $\alpha = \pi / 2$, $\delta = 1$)")
    condor_chain_2 = CondorChain(2 * np.pi, np.pi / 2, 0.25, 1 / 0.25, (-3 * np.pi, 3 * np.pi))
    condor_chain_2.plot((-2 * np.pi, 2 * np.pi), fmt="--", fig=fig, linewidth=lw, label=r"Condor chain ($\lambda = 2 \pi$, $\alpha = \pi / 2$, $\delta = 0.25$)")

    plt.xlabel("$S$")
    plt.ylabel("Payoff")
    plt.tight_layout()
    plt.legend()
    fig.savefig("figures/condor_chain_visualisation.pdf")


def sine_approx_visualisation():

    fig = plt.figure(figsize=figsize)

    sine_n2 = SineApproximation(2 * np.pi, np.pi / 2, 2, (-3 * np.pi, 3 * np.pi))
    sine_n2.plot((-2 * np.pi, 2 * np.pi), fig=fig, linewidth=lw, label=r"Sine approximation ($n = 2$)")
    sine_n4 = SineApproximation(2 * np.pi, np.pi / 2, 4, (-3 * np.pi, 3 * np.pi))
    sine_n4.plot((-2 * np.pi, 2 * np.pi), fig=fig, linewidth=lw, label=r"Sine approximation ($n = 4$)")
    sine_n20 = SineApproximation(2 * np.pi, np.pi / 2, 20, (-3 * np.pi, 3 * np.pi))
    sine_n20.plot((-2 * np.pi, 2 * np.pi), fig=fig, linewidth=lw, label=r"Sine approximation ($n = 20$)")

    xx = np.linspace(-2 * np.pi, 2 * np.pi, 1000)
    yy_sin = (1 / 2) * np.sin(xx) + (1 / 2)
    plt.plot(xx, yy_sin, '--', label="Sine exact")

    plt.xlabel("$S$")
    plt.ylabel("Payoff")
    plt.tight_layout()
    plt.legend()
    fig.savefig("figures/sine_approx_visualisation.pdf")


def sine_formulation_visualisation():

    fig = plt.figure(figsize=figsize)

    sine_n10 = SineApproximation(2 * np.pi, np.pi / 2, 10, (-3 * np.pi, 3 * np.pi))
    sine_n10.plot((-2 * np.pi, 2 * np.pi), fig=fig, linewidth=lw, label=r"Sine approximation ($n = 10$)")

    sine_n10.plot_condors((-2 * np.pi, 2 * np.pi), fig=fig, alpha=0.3, linewidth=lw)

    xx = np.linspace(-2 * np.pi, 2 * np.pi, 1000)
    yy_sin = (1 / 2) * np.sin(xx) + (1 / 2)
    plt.plot(xx, yy_sin, '--', label="Sine exact")

    plt.xlabel("$S$")
    plt.ylabel("Payoff")
    plt.tight_layout()
    plt.legend()
    fig.savefig("figures/sine_form_visualisation.pdf")


def sine_num_analysis_visualisation():

    n_points = 1000

    xx = np.linspace(-2 * np.pi, 2 * np.pi, n_points)
    yy_sin = (1 / 2) * np.sin(xx) + (1 / 2)

    d_arr = []
    n_range = range(5, 205, 5)

    for n in n_range:
        sine_n = SineApproximation(2 * np.pi, np.pi / 2, n, (-3 * np.pi, 3 * np.pi))
        yy_approx = np.array([sine_n(x) for x in xx])

        d_n = np.linalg.norm(yy_sin - yy_approx)
        d_arr.append(d_n)

        if n % 10 == 0:
            print(f"Distance for n = {n}: {d_n} (average distance: {d_n / n_points})")

    fig = plt.figure(figsize=figsize)

    plt.plot(list(n_range), d_arr, linewidth=lw)

    plt.xlabel("$n$")
    plt.ylabel("Euclidean distance")
    plt.tight_layout()
    # plt.legend()
    fig.savefig("figures/numerical_analysis_visualisation.pdf")


if __name__ == "__main__":
    option_visualisation()
    strategy_visualisation()
    condor_chain_visualisation()
    sine_approx_visualisation()
    sine_formulation_visualisation()
    sine_num_analysis_visualisation()  # This might take a while
