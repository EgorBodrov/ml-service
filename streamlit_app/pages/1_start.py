import streamlit as st

from post_requests import get_predictors, run_predictor, get_balance

if "auth" not in st.session_state:
    st.info("Sign In first")
    st.stop()

st.header("Enter your data")

data = st.session_state["data"]

brand = st.selectbox(
    "Brand", data["brand"].unique().tolist(), index=0
)

model = st.selectbox(
    "Model", data[data["brand"] == brand]["model"].unique().tolist(), index=0
)

highwaympg = st.number_input(
    "MPG on the Highway",
    min_value=data["highwaympg"].min(),
    value=data["highwaympg"].mode().iloc[0],
    max_value=data["highwaympg"].max()
)

citympg = st.number_input(
    "Miles Per Gallon (MPG) in City Driving",
    min_value=data["citympg"].min(),
    value=data["citympg"].mode().iloc[0],
    max_value=data["citympg"].max()
)

peakrpm = st.number_input(
    "Engine's Peak RPM",
    min_value=data["peakrpm"].min(),
    value=data["peakrpm"].mode().iloc[0],
    max_value=data["peakrpm"].max()
)

horsepower = st.number_input(
    "Horsepower",
    min_value=data["horsepower"].min(),
    value=data["horsepower"].mode().iloc[0],
    max_value=data["horsepower"].max()
)

compressionratio = st.number_input(
    "Compression Ratio",
    min_value=data["compressionratio"].min(),
    value=data["compressionratio"].mode().iloc[0],
    max_value=data["compressionratio"].max()
)

stroke = st.number_input(
    "Stroke Length",
    min_value=data["stroke"].min(),
    value=data["stroke"].mode().iloc[0],
    max_value=data["stroke"].max(),
    step=0.01
)

boreratio = st.number_input(
    "Bore Ratio",
    min_value=data["boreratio"].min(),
    value=data["boreratio"].mode().iloc[0],
    max_value=data["boreratio"].max(),
    step=0.01
)

enginesize = st.number_input(
    "Engine Size",
    min_value=int(data["enginesize"].min()),
    value=int(data["enginesize"].mode().iloc[0]),
    max_value=int(data["enginesize"].max()),
    step=1
)

cylindernumber = st.selectbox(
    "Number of Cylinders",
    data["cylindernumber"].unique().tolist()
)

enginetype = st.selectbox(
    "Engine Type",
    data["enginetype"].unique().tolist()
)

curbweight = st.number_input(
    "Curb Weight",
    min_value=int(data["curbweight"].min()),
    value=int(data["curbweight"].mode().iloc[0]),
    max_value=int(data["curbweight"].max()),
    step=1
)

carheight = st.number_input(
    "Car Height",
    min_value=float(data["carheight"].min()),
    value=float(data["carheight"].mode().iloc[0]),
    max_value=float(data["carheight"].max()),
    step=0.01
)

carwidth = st.number_input(
    "Car Width",
    min_value=float(data["carwidth"].min()),
    value=float(data["carwidth"].mode().iloc[0]),
    max_value=float(data["carwidth"].max()),
    step=0.01
)

carlength = st.number_input(
    "Car Length",
    min_value=float(data["carlength"].min()),
    value=float(data["carlength"].mode().iloc[0]),
    max_value=float(data["carlength"].max()),
    step=0.01
)

wheelbase = st.number_input(
    "Wheelbase",
    min_value=float(data["wheelbase"].min()),
    value=float(data["wheelbase"].mode().iloc[0]),
    max_value=float(data["wheelbase"].max()),
    step=0.01
)

enginelocation = st.selectbox(
    "Engine Location",
    data["enginelocation"].unique().tolist()
)

drivewheel = st.selectbox(
    "Drive Wheel",
    data["drivewheel"].unique().tolist()
)

carbody = st.selectbox(
    "Car Body",
    data["carbody"].unique().tolist()
)

doornumber = st.selectbox(
    "Number of Doors",
    data["doornumber"].unique().tolist()
)

aspiration = st.selectbox(
    "Aspiration",
    data["aspiration"].unique().tolist()
)

fueltype = st.selectbox(
    "Fuel Type",
    data["fueltype"].unique().tolist()
)

symboling = st.selectbox(
    "Symboling",
    sorted(data["symboling"].unique().tolist())
)

fuelsystem = st.selectbox(
    "Fuel System",
    data["fuelsystem"].unique().tolist()
)

data = {
        "symboling": symboling,
        "fueltype": fueltype,
        "aspiration": aspiration,
        "doornumber": doornumber,
        "carbody": carbody,
        "drivewheel": drivewheel,
        "enginelocation": enginelocation,
        "wheelbase": wheelbase,
        "carlength": carlength,
        "carwidth": carwidth,
        "carheight": carheight,
        "curbweight": curbweight,
        "enginetype": enginetype,
        "cylindernumber": cylindernumber,
        "enginesize": enginesize,
        "fuelsystem": fuelsystem,
        "boreratio": boreratio,
        "stroke": stroke,
        "compressionratio": compressionratio,
        "horsepower": horsepower,
        "peakrpm": peakrpm,
        "citympg": citympg,
        "highwaympg": highwaympg,
        "brand": brand,
        "model": model
    }

st.header("Available models")

if "predictors" not in st.session_state:
    st.session_state["predictors"] = get_predictors(st.session_state["auth"]["token"])

for predictor in st.session_state["predictors"]["models"]:
    st.markdown("---")
    st.markdown(f"**NAME**: {predictor['model_name']}")
    st.markdown(f"**PRICE**: {predictor['price']}")

    if st.button("Run", key=predictor['model_name']):
        try:
            result = run_predictor(st.session_state["auth"]["token"], predictor["model_name"], data)
            st.session_state["balance"] = get_balance(st.session_state["auth"]["token"])
            st.rerun()
        except Exception as exc:
            st.error(str(exc))
