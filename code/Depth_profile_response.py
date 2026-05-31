# ── FIGURE 2: Depth-profile structural response (原 Panel a) ──

# 从保存的 profiles CSV 加载深度剖面
prof_df = pd.read_csv('/mnt/agents/output/Ocean_Oxygen_Sensitivity_profiles.csv')

fig, ax = plt.subplots(figsize=(9, 7))

for scen_name in scenarios.keys():
    prof = prof_df[prof_df['Scenario'] == scen_name]
    ax.plot(prof['rho_d'], prof['Depth_m'], color=colors[scen_name], 
           linewidth=2.5, label=scenario_labels[scen_name])

# 关键阈值线
ax.axvline(x=0.60, color='black', linestyle='--', linewidth=1.5, alpha=0.7, 
          label=r'$\rho_c^{emp} = 0.60$')
ax.axvline(x=0.30, color='gray', linestyle=':', linewidth=1.5, alpha=0.7, 
          label='Simplification threshold')

ax.invert_yaxis()
ax.set_xlabel(r'$\rho_d = \sigma\sqrt{SC}$', fontsize=13)
ax.set_ylabel('Depth (m)', fontsize=13)
ax.set_title('Depth-profile structural response to uniform O₂ decline', 
            fontsize=15, fontweight='bold', loc='left', pad=15)
ax.legend(loc='lower left', fontsize=10, frameon=True, fancybox=True, shadow=True)
ax.set_xlim(0.45, 0.92)
ax.grid(True, alpha=0.3)

# 添加深度区域标注
ax.axhspan(0, 200, alpha=0.08, color='blue')
ax.axhspan(200, 1000, alpha=0.05, color='green')
ax.axhspan(1000, 5500, alpha=0.08, color='purple')
ax.text(0.46, 100, 'Surface\n(0–200 m)', fontsize=9, color='blue', alpha=0.7, fontweight='bold')
ax.text(0.46, 500, 'Mesopelagic\n(200–1000 m)', fontsize=9, color='green', alpha=0.7, fontweight='bold')
ax.text(0.46, 3000, 'Bathypelagic\n(>1000 m)', fontsize=9, color='purple', alpha=0.7, fontweight='bold')

plt.tight_layout()
panel_a_path = '/mnt/agents/output/Fig_Depth_profile_response.png'
plt.savefig(panel_a_path, dpi=300, bbox_inches='tight', facecolor='white')
plt.show()
print(f"✅ Depth-profile figure saved: {panel_a_path}")