import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from utils import (
    inject_css, style_ax, analyser_gpx,
    CHART_LINE_ASCENT, CHART_LINE_DESCENT,
    CHART_FILL_ASCENT, CHART_FILL_DESCENT, CHART_HIGHLIGHT
)


def render():
    inject_css()

    st.markdown("# Analyse du parcours GPX")
    st.markdown('<p class="section-label">Importez le fichier GPX de votre prochaine course</p>', unsafe_allow_html=True)
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Importer le fichier GPX de votre prochaine course", type=['gpx'])

    if uploaded_file is not None:
        analyse = analyser_gpx(uploaded_file)

        if analyse:
            st.session_state['analyse'] = analyse

            st.markdown('<p class="section-label">Statistiques du parcours</p>', unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            stats = [
                (col1, "Distance", f"{analyse['distance_totale_km']:.2f}", "km"),
                (col2, "Altitude min", f"{analyse['altitude_min_m']:.0f}", "m"),
                (col3, "Altitude max", f"{analyse['altitude_max_m']:.0f}", "m"),
                (col4, "D+", f"{analyse['D_plus_m']:.0f}", "m"),
            ]
            for col, label, value, unit in stats:
                with col:
                    st.markdown(f"""
                    <div class="stat-card">
                      <span class="stat-label">{label}</span>
                      <span class="stat-value">{value} <span class="stat-unit">{unit}</span></span>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

            # --- Graphique montées ---
            st.markdown('<p class="section-label">Profil d\'altitude \u2014 mont\u00e9es</p>', unsafe_allow_html=True)
            df = analyse['df']
            fig, ax = plt.subplots(figsize=(11, 3.5))
            style_ax(ax, fig)

            y_min_data, y_max_data = df['elevation'].min(), df['elevation'].max()
            data_range = y_max_data - y_min_data if y_max_data != y_min_data else 100
            total_dist = df['cum_distance'].iloc[-1]
            label_offset = data_range * 0.08
            min_gap_x = total_dist * 0.07
            min_gap_y = data_range * 0.10

            cote_labels = []
            for cote in analyse['cotes']:
                mid = (cote['start_km'] + cote['end_km']) / 2
                mask = (df['cum_distance'] >= cote['start_km']) & (df['cum_distance'] <= cote['end_km'])
                max_elev = df.loc[mask, 'elevation'].max()
                cote_labels.append((cote, mid, max_elev + label_offset))

            for i in range(1, len(cote_labels)):
                cote_i, x_i, y_i = cote_labels[i]
                for j in range(i):
                    _, x_j, y_j = cote_labels[j]
                    if abs(x_i - x_j) < min_gap_x and abs(y_i - y_j) < min_gap_y:
                        y_i = y_j + min_gap_y
                        cote_labels[i] = (cote_i, x_i, y_i)

            max_y_label = max((y for _, _, y in cote_labels), default=y_max_data)
            y_top = max_y_label + data_range * 0.15
            y_bottom = y_min_data - data_range * 0.05
            ax.set_ylim(y_bottom, y_top)
            ax.fill_between(df['cum_distance'], df['elevation'], y_bottom, color=CHART_FILL_ASCENT, alpha=0.06)

            for cote, mid, y_label in cote_labels:
                mask = (df['cum_distance'] >= cote['start_km']) & (df['cum_distance'] <= cote['end_km'])
                df_section = df[mask]
                if not df_section.empty:
                    ax.fill_between(df_section['cum_distance'], df_section['elevation'], y_bottom,
                                    color=CHART_HIGHLIGHT, alpha=0.15)

            ax.plot(df['cum_distance'], df['elevation'], color=CHART_LINE_ASCENT, linewidth=1.5)
            ax.xaxis.set_major_locator(MultipleLocator(1))
            ax.set_xlim(0, total_dist)
            ax.set_xlabel("Distance (km)", fontsize=10)
            ax.set_ylabel("Altitude (m)", fontsize=10)

            for cote, mid, y_label in cote_labels:
                ax.text(mid, y_label, f"{cote['pente_pct']}%",
                        ha='center', va='bottom', color=CHART_HIGHLIGHT,
                        fontsize=8.5, fontweight='bold', zorder=6)

            fig.tight_layout()
            st.pyplot(fig)

            # --- Tableau des côtes ---
            if analyse['cotes']:
                st.markdown('<p class="section-label">Mont\u00e9es &gt; 200 m</p>', unsafe_allow_html=True)
                cotes_df = pd.DataFrame(analyse['cotes'])
                cotes_df = cotes_df[['start_km', 'end_km', 'longueur_km', 'pente_pct']]
                cotes_df = cotes_df.round({'start_km': 1, 'end_km': 1, 'longueur_km': 1})
                cotes_df.index = range(1, len(cotes_df) + 1)
                cotes_df.rename(columns={
                    'start_km': 'D\u00e9but (km)', 'end_km': 'Fin (km)',
                    'longueur_km': 'Longueur (km)', 'pente_pct': 'Pente (%)'
                }, inplace=True)
                st.dataframe(cotes_df, use_container_width=True, column_config={
                    'Pente (%)': st.column_config.NumberColumn(format="%.1f %%")
                })

            # --- Graphique descentes ---
            if analyse['descentes']:
                st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
                st.markdown('<p class="section-label">Profil d\'altitude \u2014 descentes</p>', unsafe_allow_html=True)
                fig3, ax3 = plt.subplots(figsize=(11, 3.5))
                style_ax(ax3, fig3)

                y_min_d, y_max_d = df['elevation'].min(), df['elevation'].max()
                data_range_d = y_max_d - y_min_d if y_max_d != y_min_d else 100
                total_dist_d = df['cum_distance'].iloc[-1]
                label_offset_d = data_range_d * 0.08
                min_gap_x_d = total_dist_d * 0.07
                min_gap_y_d = data_range_d * 0.10

                desc_labels = []
                for desc in analyse['descentes']:
                    mid = (desc['start_km'] + desc['end_km']) / 2
                    mask = (df['cum_distance'] >= desc['start_km']) & (df['cum_distance'] <= desc['end_km'])
                    max_elev = df.loc[mask, 'elevation'].max()
                    desc_labels.append((desc, mid, max_elev + label_offset_d))

                for i in range(1, len(desc_labels)):
                    desc_i, x_i, y_i = desc_labels[i]
                    for j in range(i):
                        _, x_j, y_j = desc_labels[j]
                        if abs(x_i - x_j) < min_gap_x_d and abs(y_i - y_j) < min_gap_y_d:
                            y_i = y_j + min_gap_y_d
                            desc_labels[i] = (desc_i, x_i, y_i)

                max_y_label_d = max((y for _, _, y in desc_labels), default=y_max_d)
                y_top_d = max_y_label_d + data_range_d * 0.15
                y_bottom_d = y_min_d - data_range_d * 0.05
                ax3.set_ylim(y_bottom_d, y_top_d)
                ax3.fill_between(df['cum_distance'], df['elevation'], y_bottom_d, color=CHART_FILL_DESCENT, alpha=0.06)

                for desc, mid, y_label in desc_labels:
                    mask = (df['cum_distance'] >= desc['start_km']) & (df['cum_distance'] <= desc['end_km'])
                    df_section = df[mask]
                    if not df_section.empty:
                        ax3.fill_between(df_section['cum_distance'], df_section['elevation'], y_bottom_d,
                                         color=CHART_LINE_DESCENT, alpha=0.15)

                ax3.plot(df['cum_distance'], df['elevation'], color=CHART_LINE_DESCENT, linewidth=1.5)
                ax3.xaxis.set_major_locator(MultipleLocator(1))
                ax3.set_xlim(0, total_dist_d)
                ax3.set_xlabel("Distance (km)", fontsize=10)
                ax3.set_ylabel("Altitude (m)", fontsize=10)

                for desc, mid, y_label in desc_labels:
                    ax3.text(mid, y_label, f"({desc['pente_pct']})%",
                             ha='center', va='bottom', color=CHART_LINE_DESCENT,
                             fontsize=8.5, fontweight='bold', zorder=6)

                fig3.tight_layout()
                st.pyplot(fig3)

                st.markdown('<p class="section-label">Descentes &gt; 200 m</p>', unsafe_allow_html=True)
                desc_df = pd.DataFrame(analyse['descentes'])
                desc_df = desc_df[['start_km', 'end_km', 'longueur_km', 'pente_pct']]
                desc_df = desc_df.round({'start_km': 1, 'end_km': 1, 'longueur_km': 1})
                desc_df.index = range(1, len(desc_df) + 1)
                desc_df.rename(columns={
                    'start_km': 'D\u00e9but (km)', 'end_km': 'Fin (km)',
                    'longueur_km': 'Longueur (km)', 'pente_pct': 'Pente (%)'
                }, inplace=True)
                st.dataframe(desc_df, use_container_width=True, column_config={
                    'Pente (%)': st.column_config.NumberColumn(format="(%.1f) %%")
                })

        else:
            st.error("Impossible d'analyser le fichier GPX.")
