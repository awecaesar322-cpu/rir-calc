import streamlit as st
import math

st.set_page_config(
    page_title="Калькулятор РИР", 
    page_icon="🛠️", 
    layout="centered"
)

st.title("🛠️ Калькулятор РИР")
st.caption("Расчёт установки цементного моста")

# --- Блок 1: Параметры скважины ---
with st.expander("Параметры колонны и компоновки", expanded=True):
    col_ext = st.number_input("Наружный диаметр ЭК, мм", value=146.0, step=1.0)
    col_wall = st.number_input("Толщина стенки ЭК, мм", value=7.7, step=0.1)
    
    use_nkt = st.toggle("Заливка через НКТ", value=True)
    if use_nkt:
        nkt_ext = st.number_input("Наружный диаметр НКТ, мм", value=73.0, step=1.0)
        nkt_wall = st.number_input("Толщина стенки НКТ, мм", value=5.5, step=0.1)

# --- Блок 2: Интервал и раствор ---
with st.expander("Интервал и параметры смеси", expanded=True):
    depth_sole = st.number_input("Глубина подошвы (забой), м", value=2200.0, step=10.0)
    h_bridge = st.number_input("Высота (мощность) моста, м", value=80.0, step=5.0)
    k_excess = st.number_input("Коэффициент запаса (k)", value=1.10, step=0.01)
    
    rho_slurry = st.number_input("Плотность раствора, г/см³", value=1.85, step=0.01)
    wc_ratio = st.number_input("Водоцементное отношение (В/Ц)", value=0.50, step=0.01)

# --- Расчёт ---
depth_roof = depth_sole - h_bridge

if depth_roof < 0:
    st.error("Ошибка: высота моста превышает глубину скважины!")
else:
    # Внутренний диаметр и погонный объем ЭК
    id_col_m = (col_ext - 2 * col_wall) / 1000
    v_per_m_col = (math.pi * (id_col_m ** 2)) / 4

    # Объем раствора
    v_slurry = v_per_m_col * h_bridge * k_excess

    # Масса цемента и объем воды
    total_mass_kg = v_slurry * (rho_slurry * 1000)
    m_cement_t = (total_mass_kg / (1 + wc_ratio)) / 1000
    v_water_m3 = m_cement_t * wc_ratio

    # Продавка
    if use_nkt:
        id_nkt_m = (nkt_ext - 2 * nkt_wall) / 1000
        v_per_m_nkt = (math.pi * (id_nkt_m ** 2)) / 4
        v_disp = v_per_m_nkt * depth_roof
    else:
        v_disp = v_per_m_col * depth_roof

    st.markdown("---")
    st.subheader("Результаты")

    c1, c2 = st.columns(2)
    c1.metric("Кровля моста", f"{depth_roof:.1f} м")
    c2.metric("Объём раствора", f"{v_slurry:.2f} м³")
    
    c3, c4 = st.columns(2)
    c3.metric("Сухой цемент", f"{m_cement_t:.2f} т")
    c4.metric("Вода затворения", f"{v_water_m3:.2f} м³")

    st.metric("Объём продавки (до кровли)", f"{v_disp:.2f} м³")

    # Итоговая сводка
    with st.expander("Технологическая сводка"):
        st.write(f"• **D внутр. ЭК:** {id_col_m * 1000:.1f} мм ({v_per_m_col * 1000:.2f} л/м)")
        st.write(f"• **Интервал:** {depth_sole:.1f} — {depth_roof:.1f} м")
        st.write(f"• **Теоретический объём стакана:** {v_per_m_col * h_bridge:.2f} м³")
        if use_nkt:
            st.write(f"• **D внутр. НКТ:** {id_nkt_m * 1000:.1f} мм ({v_per_m_nkt * 1000:.2f} л/м)")
