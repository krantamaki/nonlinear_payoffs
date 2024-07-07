import sys
import matplotlib.pyplot as plt
import numpy as np

sys.path.append("..")
from option import CallOption, PutOption
from strategy import Condor, CondorChain, StrategyCollection


def main():

    fig = plt.figure(figsize=(8, 4))

    long_call = CallOption(110, "long", 1, premium = 10)
    long_call.plot((80, 120), fig=fig, label="Long Call ($K = 110$)")
    short_call = CallOption(90, "short", 1, premium = 10)
    short_call.plot((80, 120), fig=fig, label="Short Call ($K = 90$)")
    long_put = PutOption(105, "long", 1, premium = 10)
    long_put.plot((80, 120), fig=fig, label="Long Put ($K = 105$)")
    short_put = PutOption(95, "short", 1, premium = 10)
    short_put.plot((80, 120), fig=fig, label="Short Put ($K = 95$)")

    plt.tight_layout()
    plt.legend()
    fig.savefig("option_tmp.pdf")


    fig = plt.figure(figsize=(10, 5))

    alpha = 0.3
    fmt = '--'

    _lambda = 2 * np.pi
    _alpha = np.pi / 2
    eval_range = (-2 * np.pi, 2 * np.pi)

    n = 100
    condor_chains = []
    mag_sum = 0

    for i in range(1, n + 1):
        diff = (i * _lambda) / (2 * n)
        mag = np.sin(diff / 2) * i / n
        mag_sum += mag
        tmp_chain = CondorChain(_lambda, _alpha, diff, (1 / diff) * mag, eval_range)
        tmp_chain.plot(eval_range, fig=fig, alpha=alpha, fmt=fmt)
        condor_chains.append(tmp_chain)

    condor_strategy = StrategyCollection(condor_chains, magnitude=1 / mag_sum)
    condor_strategy.plot(eval_range, fig=fig, label="Sine approximation")

    xx = np.linspace(eval_range[0], eval_range[1], 1000)
    yy_sin = (1 / 2) * np.sin(xx) + (1 / 2)
    plt.plot(xx, yy_sin, '--', label="Sine exact")

    plt.tight_layout()
    plt.legend()
    fig.savefig("condor_tmp.pdf")


if __name__ == "__main__":
    main()
