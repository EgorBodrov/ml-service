import streamlit as st

from post_requests import get_all_jobs, get_job


if "auth" not in st.session_state:
    st.info("Sign In first")
    st.stop()


if st.button("Refresh"):
    st.rerun()

st.header("History of requests")

job_ids = get_all_jobs(st.session_state["auth"]["token"])["job_ids"]
for job_id in job_ids[::-1]:
    job = get_job(st.session_state["auth"]["token"], job_id)
    
    st.metric("status", job["status"])
    st.metric("result", job["result"])
    st.metric("model_name", job["model_name"])
    st.metric("created_at", job["created_at"])
    st.metric("finished_at", job["finished_at"])
    st.markdown("---")
