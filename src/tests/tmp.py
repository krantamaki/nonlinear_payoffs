import sys
import matplotlib.pyplot as plt
import numpy as np

sys.path.append("..")
from strategy import Condor, CondorChain, StrategyCollection


def main():

    fig = plt.figure(figsize=(12, 6))

    mag = 0.1
    alpha = 0.3
    fmt = '--'

    condor_chain0 = CondorChain(25, 5, 100, mag * 2, (0, 200))
    condor_chain0.plot((0, 200), fig=fig, alpha=alpha, format=fmt)

    condor_chain1 = CondorChain(20, 10, 100, mag, (0, 200))
    condor_chain1.plot((0, 200), fig=fig, alpha=alpha, format=fmt)

    condor_chain1_5 = CondorChain(15, 15, 100, mag/1.5, (0, 200))
    condor_chain1_5.plot((0, 200), fig=fig, alpha=alpha, format=fmt)

    condor_chain2 = CondorChain(10, 20, 100, mag/2, (0, 200))
    condor_chain2.plot((0, 200), fig=fig, alpha=alpha, format=fmt)

    condor_chain2_5 = CondorChain(5, 25, 100, mag/2.5, (0, 200))
    condor_chain2_5.plot((0, 200), fig=fig, alpha=alpha, format=fmt)

    condor_chain3 = CondorChain(0, 30, 100, mag/3, (0, 200))
    condor_chain3.plot((0, 200), fig=fig, alpha=alpha, format=fmt)

    condor_chains = StrategyCollection([condor_chain0, condor_chain1, condor_chain1_5, condor_chain2, condor_chain2_5,
                                        condor_chain3], magnitude=1/6)  # , condor_chain4, condor_chain5])
    condor_chains.plot((0, 200), fig=fig)

    plt.tight_layout()
    fig.savefig("tmp.png")


if __name__ == "__main__":
    main()
