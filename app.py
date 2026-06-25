import streamlit as st
import time

# ==========================================
# 1. CONFIGURACIÓN E INICIALIZACIÓN
# ==========================================
st.set_page_config(page_title="Nutricionista-Martin Urday", layout="wide")

# ==========================================
# 2. CAPA DE ENTRADA (Filtros del Usuario)
# ==========================================
with st.sidebar:
    st.header("📋 Perfil del Paciente")
    
    nivel_glucosa = st.number_input("Nivel de Glucosa (mg/dL):", min_value=0, max_value=600, value=120)
    momento_medicion = st.selectbox("Momento de Medición:", ["En ayunas", "2 horas postprandial"])
    
    st.markdown("---")
    st.subheader("Determinantes Sociales")
    presupuesto = st.selectbox("Presupuesto:", ["Bajo", "Medio", "Alto"])
    region = st.selectbox("Región de Residencia:", ["Andina", "Costa", "Selva"])
    alfabetizacion = st.radio("Nivel de Alfabetización:", ["Baja (Visual/Directo)", "Media/Alta (Detallado)"])
    
    analizar_btn = st.button("Generar Evaluación Nutricional", use_container_width=True)

# ==========================================
# 3. CAPA DE INTELIGENCIA (Motor de Reglas Local Expandido)
# ==========================================
def obtener_evaluacion_local(glucosa, momento, presupuesto, region):
    """Cerebro interno: Evalúa reglas médicas, presupuestos detallados y flexibilidad."""
    
    resultado = {
        "diagnostico": "",
        "alerta_critica": "",
        "alimentos_permitidos": [],
        "alimentos_moderados": [],
        "alimentos_evitar": [],
        "justificacion_cientifica": ""
    }
    
    # 1. Evaluación de Alertas Críticas
    if glucosa > 300:
        resultado["alerta_critica"] = "Nivel peligrosamente alto (>300 mg/dL). Riesgo de cetoacidosis. Acuda a urgencias."
        return resultado
    elif glucosa < 70:
        resultado["alerta_critica"] = "Hipoglucemia severa (<70 mg/dL). Consuma carbohidratos de acción rápida inmediatamente."
        return resultado

    # 2. Evaluación Diagnóstica y Gravedad (1 a 4)
    gravedad = 1
    if momento == "En ayunas":
        if glucosa < 100:
            resultado["diagnostico"] = "Sana (Normal)"
        elif 100 <= glucosa <= 109:
            resultado["diagnostico"] = "No tan sana (Resistencia a la insulina inicial)"
            gravedad = 2
        elif 110 <= glucosa <= 125:
            resultado["diagnostico"] = "Prediabetes"
            gravedad = 3
        else:
            resultado["diagnostico"] = "Diabetes"
            gravedad = 4
    else: # Postprandial
        if glucosa < 140:
            resultado["diagnostico"] = "Sana (Normal)"
        elif 140 <= glucosa <= 160:
            resultado["diagnostico"] = "No tan sana (Picos postprandiales elevados)"
            gravedad = 2
        elif 161 <= glucosa <= 199:
            resultado["diagnostico"] = "Prediabetes (Tolerancia disminuida a la glucosa)"
            gravedad = 3
        else:
            resultado["diagnostico"] = "Diabetes"
            gravedad = 4

    # 3. Base de Datos Nutricional Expandida
    
    # A. Asignación estricta por Presupuesto (Proteínas y Grasas)
    if presupuesto == "Bajo":
        proteina = "Huevos sancochados, sangrecita o conservas de atún"
        grasa = "Maní tostado económico y aceitunas"
    elif presupuesto == "Medio":
        proteina = "Pechuga de pollo, pavita o pescado fresco de temporada"
        grasa = "Palta fuerte y aceite de oliva clásico"
    else: # Alto
        proteina = "Cortes magros de res, salmón o pescados finos"
        grasa = "Aceite de oliva extra virgen, almendras y nueces"

    # Alimentos libres universales
    resultado["alimentos_permitidos"] = [
        proteina,
        grasa,
        "Abundantes verduras de hoja verde (Lechuga, espinaca, acelga)",
        "Vegetales ricos en agua (Pepino, tomate, calabacín)",
        "Agua pura o infusiones sin azúcar (Mínimo 2 litros diarios)"
    ]
    
    # B. Asignación de Carbohidratos por Región y Gravedad
    if gravedad == 1: # SANA (Flexibilidad y abundancia)
        resultado["alimentos_evitar"] = [
            "Consumo diario de comida rápida", 
            "Exceso de alcohol",
            "Azúcar añadida en infusiones diarias"
        ]
        
        # Regla de Oro para Sanos: El Cheat Meal
        regla_flexible = "🍔 *Gusto permitido:* 1 comida libre a la semana (postre o comida rápida) para evitar fatiga dietética."
        
        if region == "Andina":
            resultado["alimentos_moderados"] = ["Quinua o Kiwicha (1 a 1.5 tazas)", "Papa o camote (1 a 2 unidades)", "Frutas locales (Chirimoya, aguaymanto)", regla_flexible]
        elif region == "Selva":
            resultado["alimentos_moderados"] = ["Plátano verde o maduro sancochado", "Yuca (porción normal)", "Frutas (Papaya, piña)", regla_flexible]
        else:
            resultado["alimentos_moderados"] = ["Lentejas o pallares", "Arroz integral o fideos (1 taza)", "Frutas de estación", regla_flexible]
            
    elif gravedad == 2: # RESISTENCIA (Advertencia)
        resultado["alimentos_evitar"] = ["Frituras y comida rápida", "Dulces, helados y panadería", "Jugos de fruta (comer la fruta entera)"]
        if region == "Andina":
            resultado["alimentos_moderados"] = ["Quinua (1 taza máximo)", "Papa sancochada (solo 1 unidad pequeña)"]
        elif region == "Selva":
            resultado["alimentos_moderados"] = ["Plátano verde sancochado (evitar el maduro dulce)", "Yuca (solo media porción)"]
        else:
            resultado["alimentos_moderados"] = ["Lentejas (1 taza)", "Arroz integral (media taza)"]
            
    else: # PREDIABETES O DIABETES (Restricción clínica estricta)
        resultado["alimentos_evitar"] = ["Cualquier tipo de azúcar, miel o panela", "Pan blanco y galletas", "Gaseosas (incluso zero)", "Bebidas alcohólicas"]
        if region == "Andina":
            resultado["alimentos_moderados"] = ["Quinua (reducir a 1/3 de taza)"]
            resultado["alimentos_evitar"].append("Papas y tubérculos en puré (alto índice glucémico)")
        elif region == "Selva":
            resultado["alimentos_moderados"] = ["Ensalada de chonta o cocona"]
            resultado["alimentos_evitar"].extend(["Plátano maduro", "Yuca sancochada"])
        else:
            resultado["alimentos_moderados"] = ["Garbanzos sancochados (1/2 taza)"]
            resultado["alimentos_evitar"].append("Arroz blanco e integral")

    # 4. Justificación
    resultado["justificacion_cientifica"] = f"El paciente presenta un diagnóstico de {resultado['diagnostico']} tras registrar {glucosa} mg/dL {momento.lower()}. Se ha aplicado el nivel de restricción {gravedad}/4, ajustando la canasta de proteínas a un presupuesto {presupuesto.lower()} e integrando carbohidratos de la región {region}."

    return resultado

    # 3. Base de Datos Nutricional Cruzada
    # Proteínas por presupuesto
    proteina = "Huevos sancochados o conservas en agua" if presupuesto == "Bajo" else "Pescado fresco, pechuga de pollo o pavita"
    resultado["alimentos_permitidos"] = [proteina, "Verduras de hoja verde (Lechuga, espinaca, brócoli)"]
    
    # Carbohidratos por Región y Gravedad
    if gravedad <= 2: # Sana o Resistencia leve
        if region == "Andina":
            resultado["alimentos_moderados"] = ["Quinua o Kiwicha (1 taza)", "Papa sancochada (1 mediana)"]
            resultado["alimentos_evitar"] = ["Frituras", "Dulces y pan blanco"]
        elif region == "Selva":
            resultado["alimentos_moderados"] = ["Plátano verde sancochado", "Yuca (porción normal)"]
            resultado["alimentos_evitar"] = ["Gaseosas", "Refrescos azucarados locales"]
        else:
            resultado["alimentos_moderados"] = ["Lentejas o pallares", "Arroz integral (1 taza)"]
            resultado["alimentos_evitar"] = ["Fideos blancos", "Panadería refinada"]
    else: # Prediabetes o Diabetes (Restricción dura)
        resultado["alimentos_evitar"] = ["Cualquier tipo de azúcar, miel o panela", "Pan blanco, galletas y postres", "Jugos de fruta (incluso naturales)"]
        if region == "Andina":
            resultado["alimentos_moderados"] = ["Quinua (reducir a 1/3 de taza)"]
            resultado["alimentos_evitar"].append("Papas y tubérculos en puré")
        elif region == "Selva":
            resultado["alimentos_moderados"] = ["Ensalada de chonta o cocona"]
            resultado["alimentos_evitar"].extend(["Plátano maduro", "Yuca sancochada"])
        else:
            resultado["alimentos_moderados"] = ["Garbanzos sancochados (1/2 taza)"]
            resultado["alimentos_evitar"].append("Arroz blanco e integral")

    # 4. Justificación
    resultado["justificacion_cientifica"] = f"El paciente se encuentra en estado de {resultado['diagnostico']} debido a un nivel de {glucosa} mg/dL en medición {momento.lower()}. Se aplica restricción glucémica nivel {gravedad} priorizando insumos accesibles de la región {region}."

    return resultado

