
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 重新加载数据
profiles = pd.read_csv('/mnt/agents/upload/Ocean_Oxygen_Sensitivity_profiles.csv')

print("Regenerating Figure 2: Stepwise Extinction Cumulative Curve")

# 功能群定义
thresholds = {
    'Picophytoplankton': 5.0,
    'Nanophytoplankton': 12.0,
    'Microzooplankton': 22.0,
    'Mesozooplankton': 35.0,
    'Small Fish': 50.0,
    'Large Fish': 80.0,
    'Benthos': 55.0,
}

# 按阈值排序（从高到低）
sorted_groups = sorted(thresholds.items(), key=lambda x: x[1], reverse=True)

# 计算累积灭绝曲线
o2_range = np.arange(0, 250, 1)
cumulative_extinct = []

for o2_val in o2_range:
    n_extinct = 0
    for group, thresh in thresholds.items():
        if o2_val < thresh:
            n_extinct += 1
    cumulative_extinct.append(n_extinct)

cumulative_extinct = np.array(cumulative_extinct)

# 找到breakpoints
jumps = np.where(np.diff(cumulative_extinct) != 0)[0]

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(o2_range, cumulative_extinct, 'b-', linewidth=2.5, label='Cumulative extinct groups')
ax.scatter([o2_range[j] for j in jumps], [cumulative_extinct[j] for j in jumps], 
           c='red', s=120, zorder=5, edgecolors='black', linewidth=1.5, label='Breakpoints')

for idx in jumps:
    ax.axvline(x=o2_range[idx], color='gray', linestyle='--', alpha=0.4)
    ax.text(o2_range[idx], cumulative_extinct[idx]+0.3, f'{o2_range[idx]:.0f}', 
            fontsize=10, ha='center', color='red', fontweight='bold')

ax.set_xlabel('O2 (μmol/kg)', fontsize=13)
ax.set_ylabel('Number of Extinct Functional Groups', fontsize=13)
ax.set_title('Stepwise Extinction: Cumulative Functional Group Loss vs Oxygen', fontsize=15, fontweight='bold')
ax.set_xlim(0, 150)
ax.set_ylim(-0.5, 7.5)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11, loc='upper left')

plt.tight_layout()
plt.savefig('/mnt/agents/output/FigS2_Stepwise_Extinction.png', dpi=300, bbox_inches='tight')
plt.show()
print("✓ Fig S2 saved")
