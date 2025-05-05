import streamlit as st
import time
import pydeck as pdk

COORD_ORIGEN = [10.4001, -75.5144]
COORD_DESTINO = [10.4236, -75.5336]


def show_tracking():
    st.subheader("📍 Simulación de Seguimiento de Entrega")

    progress = st.slider("Progreso del vehículo (%)", 0, 100, 0)
    lat = COORD_ORIGEN[0] + (COORD_DESTINO[0] - COORD_ORIGEN[0]) * (progress / 100)
    lon = COORD_ORIGEN[1] + (COORD_DESTINO[1] - COORD_ORIGEN[1]) * (progress / 100)

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=[{"position": [lon, lat]}],
        get_position="position",
        get_color="[255, 0, 0, 160]",
        get_radius=150,
    )

    view_state = pdk.ViewState(
        longitude=lon,
        latitude=lat,
        zoom=12,
        pitch=40
    )

    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
