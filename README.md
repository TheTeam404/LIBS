# LIBS
Best LIBS Software in the world
Initialization:

Load the spectral data (wavelengths W, intensities I).
Load the list of detected peak centers P = {p1, p2, ..., pn}.
Iterate Through Peaks: For each peak center p in P:
a.  Define Region of Interest (ROI):
* Determine a wavelength window around p. This needs to be wide enough to capture the peak wings and some baseline but narrow enough to avoid excessive overlap with adjacent peaks (this is a critical parameter). A common approach is p ± k * FWHM_est, where FWHM_est is an initial rough estimate of the peak's width (perhaps from the peak detection step) and k is a factor (e.g., 5 to 10).
* Select the data points (W_roi, I_roi) within this window.
b.  Local Baseline Correction:
* Estimate and subtract the baseline from I_roi to get baseline-corrected intensities I_corr. Methods include:
* Fitting a low-order polynomial to the edges of the ROI.
* Using algorithms like SNIP (Statistics-sensitive Non-linear Iterative Peak-clipping).
* Accurate baseline correction is crucial here.
c.  Estimate Initial Parameters:
* From I_corr, estimate initial guesses for:
* Amplitude (A_guess): Max value of I_corr.
* Center (p_guess): Wavelength corresponding to max I_corr (can refine the initial p).
* Width (w_guess): Estimate FWHM from I_corr.
d.  Perform Fits: Fit the I_corr data within the ROI using non-linear least squares fitting for each profile:
* Fit 1: Gaussian: G(w; A_g, p_g, σ_g)
* Fit 2: Lorentzian: L(w; A_l, p_l, γ_l)
* Fit 3: Pseudo-Voigt: PV(w; A_pv, p_pv, FWHM_pv, η_pv) (where η is the mixing parameter, often 0 for Gaussian, 1 for Lorentzian). Alternatively, use a true Voigt function if your library supports it and computation time allows.
* Crucial: Ensure your fitting routine uses the initial guesses and potentially constraints (e.g., center must be near p, width must be positive) to aid convergence. Store the fitted parameters for each successful fit.
e.  Calculate Goodness-of-Fit Metrics: For each successful fit, calculate metrics that evaluate fit quality and penalize complexity. Good choices include:
* Akaike Information Criterion (AIC): Balances goodness of fit (likelihood) with the number of parameters. Lower AIC is better. AIC = 2k - 2ln(L) where k is number of parameters, L is maximized likelihood (often approximated using residual sum of squares: AIC ≈ n*ln(RSS/n) + 2k).
* Bayesian Information Criterion (BIC): Similar to AIC but penalizes complexity more heavily, especially for larger datasets. Lower BIC is better. BIC = k*ln(n) - 2ln(L) (or BIC ≈ n*ln(RSS/n) + k*ln(n)).
* You can also calculate R-squared or Reduced Chi-squared, but AIC/BIC are often preferred for model selection.
f.  Select Best Model:
* Compare the AIC (or BIC) values calculated for the Gaussian, Lorentzian, and Pseudo-Voigt fits.
* The function that yields the lowest AIC (or BIC) value is generally considered the best model for that peak, balancing fit quality with model simplicity.
* Store the chosen model type ("Gaussian", "Lorentzian", "Pseudo-Voigt") and its corresponding fitted parameters for peak p.
g.  Quality Control (Optional but Recommended):
* Check if the chosen fit meets minimum quality standards (e.g., R-squared > 0.95, acceptable residual pattern).
* Check for signs of asymmetry (e.g., calculate skewness of the peak data or residuals).
* Add flags to the output indicating potential issues like "Poor Fit Quality", "Asymmetry Detected", or "Convergence Failure".

Output: Return a data structure (e.g., a list of dictionaries or a table) containing, for each input peak p:

The original peak center p.
The chosen best fit function type.
The parameters of the chosen fit (Amplitude, Center, Width(s), Mixing parameter if applicable).
Goodness-of-fit metrics (AIC/BIC, R², etc.).
Any quality flags.
Alternative Strategy (Parameter-Based Heuristic):

Fit only a Pseudo-Voigt function initially.
Examine the fitted mixing parameter (η).
If η is very close to 0 (e.g., < 0.1), tentatively classify as Gaussian.
If η is very close to 1 (e.g., > 0.9), tentatively classify as Lorentzian.
Otherwise, classify as Pseudo-Voigt.
(Optional) Re-fit with the simpler model (G or L) if classified as such, and use AIC/BIC to confirm if the simpler model is statistically justified compared to the original Pseudo-Voigt fit.
Pro: Faster (fewer fits). Con: Relies heavily on the robustness of the Pseudo-Voigt fit and the chosen thresholds for η.

Important Considerations for Implementation:

Robust Fitting: Use reliable non-linear least-squares fitting libraries (e.g., scipy.optimize.curve_fit in Python, ensuring good initial parameter estimates).
Handling Overlap: This algorithm works best for relatively isolated peaks. Significant overlap requires simultaneous multi-peak fitting within a shared ROI, which is considerably more complex to automate reliably. You might need a separate step to identify regions requiring multi-peak fits.
Parameter Tuning: The ROI size (k factor) and baseline method significantly impact results. These may need tuning based on your specific spectrometer and data characteristics.
Computational Cost: Fitting 3 functions per peak can be time-consuming for spectra with thousands of peaks.
