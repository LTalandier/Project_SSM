# P1 source refresh — 2026-09-13

Performed in the main session while the registered correction rerun executes.
These reads update citation evidence, not frozen numerical experiment inputs.
No independent reviewer or exhaustive novelty guarantee is claimed.

## Registered page checks

- **Zhang et al., eLight 6:6:** [full text, arXiv v6](https://arxiv.org/html/2505.11369),
  §2.4, explicitly uses PSO to tune ten MRR currents and one bias. The recurrent
  mode has electrical feedback. This does not demonstrate gradient-based training
  of a coupled-resonator memory lattice. The same section reports 0.1 ms heater
  response and about 3 ms FPGA control latency; these are another device's values,
  not timings assigned to our unbuilt hardware.
- **Ashtiani et al.:** [author manuscript](https://arxiv.org/html/2506.14575),
  Fig. 3 describes input, hidden, and output layers with a backward error path.
  It supports the layered-network distinction in §1; no trained recurrent state
  lattice is demonstrated there. Publisher record: [Nature article](https://www.nature.com/articles/s41586-026-10262-8).
- **Van Assche et al.:** [published article](https://www.nature.com/articles/s41566-026-01968-2),
  published 21 July 2026, Nature Photonics 20, 1062–1069. The readout is programmable;
  the reservoir is fixed. The [author manuscript methods](https://arxiv.org/html/2503.19911)
  explicitly optimize readout weights with CMA-ES. Citation metadata now includes
  authors and the final DOI; the recurrence-training boundary remains unchanged.
- **Rukh et al.:** [Table 2](https://arxiv.org/html/2511.02198) confirms doublet
  separations of 180–210 MHz for the polymer-mask rows and 230–320 MHz for metal-mask
  rows. These are separations, not directly the off-diagonal rate γ.
- **Dacha et al.:** [results around Fig. 2](https://arxiv.org/html/2506.21692) confirm
  24-hour recording, 341 MHz free-running standard deviation, and loaded Q near
  3 million. The conversion into our random-walk schedule is a model assumption;
  it does not measure independent per-ring drift in our lattice. Publisher DOI:
  [10.1038/s41566-025-01789-9](https://www.nature.com/articles/s41566-025-01789-9).

## Exclusions-ledger rechecks

- [Red Pitaya original STEMlab 125-14 specifications](https://redpitaya.readthedocs.io/en/latest/developerGuide/hardware/ORIG_GEN/125-14/top.html):
  5 V, 2 A maximum draw verifies the 10 W bound for the original board, not Gen 2.
- [TOPTICA DigiLock manual](https://www.toptica.com/fileadmin/Editors_English/03_products/03_tunable_diode_lasers/04_control_electronics/02_laser_locking_electronics/04_DigiLock_110/toptica_digilock_manual.pdf),
  PDF page 73: +15 V at 700 mA max and −15 V at 200 mA max. Their sum gives a
  **derived 13.5 W rail-power bound**, not measured typical consumption.
- [ST STM32F407/417 product page](https://www.st.com/en/microcontrollers-microprocessors/stm32f407-417.html):
  238 µA/MHz at 168 MHz is stated as a low-current operating point. Multiplication
  by 3.3 V gives 0.132 W. Calling this an upper bound was incorrect; it is an
  operating-point estimate, not a worst-case controller budget. No frozen input changes.
- [CORNERSTONE platform page](https://cornerstone.sotonfab.co.uk/mpw/technology-platforms/):
  <10 dB/grating for 300 nm SiN, TE at 1.55 µm. Correct the ledger's 1.57 µm label.
- [Zeng et al., Optics Letters 50, 3768–3771](https://opg.optica.org/ol/abstract.cfm?uri=ol-50-11-3768):
  abstract reports 0.98 mW/π for a suspended ten-fold phase shifter. This verifies
  the approximately 1 mW/π class, not compatibility with a particular foundry ring.
- [LIGENTEC press release, 16 September 2024](https://www.ligentec.com/wp-content/uploads/2024/09/202401609-Press-release-Standardized-low-loss-fiber-array-to-PIC-interface-demonstrated-with-Photonic-Wire-bonds-.pdf):
  manufacturer reports total insertion loss below 1.5 dB for its demonstrated
  photonic-wire-bond interface. Preserve the manufacturer's scope.
- [TEC Microsystems 1ML06-017-03 datasheet](https://www.tec-microsystems.com/Download/Datasheets/Thermoelectric%20Coolers/1ML06/1ML06-017-03_Datasheet_Standard_2022.pdf),
  PDF page 2: Qmax=5.8 W at 27°C in vacuum. This is cooling capacity, not electrical
  holding consumption; it does not source the 0.18 W holding assumption.
- **TTX1995:** the exact current manufacturer-hosted 2.0 W/3.0 W datasheet was not
  retrieved. Keep this non-load-bearing cross-check unverified and exclude it from
  the manuscript's quantitative support; do not promote secondary-host snippets.

## Search refresh and scope

Searches performed: continuous-time resonator in-situ recurrent training (2026);
photonic coupled-resonator poles/couplings trained by gradients (2026); updated
Zhang/Van Assche/Ashtiani records; and D-LinOSS venue record. The results retained
known nearest neighbors (PSO MRR neuron, fixed reservoir with trained readout,
layered optical backprop, and time-synthetic networks). No new demonstrated
coupled-resonator memory lattice satisfying the complete PR-15 criterion was
identified in this bounded refresh. That is an absence-of-found-evidence result,
not proof of priority. D-LinOSS remains cited as its arXiv preprint: the OpenReview
forum was browser-challenged, so no venue claim was inferred.

The PR-20 negative inline result and the withdrawn total-training-energy claim
are unaffected by these citation edits. This refresh is dated; if submission is
materially delayed, repeat the novelty search then.
