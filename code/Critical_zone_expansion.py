import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# 加载WOA23数据
file_path = '/mnt/agents/upload/woa23_all_o00an01.csv'

with open(file_path, 'r') as f:
    lines = f.readlines()

header_line = lines[1].strip()
depth_part = header_line.split('(M):')[1]
depths = [float(d.strip()) for d in depth_part.split(',') if d.strip()]
n_depths = len(depths)

data_rows = []
for line in lines[2:]:
    line = line.strip()
    if not line:
        continue
    parts = line.split(',')
    if len(parts) < 2 + n_depths:
        continue
    lat = float(parts[0])
    lon = float(parts[1])
    o2_values = []
    valid = False
    for p in parts[2:2+n_depths]:
        p = p.strip()
        if p == '':
            o2_values.append(np.nan)
        else:
            try:
                v = float(p)
                o2_values.append(v)
                valid = True
            except:
                o2_values.append(np.nan)
    if valid:
        data_rows.append([lat, lon] + o2_values)

o2_cols = [f'o2_{int(d)}m' for d in depths]
cols = ['lat', 'lon'] + o2_cols
df = pd.DataFrame(data_rows, columns=cols)

# 定义情景
scenarios = {
    'Baseline (2023)': 1.0,
    'Uniform O₂ decline -10%': 0.9,
    'Uniform O₂ decline -20%': 0.8,
}

colors = {
    'Baseline (2023)': '#2E86AB',
    'Uniform O₂ decline -10%': '#F18F01',
    'Uniform O₂ decline -20%': '#C73E1D',
}

scenario_labels = {
    'Baseline (2023)': 'Present-day (2023)',
    'Uniform O₂ decline -10%': 'Uniform −10% O₂',
    'Uniform O₂ decline -20%': 'Uniform −20% O₂',
}

# 重新计算四个纯O₂浓度指标
results_o2_only = []

for scen_name, factor in scenarios.items():
    o2_matrix = df[o2_cols].values * factor
    deep_mask = np.array([depths[j] > 200 for j in range(len(depths))])
    
    o2_deep = o2_matrix[:, deep_mask]
    valid_deep = ~np.isnan(o2_deep)
    total_deep_cells = np.sum(valid_deep)
    
    critical = np.sum((o2_deep < 10) & valid_deep) / total_deep_cells * 100
    severe = np.sum((o2_deep < 20) & valid_deep) / total_deep_cells * 100
    omz = np.sum((o2_deep < 45) & valid_deep) / total_deep_cells * 100
    transition = np.sum((o2_deep >= 40) & (o2_deep <= 80) & valid_deep) / total_deep_cells * 100
    
    results_o2_only.append({
        'Scenario': scen_name,
        'Critical_hypoxia_pct': critical,
        'Severe_hypoxia_pct': severe,
        'OMZ_pct': omz,
        'Transition_risk_pct': transition,
    })

res_o2_df = pd.DataFrame(results_o2_only)
print("统一O₂浓度指标结果（depth > 200m，按浓度排序）:")
print(res_o2_df.to_string(index=False))

# ── 按浓度阈值从低到高排列: 10 → 20 → 45 → 40-80 ──
fig, ax = plt.subplots(figsize=(10, 7))

# 按浓度顺序: <10, <20, <45, 40-80
metrics = ['Critical_hypoxia_pct', 'Severe_hypoxia_pct', 'OMZ_pct', 'Transition_risk_pct']
metric_labels = [
    'Critical hypoxia\n(O₂ < 10 μM)',
    'Severe hypoxia\n(O₂ < 20 μM)',
    'OMZ\n(O₂ < 45 μM)',
    'Transition risk\n(O₂ 40–80 μM)'
]

x = np.arange(len(metrics))
width = 0.25

for i, scen_name in enumerate(scenarios.keys()):
    vals = [res_o2_df[res_o2_df['Scenario']==scen_name][m].values[0] for m in metrics]
    bars = ax.bar(x + i*width, vals, width, label=scenario_labels[scen_name], 
                  color=colors[scen_name], edgecolor='black', linewidth=0.8, zorder=3)
    for j, v in enumerate(vals):
        ax.text(x[j] + i*width, v + 0.15, f'{v:.2f}%', ha='center', va='bottom', 
               fontsize=9, fontweight='bold', color=colors[scen_name])

# 相对变化标注
baseline_vals = [res_o2_df[res_o2_df['Scenario']=='Baseline (2023)'][m].values[0] for m in metrics]
end_vals = [res_o2_df[res_o2_df['Scenario']=='Uniform O₂ decline -20%'][m].values[0] for m in metrics]

for j, (bv, ev) in enumerate(zip(baseline_vals, end_vals)):
    if bv > 0:
        pct_change = (ev - bv) / bv * 100
        ax.annotate(f'+{pct_change:.0f}%', 
                   xy=(x[j] + 2*width + 0.08, ev + 0.6), 
                   fontsize=11, color='#C73E1D', fontweight='bold', 
                   ha='left', va='bottom',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#C73E1D', alpha=0.9))

ax.set_ylabel('Fraction of deep-ocean volume (%)', fontsize=13)
ax.set_title('Critical-zone expansion under deoxygenation scenarios', 
            fontsize=15, fontweight='bold', loc='left', pad=15)
ax.set_xticks(x + width)
ax.set_xticklabels(metric_labels, fontsize=11)
ax.legend(fontsize=11, loc='upper left', frameon=True, fancybox=True, shadow=True)
ax.grid(True, alpha=0.3, axis='y', zorder=0)
ax.set_ylim(0, max(end_vals) * 1.4)

ax.text(0.98, 0.02, 
       'Depth > 200 m | WOA23 climatology\nUniform O₂ decline scenarios', 
       transform=ax.transAxes, fontsize=9, ha='right', va='bottom',
       style='italic', color='gray')

plt.tight_layout()

output_path = '/mnt/agents/output/Fig_Critical_zone_expansion_v4.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

print(f"\n✅ 浓度顺序排列版已保存: {output_path}")