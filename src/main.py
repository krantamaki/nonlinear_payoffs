import matplotlib.pyplot as plt
import numpy as np
from option import CallOption, PutOption
from strategy import Butterfly, Condor, CondorChain, StrategyCollection, SineApproximation


def option_visualisation():

    fig = plt.figure(figsize=(8, 4))

    long_call = CallOption(110, "long", 1, premium = 10)
    long_call.plot((80, 120), fig=fig, linewidth=2, label="Long Call ($K = 110$)")
    short_call = CallOption(90, "short", 1, premium = 10)
    short_call.plot((80, 120), fig=fig, linewidth=2, label="Short Call ($K = 90$)")
    long_put = PutOption(105, "long", 1, premium = 10)
    long_put.plot((80, 120), fig=fig, linewidth=2, label="Long Put ($K = 105$)")
    short_put = PutOption(95, "short", 1, premium = 10)
    short_put.plot((80, 120), fig=fig, linewidth=2, label="Short Put ($K = 95$)")

    plt.tight_layout()
    plt.legend()
    fig.savefig("figures/option_visualisation.pdf")


def strategy_visualisation():

    fig = plt.figure(figsize=(8, 4))

    butterfly = Butterfly(100, 7.5, 1)
    butterfly.plot((80, 120), fig=fig, linewidth=2, label="Butterfly ($K = 100$, $d = 7.5$)")
    condor = Condor(90, 7.5, 110, 1)
    condor.plot((80, 120), fig=fig, linewidth=2, label="Condor ($K_l = 90$, $\delta = 7.5$, $K_u = 110$)")

    plt.tight_layout()
    plt.legend()
    fig.savefig("figures/strategy_visualisation.pdf")


def condor_chain_visualisation():

    fig = plt.figure(figsize=(8, 4))

    condor_chain_1 = CondorChain(2 * np.pi, np.pi / 2, 1, 1, (-3 * np.pi, 3 * np.pi))
    condor_chain_1.plot((-2 * np.pi, 2 * np.pi), fig=fig, linewidth=2, label=r"Condor chain ($\lambda = 2 \pi$, $\alpha = \pi / 2$, $\delta = 1$)")
    condor_chain_2 = CondorChain(2 * np.pi, np.pi / 2, 0.25, 1 / 0.25, (-3 * np.pi, 3 * np.pi))
    condor_chain_2.plot((-2 * np.pi, 2 * np.pi), fmt="--", fig=fig, linewidth=2, label=r"Condor chain ($\lambda = 2 \pi$, $\alpha = \pi / 2$, $\delta = 0.25$)")

    plt.tight_layout()
    plt.legend()
    fig.savefig("figures/condor_chain_visualisation.pdf")


def sine_approx_visualisation():

    fig = plt.figure(figsize=(8, 4))

    sine_n2 = SineApproximation(2 * np.pi, np.pi / 2, 2, (-3 * np.pi, 3 * np.pi))
    sine_n2.plot((-2 * np.pi, 2 * np.pi), fig=fig, linewidth=1, label=r"Sine approximation ($n = 2$)")
    sine_n4 = SineApproximation(2 * np.pi, np.pi / 2, 4, (-3 * np.pi, 3 * np.pi))
    sine_n4.plot((-2 * np.pi, 2 * np.pi), fig=fig, linewidth=1, label=r"Sine approximation ($n = 4$)")
    sine_n20 = SineApproximation(2 * np.pi, np.pi / 2, 20, (-3 * np.pi, 3 * np.pi))
    sine_n20.plot((-2 * np.pi, 2 * np.pi), fig=fig, linewidth=1, label=r"Sine approximation ($n = 20$)")

    xx = np.linspace(-2 * np.pi, 2 * np.pi, 1000)
    yy_sin = (1 / 2) * np.sin(xx) + (1 / 2)
    plt.plot(xx, yy_sin, '--', label="Sine exact")

    plt.tight_layout()
    plt.legend()
    fig.savefig("figures/sine_approx_visualisation.pdf")


if __name__ == "__main__":
    option_visualisation()
    strategy_visualisation()
    condor_chain_visualisation()
    sine_approx_visualisation()