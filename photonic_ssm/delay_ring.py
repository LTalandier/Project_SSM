"""Exact passive single-bus ring cascade, evaluated in continuous frequency.

A unit z delay denotes a round trip, not an arbitrary symbol interval.
This is an all-pass cascade topology, not the coupled-ring CROW from P1.
"""
import math
import torch


def ring_cascade(f_hz, phase, coupling, *, fsr_hz=100e9,
                 loss_db_cm=0.051, radius_um=242.2002619):
    a = 10 ** (-loss_db_cm * 2 * math.pi * radius_um * 1e-4 / 20)
    t = torch.sqrt(1 - coupling)
    q = a * torch.exp(1j * (phase[:, None] - 2 * math.pi * f_hz[None, :] / fsr_hz))
    return ((t[:, None] - q) / (1 - t[:, None] * q)).prod(dim=0)


def decode_controls(parameters):
    n = parameters.numel() // 2
    return parameters[:n], 0.05 + 0.15 * torch.sigmoid(parameters[n:])


def chromatic_dispersion(f_hz, length_km=20.0):
    # 17 ps/(nm km) = 17e-6 s/m^2; beta2 = -D lambda^2/(2 pi c).
    beta2 = -17e-6 * (1550e-9) ** 2 / (2 * math.pi * 299792458)
    return torch.exp(-0.5j * beta2 * length_km * 1000 * (2 * math.pi * f_hz) ** 2)


def fit_response(parameters, f_hz, channel, target):
    phase, coupling = decode_controls(parameters)
    response = ring_cascade(f_hz, phase, coupling) * channel
    scalar = (response.conj() * target).mean() / response.abs().square().mean()
    return scalar * response - target
