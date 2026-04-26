# Visualização de KPIs
import streamlit as st
import matplotlib.pyplot as plt

def plot_bar_with_labels(df, x, y, title, ylabel='Taxa', ylim_pad=0.01, rotate_x=False):
    fig, ax = plt.subplots(figsize=(8,4))
    if df.empty or y not in df.columns:
        st.warning(f"Não há dados para plotar '{title}'")
        ax.set_title(title)
        st.pyplot(fig)
        return

    df = df.sort_values(y, ascending=False)
    bars = ax.bar(df[x].astype(str), df[y])
    min_y = df[y].min()
    max_y = df[y].max()
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_ylim(max(0, min_y - ylim_pad), max_y + ylim_pad)
    if rotate_x:
        plt.xticks(rotation=30, ha='right')
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + (ylim_pad/2 if ylim_pad>0 else 0.005), f"{height:.3f}", ha='center', fontsize=9)
    st.pyplot(fig)