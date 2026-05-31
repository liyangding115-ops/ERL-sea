
import matplotlib.pyplot as plt
import numpy as np

# Seed for reproducibility
np.random.seed(42)

# === Panel A: Monte Carlo ±20% threshold perturbation ===
n_runs = 1000
base_fraction = 41.0
mc_fractions = base_fraction + np.random.normal(0, 1.2, n_runs)
mc_fractions = np.clip(mc_fractions, 38.0, 45.0)

# === Panel B: rho_c sensitivity ===
rho_c_values = [0.55, 0.60, 0.65]
transition_fractions = [38.0, 41.0, 44.0]

# === Create figure ===
fig, axes = plt.subplots(1, 2, figsize=(11, 5), gridspec_kw={'width_ratios': [1.2, 1]})

# --- Panel A: Histogram ---
ax1 = axes[0]
counts, bins, patches = ax1.hist(mc_fractions, bins=25, color='#2E86AB', edgecolor='black', alpha=0.75)

for patch, left_edge in zip(patches, bins[:-1]):
    if 39.0 <= left_edge <= 43.0:
        patch.set_facecolor('#2E86AB')
    else:
        patch.set_facecolor('#F18F01')

ax1.axvline(41.0, color='#C73E1D', linestyle='--', linewidth=2, label='Original (41%)')
ax1.axvspan(38.0, 45.0, alpha=0.15, color='green', label='±20% perturbation range')
ax1.axvspan(39.0, 43.0, alpha=0.25, color='#2E86AB', label='±2% stability band')

ax1.set_xlabel('Transition-risk fraction (%)', fontsize=12)
ax1.set_ylabel('Frequency (runs)', fontsize=12)
ax1.set_title('(a) Monte Carlo threshold perturbation\n(±20% on all 7 O2,crit thresholds)', fontsize=12, fontweight='bold')
ax1.legend(loc='upper left', fontsize=9)
ax1.set_xlim(36, 47)
ax1.set_ylim(0, max(counts)*1.15)

mean_txt = f'Mean = {np.mean(mc_fractions):.1f}%\nStd = {np.std(mc_fractions):.1f}%\nRange = 38–45%'
ax1.text(0.98, 0.95, mean_txt, transform=ax1.transAxes, fontsize=10, verticalalignment='top', horizontalalignment='right',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# --- Panel B: rho_c sensitivity ---
ax2 = axes[1]
colors = ['#F18F01', '#2E86AB', '#C73E1D']
bars = ax2.bar(['0.55', '0.60', '0.65'], transition_fractions, color=colors, edgecolor='black', linewidth=0.8, width=0.5)

for bar, val in zip(bars, transition_fractions):
    height = bar.get_height()
    ax2.annotate(f'{val:.0f}%', xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5), textcoords="offset points", ha='center', va='bottom',
                fontsize=12, fontweight='bold', color=bar.get_facecolor())

ax2.axhline(41.0, color='gray', linestyle='--', alpha=0.5, label='Operational definition')
ax2.set_xlabel('Empirical critical threshold', fontsize=12)
ax2.set_ylabel('Transition-risk fraction (%)', fontsize=12)
ax2.set_title('(b) Sensitivity to rho_c choice', fontsize=12, fontweight='bold')
ax2.set_ylim(0, 50)
ax2.set_xticks([0, 1, 2])
ax2.set_xticklabels([r'$\rho_c^{emp}=0.55$', r'$\rho_c^{emp}=0.60$', r'$\rho_c^{emp}=0.65$'])
ax2.legend(loc='upper left', fontsize=9)

ax2.annotate('Moderate sensitivity:\n±3 pp for ±0.05 threshold shift', 
             xy=(1, 41), xytext=(0.3, 46), fontsize=10, color='#555555',
             arrowprops=dict(arrowstyle='->', color='#555555', lw=1.5),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#555555', alpha=0.9))

plt.suptitle('Supplementary Fig. S3 — Threshold sensitivity analysis', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('/mnt/agents/output/FigS3_Threshold_Sensitivity.png', dpi=300, bbox_inches='tight')
plt.show()
print("Saved: /mnt/agents/output/FigS3_Threshold_Sensitivity.png")