# ==========================================
# 4. CAPA DE PRESENTACIÓN ADAPTATIVA (UI)
# ==========================================
st.title("🥗 Nutricionista - Martin Urday")
st.markdown("---")

if analizar_btn:
    # Simulamos un tiempo de procesamiento para dar la sensación de análisis profundo
    with st.spinner("Analizando matrices metabólicas y socioeconómicas..."):
        time.sleep(1.5) 
        
        datos = obtener_evaluacion_local(nivel_glucosa, momento_medicion, presupuesto, region)
        
        # Alertas Críticas
        if datos["alerta_critica"]:
            st.error(f"🚨 **ALERTA MÉDICA:** {datos['alerta_critica']}")
            st.stop()
        
        # Diagnóstico general
        st.info(f"🩺 **Diagnóstico Clínico:** {datos['diagnostico']}")
        
        # Interfaz por Alfabetización
        if "Baja" in alfabetizacion:
            st.markdown("### 🚦 Semáforo de Alimentación")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.success("🟢 **SÍ COMER**")
                for item in datos["alimentos_permitidos"]: st.write(f"✔️ {item}")
                    
            with col2:
                st.warning("🟡 **POCO (Medir)**")
                for item in datos["alimentos_moderados"]: st.write(f"⚠️ {item}")
                    
            with col3:
                st.error("🔴 **NO COMER**")
                for item in datos["alimentos_evitar"]: st.write(f"❌ {item}")
        
        else:
            st.markdown("### 📊 Expediente Nutricional Detallado")
            tab1, tab2, tab3 = st.tabs(["🟢 Permitidos", "🟡 Moderados", "🔴 Restringidos"])
            
            with tab1:
                for item in datos["alimentos_permitidos"]: st.markdown(f"- {item}")
            with tab2:
                for item in datos["alimentos_moderados"]: st.markdown(f"- {item}")
            with tab3:
                for item in datos["alimentos_evitar"]: st.markdown(f"- {item}")
            
            with st.expander("🔬 Ver Justificación Fisiológica"):
                st.write(datos["justificacion_cientifica"])
else:
    st.info("👈 Ingrese los datos en el panel lateral y presione 'Generar Evaluación Nutricional'.")