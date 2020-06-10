"""
Created at 12.08.2019

@author: Piotr Bartman
@author: Sylwester Arabas
"""

import numpy as np
from matplotlib import pyplot
from PySDM.physics.constants import si
from PySDM.physics import formulae as phys
from labellines import labelLine, labelLines


class Plotter:
    def __init__(self, setup):
        self.setup = setup
        size = 2*5.236
        pyplot.figure(num=1, figsize=(size, size * 0.54))

    def show(self, title=None):
        pyplot.xscale('log', basex=2)
        xticks = [4, 6.25, 12.5, 25, 50, 100, 200]
        pyplot.xticks(xticks, xticks)
        pyplot.yticks([0.5 * i for i in range(5)], [0, None, 1, None, 2])
        pyplot.xlabel('particle radius [µm]')
        pyplot.ylabel('dm/dlnr [g/m^3/(unit dr/r)]')
        # labelLines(pyplot.gca().get_lines(), zorder=2.5)
        pyplot.title(title)
        pyplot.grid()
        pyplot.show()

    def save(self, file):
        pyplot.savefig(file)

    def plot(self, vals, t):
        setup = self.setup

        if t == 0:
            analytic_solution = setup.spectrum.size_distribution
        else:
            analytic_solution = lambda x: setup.norm_factor * setup.kernel.analytic_solution(
                x=x, t=t, x_0=setup.X0, N_0=setup.n_part
            )

        volume_bins_edges = phys.volume(setup.radius_bins_edges)
        dm = np.diff(volume_bins_edges)
        dr = np.diff(setup.radius_bins_edges)

        pdf_m_x = volume_bins_edges[:-1] + dm / 2
        pdf_m_y = analytic_solution(pdf_m_x)

        pdf_r_x = setup.radius_bins_edges[:-1] + dr / 2
        pdf_r_y = pdf_m_y * dm / dr * pdf_r_x

        # pyplot.plot(
        #     pdf_r_x * si.metres / si.micrometres,
        #     pdf_r_y * phys.volume(radius=pdf_r_x) * setup.rho / setup.dv * si.kilograms / si.grams,
        #     color='black'
        # )

        new = np.copy(vals)
        for _ in range(2):
            scope = 1
            for i in range(scope, len(vals)-scope):
                new[i] = np.mean(vals[i-scope:i+scope+1])
            scope = 1
            for i in range(scope, len(vals) - scope):
                vals[i] = np.mean(new[i - scope:i + scope + 1])

        pyplot.plot(
            setup.radius_bins_edges[:-scope-1] * si.metres / si.micrometres,
            vals[:-scope] * si.kilograms / si.grams,
            label=f"{t}",
            color='black'
        )

        # pyplot.step(
        #     setup.radius_bins_edges[:-1] * si.metres / si.micrometres,
        #     vals * si.kilograms / si.grams,
        #     where='post',
        #     label=f"t = {t}s"
        # )


