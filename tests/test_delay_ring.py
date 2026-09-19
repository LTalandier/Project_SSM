import math
import numpy as np
import torch
from scipy.signal import lfilter
from photonic_ssm.delay_ring import ring_cascade, decode_controls, fit_response, chromatic_dispersion


def test_exact_roundtrip_recurrence_and_fractional_grid():
    n = 8192
    phase, k = 0.4, 0.1
    a = 10 ** (-0.051 * 2 * math.pi * 242.2002619 * 1e-4 / 20)
    t = math.sqrt(1-k)
    impulse = np.zeros(n); impulse[0] = 1
    response = np.fft.fft(lfilter([t, -a*np.exp(1j*phase)], [1, -t*a*np.exp(1j*phase)], impulse))
    f = torch.tensor(np.fft.fftfreq(n, 1/100e9))
    exact = ring_cascade(f, torch.tensor([phase], dtype=torch.float64), torch.tensor([k], dtype=torch.float64))
    np.testing.assert_allclose(exact.numpy(), response, atol=2e-13)
    # Fractional symbol grid must use f/FSR, not f/symbol_rate.
    f64 = torch.fft.fftfreq(512, d=1/64e9, dtype=torch.float64)
    got = ring_cascade(f64, torch.tensor([phase], dtype=torch.float64), torch.tensor([k], dtype=torch.float64))
    q = a*np.exp(1j*phase-2j*np.pi*f64.numpy()/100e9)
    np.testing.assert_allclose(got.numpy(), (t-q)/(1-t*q), atol=2e-13)


def test_passivity_and_lossless_limit():
    f = torch.linspace(-100e9, 100e9, 4096, dtype=torch.float64)
    p = torch.tensor([0.1, 1.2], dtype=torch.float64)
    k = torch.tensor([0.05, 0.2], dtype=torch.float64)
    assert ring_cascade(f,p,k).abs().max() <= 1+1e-12
    torch.testing.assert_close(ring_cascade(f,p,k,loss_db_cm=0).abs(), torch.ones_like(f))


def test_gradient_and_parseval():
    f = torch.fft.fftfreq(128,d=1/64e9,dtype=torch.float64)
    p = torch.tensor([0.2,0.7,0.0,0.0],dtype=torch.float64,requires_grad=True)
    h = chromatic_dispersion(f)
    target = torch.exp(-2j*math.pi*f*8/64e9)
    assert torch.autograd.gradcheck(lambda x: fit_response(x,f,h,target).abs().square().mean(), (p,))
    residual = fit_response(p,f,h,target)
    spectrum = residual.abs().square().mean()
    waveform = torch.fft.ifft(residual,norm='ortho').abs().square().mean()
    torch.testing.assert_close(spectrum,waveform,atol=1e-13,rtol=1e-13)
    gs = torch.autograd.grad(spectrum,p,retain_graph=True)[0]
    gw = torch.autograd.grad(waveform,p)[0]
    torch.testing.assert_close(gs,gw,atol=1e-12,rtol=1e-12)
