import streamlit as st
import pandas as pd

from post_requests import (
    signup_user,
    signin_user,
    get_balance,
    topup_balance,
)


st.set_page_config(
    page_title="CAR PRICE Predictor Dashboard",
    # layout="wide",
)


@st.cache_data
def load_data():
    df = pd.read_csv("preprocessed_data.csv")
    df.drop(columns=["CarName", "price"], inplace=True)
    return df


DATA = load_data()
st.session_state["data"] = DATA


def signup_page():
    with st.form("Sign Up"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button("Sign Up")
        if submitted:
            try:
                signup_user(username, email, password)
            except Exception as exc:
                st.error(str(exc))
            else:
                st.success("User created successfully. Now sign in")


def signin_page():
    with st.form("Sign In"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button("Sign In")
        if submitted:
            try:
                response = signin_user(email, password)
            except Exception as exc:
                st.error(str(exc))
            else:
                st.success("Authinticated successfully")
                st.session_state["auth"] = response
                st.rerun()


def main_page():
    st.title(f"Welcome, {st.session_state['auth']['name']}!")

    if "balance" not in st.session_state:
        st.session_state["balance"] = get_balance(st.session_state["auth"]["token"])

    balance = st.session_state["balance"]
    st.sidebar.metric(f"Your balance in credits", value=balance["amount"])

    new_amount = st.sidebar.number_input(
        "Top Up", min_value=0, value=10, step=1
    )
    if st.sidebar.button("Submit"):
        topup_balance(st.session_state["auth"]["token"], balance["amount"] + new_amount)
        st.session_state["balance"] = get_balance(st.session_state["auth"]["token"])
        st.rerun()


if __name__ == "__main__":
    if 'auth' in st.session_state:
        main_page()

        pg = st.navigation([
            st.Page("pages/1_start.py", title="Start"),
            st.Page("pages/2_history.py", title="History")
        ])
        pg.run()
    else:
        st.title("You need to authenticate first")
        tab1, tab2 = st.tabs(["Sign Up", "Sign In"])

        with tab1:
            signup_page()
        with tab2:
            signin_page()

    st.markdown("---")
    st.text("© 2025 Egor Bodrov")
