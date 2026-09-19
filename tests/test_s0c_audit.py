import math
import numpy as np
from analysis.s0c_audit import loss_budget
from analysis.s0c_1_pilot import fir_match


def test_amplifier_loss_requires_gain_and_degrades_snr_without_inventing_power():
    low, high = loss_budget(3), loss_budget(20)
    assert math.isclose(high['gain_db']-low['gain_db'],17)
    assert high['ase_mw'] > low['ase_mw']
    assert high['output_snr_db'] < low['output_snr_db']
    assert high['electrical_total_mw'] is None
    assert not loss_budget(30)['within_illustrative_30db_gain_16dbm_output_limits']


def test_fir_reference_matches_independent_complex_least_squares():
    f = np.fft.fftfreq(32)
    channel = np.exp(11j*f*f)
    errors = fir_match(channel,0)['nmse_by_taps']
    for taps in [1,3,9]:
        a = channel[:,None]*np.exp(-2j*np.pi*f[:,None]*np.arange(taps))
        best = float('inf')
        for delay in range(32):
            y = np.exp(-2j*np.pi*f*delay)
            w = np.linalg.lstsq(a,y,rcond=None)[0]
            best = min(best,float(np.mean(abs(a@w-y)**2)))
        assert math.isclose(errors[taps-1],best,abs_tol=2e-14)
