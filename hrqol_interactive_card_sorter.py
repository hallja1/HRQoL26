# HRQoL Domain Sorting – Streamlit App
# Save as: hrqol_sorter.py
# Run with: streamlit run hrqol_sorter.py

import streamlit as st
import pandas as pd

st.set_page_config(page_title="HRQoL Domain Sorting", layout="wide")

DOMAINS = [
"Other please state:",
"Vitality",
"Insecurity",
"Role limitations due to emotional problems",
"Emotional well-being",
"Self-care",
"Energy/fatigue",
"General health",
"Fear",
"Role limitations due to physical health",
"Anxiety / Depression",
"Discomfort",
"Usual activities",
"Pain",
"Physical functioning",
"Social functioning",
"Mobility",
"Depression",
"Anxiety",
]

DEFAULT_GROUPS = [
"Domain bank",
"High priority",
"Low priority",
"Unnecessary"
]

if "assignments" not in st.session_state:
    st.session_state.assignments = {d: "Domain bank" for d in DOMAINS}

if "groups" not in st.session_state:
    st.session_state.groups = DEFAULT_GROUPS.copy()

st.title("HRQoL Domain Sorting Exercise")

st.markdown("""
Use this interface during workshops to sort HRQoL domains into priority categories.
You can also specify how many levels should be used when defining each domain in a future measure.
""")

st.divider()

st.subheader("Measurement design")

levels = st.number_input(
"How many levels should each domain have? (same for all domains)",
min_value=2,
max_value=10,
value=5,
step=1
)

st.caption("Example: EQ‑5D uses 5 levels.")

st.divider()

st.subheader("Sort domains into categories")

cols = st.columns(len(st.session_state.groups))

for col, group in zip(cols, st.session_state.groups):
    with col:
        st.markdown(f"### {group}")

        group_domains = [d for d, g in st.session_state.assignments.items() if g == group]

        for domain in group_domains:
            new_group = st.selectbox(
                domain,
                st.session_state.groups,
                index=st.session_state.groups.index(group),
                key=f"move_{domain}"
            )

            if new_group != group:
                st.session_state.assignments[domain] = new_group
                st.rerun()

st.divider()

st.subheader("Results preview")

results = []
for domain, group in st.session_state.assignments.items():
    results.append({
        "Domain": domain,
        "Category": group,
        "Levels": levels
    })

results_df = pd.DataFrame(results)

st.dataframe(results_df, use_container_width=True)

csv = results_df.to_csv(index=False).encode("utf-8")

st.download_button(
"Download results as CSV",
csv,
"hrqol_domain_sort_results.csv",
"text/csv"
)

st.divider()

if st.button("Reset exercise"):
    st.session_state.assignments = {d: "Domain bank" for d in DOMAINS}
    st.rerun()
