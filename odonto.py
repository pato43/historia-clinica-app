import streamlit as st
from datetime import date, datetime
from fpdf import FPDF
import io

st.set_page_config(page_title="Historia Clínica UPEM", layout="wide")
st.title("🦷 Historia Clínica Odontológica - Universidad Privada del Estado de México")
st.markdown("---")

# ================= FORMULARIO =================
with st.form("form_historia_clinica"):
    st.subheader("🧑‍🏫 Datos del Alumno Responsable")
    col1, col2 = st.columns(2)
    with col1:
        nombre_alumno = st.text_input("Nombre del alumno que elabora la historia clínica")
        matricula_alumno = st.text_input("Matrícula")
    with col2:
        asignatura = st.text_input("Asignatura Clínica")
        fecha_ingreso = st.date_input("Fecha de ingreso del paciente", value=date.today())

    st.markdown("---")
    st.subheader("👤 Datos Generales del Paciente")
    col1, col2, col3 = st.columns(3)
    with col1:
        nombre_paciente = st.text_input("Nombre completo")
        edad = st.number_input("Edad", min_value=0, step=1)
        sexo = st.selectbox("Sexo", ["Masculino", "Femenino", "Otro"])
    with col2:
        fecha_nacimiento = st.date_input("Fecha de nacimiento", min_value=datetime(1900, 1, 1), max_value=datetime.today())
        lugar_nacimiento = st.text_input("Lugar de nacimiento")
        curp = st.text_input("CURP")
    with col3:
        estado_civil = st.selectbox("Estado civil", ["Soltero(a)", "Casado(a)", "Viudo(a)", "Unión libre", "Otro"])
        religion = st.text_input("Religión")
        escolaridad = st.selectbox("Escolaridad", ["Primaria", "Secundaria", "Preparatoria", "Licenciatura", "Maestría", "Doctorado", "Otro"])

    col4, col5 = st.columns([2, 1])
    with col4:
        domicilio = st.text_area("Domicilio completo (calle, número, colonia, municipio, estado)")
        ocupacion = st.text_input("Ocupación actual")
    with col5:
        telefono = st.text_input("Teléfono de contacto")
        correo = st.text_input("Correo electrónico")

    st.markdown("---")
    st.subheader("🦷 Evaluación de Piezas Dentales")
    condiciones_dentales = ["Caries", "Obturaciones defectuosas", "Fracturas", "Ausencia dentaria", "Movilidad dental", "Cambio de color", "Desgaste", "Cálculo"]

    dientes_superior = [str(i) for i in range(18, 10, -1)] + [str(i) for i in range(21, 29)]
    dientes_inferior = [str(i) for i in range(48, 40, -1)] + [str(i) for i in range(31, 39)]

    seleccion_dental = {}

    def registrar_condiciones(dientes, arcada):
        st.markdown(f"**Arcada {arcada.capitalize()}**")
        filas = [dientes[i:i+9] for i in range(0, len(dientes), 9)]
        for fila in filas:
            cols = st.columns(len(fila))
            for i, diente in enumerate(fila):
                condiciones = cols[i].multiselect(f"Pieza {diente}", condiciones_dentales, key=f"{arcada}_{diente}")
                if condiciones:
                    seleccion_dental[diente] = condiciones

    registrar_condiciones(dientes_superior, "superior")
    registrar_condiciones(dientes_inferior, "inferior")

    submitted = st.form_submit_button("📄 Generar Historia Clínica PDF")
    st.markdown("---")
    st.subheader("🧬 Contexto Sociocultural")
    grupo_etnico = st.selectbox("¿Pertenece a algún grupo étnico?", ["No", "Sí - Indígena", "Sí - Afrodescendiente", "Otro"])
    idioma_indigena = st.text_input("Idioma indígena (si aplica)", disabled=(grupo_etnico == "No"))

    st.markdown("---")
    st.subheader("📋 Motivo de Consulta Principal")
    motivo_consulta = st.text_area("Describe el motivo principal por el que acude a consulta odontológica")

    st.subheader("📋 Motivo de Consulta Secundario o Subjetivo")
    sintomas_asociados = st.text_area("¿Presenta algún síntoma asociado? (dolor, sangrado, dificultad para masticar, etc.)")

    st.markdown("---")
    st.subheader("🧾 Otros Aspectos Generales")
    grupo_sanguineo = st.selectbox("Grupo sanguíneo y factor RH", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Desconocido"])
    seguro_medico = st.selectbox("Tipo de derechohabiencia médica", ["IMSS", "ISSSTE", "INSABI", "Seguro privado", "Ninguno", "Otro"])
    tipo_consulta = st.selectbox("Tipo de consulta", ["Primera vez", "Reconsulta", "Consulta preventiva", "Emergencia"])

    st.markdown("---")
    st.subheader("🧬 Antecedentes Heredofamiliares")
    antecedentes_heredo = st.text_area("Describa antecedentes relevantes en padres, abuelos, hermanos (ej. diabetes, cáncer, epilepsia, etc.)")

    st.markdown("### 🪥 Antecedentes Personales No Patológicos")
    col_np1, col_np2 = st.columns(2)
    with col_np1:
        fuma = st.checkbox("¿Fuma?", key="fuma")
        alcohol = st.checkbox("¿Consume alcohol?", key="alcohol")
        drogas = st.checkbox("¿Consume drogas?", key="drogas")
        tatuajes = st.checkbox("¿Tiene tatuajes o perforaciones?", key="tatuajes")
    with col_np2:
        tiene_mascota = st.checkbox("¿Tiene mascota(s)?", key="mascota")
        tipo_mascota = st.text_input("Tipo de mascota", disabled=not tiene_mascota)
        tipo_vivienda = st.selectbox("Tipo de vivienda", ["Casa propia", "Renta", "Cuartos", "Otro"])
        personas_hogar = st.number_input("Número de personas en su hogar", step=1, min_value=0)

    higiene_oral = st.text_area("Hábitos de higiene oral (frecuencia de cepillado, uso de hilo dental, enjuague, etc.)")

    st.markdown("### 🏥 Antecedentes Personales Patológicos")
    st.markdown("Selecciona los padecimientos que ha presentado el paciente hasta la fecha:")

    sistemas = {
        "Cardiovasculares": ["Hipertensión", "Infartos", "Arritmias"],
        "Respiratorios": ["Asma", "Faringitis crónica", "Bronquitis"],
        "Endocrinos": ["Diabetes tipo I o II", "Hipotiroidismo", "Hiperinsulinismo"],
        "Inmunológicos": ["Alergias severas", "VIH/SIDA"],
        "Digestivos": ["Colitis", "Gastritis", "Hepatitis"],
        "Neurológicos": ["Epilepsia", "Migrañas", "Parkinson"],
        "Genitourinarios": ["Cistitis", "Nefritis", "Litiasis renal"],
        "Hematológicos": ["Anemias", "Coagulopatías", "Leucemia"],
        "Otros": ["Cáncer", "Tuberculosis", "COVID prolongado"]
    }

    antecedentes_patologicos = {}
    for sistema, enfermedades in sistemas.items():
        st.markdown(f"**{sistema}**")
        enfermedades_seleccionadas = st.multiselect(f"Padecimientos en {sistema}:", enfermedades, key=sistema)
        antecedentes_patologicos[sistema] = enfermedades_seleccionadas

    st.markdown("### 👩‍⚕️ Gineco-Obstétricos (solo en caso de mujeres)")
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        embarazada = st.radio("¿Está actualmente embarazada?", ["No", "Sí", "No aplica"], key="embarazada")
        ultima_menstruacion = st.date_input("Fecha de última menstruación", disabled=(embarazada == "No aplica"))
    with col_g2:
        alteraciones_menstruales = st.checkbox("¿Tiene alteraciones menstruales?", key="alteraciones")
        metodo_anticonceptivo = st.selectbox("Método anticonceptivo", ["Ninguno", "Oral", "DIU", "Preservativo", "Inyección", "Otro"])

    st.markdown("---")
    st.subheader("🧍 Exploración Física General")
    estado_conciencia = st.selectbox("Estado de consciencia", ["Alerta", "Somnoliento", "Obnubilado", "Comatoso"])
    nutricion = st.selectbox("Estado nutricional", ["Normal", "Desnutrición leve", "Desnutrición severa", "Sobrepeso", "Obesidad"])
    postura = st.selectbox("Postura habitual", ["Erecta", "Encorvada", "Lateralizada", "Dolorosa"])

    col_gen1, col_gen2 = st.columns(2)
    with col_gen1:
        marcha = st.text_input("Tipo de marcha (normal, claudicante, etc.)")
        lenguaje = st.text_input("Lenguaje observado (normal, disartria, mudo, etc.)")
    with col_gen2:
        actitud = st.selectbox("Actitud ante el entrevistador", ["Colaborador", "Ansioso", "Hostil", "Reservado"])
        estado_animo = st.selectbox("Estado de ánimo aparente", ["Tranquilo", "Nervioso", "Triste", "Irritable", "Eufórico"])
    st.markdown("---")
    st.subheader("🩺 Signos Vitales Detallados")
    col_v1, col_v2, col_v3, col_v4 = st.columns(4)
    with col_v1:
        peso = st.number_input("Peso (kg)", step=0.1)
    with col_v2:
        talla = st.text_input("Talla (m)")
    with col_v3:
        tension_arterial = st.text_input("Tensión arterial (ej. 120/80)")
    with col_v4:
        temperatura = st.number_input("Temperatura (°C)", step=0.1)

    col_v5, col_v6, col_v7 = st.columns(3)
    with col_v5:
        pulso = st.number_input("Pulso (lpm)", step=1)
    with col_v6:
        frecuencia_resp = st.number_input("Frecuencia respiratoria (rpm)", step=1)
    with col_v7:
        saturacion = st.number_input("Saturación O₂ (%)", min_value=0, max_value=100)

    st.markdown("---")
    st.subheader("🦷 Exploración Regional (Cabeza y Cuello)")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        cabeza = st.text_input("Cabeza (forma, simetría, lesiones visibles, etc.)")
        cuello = st.text_input("Cuello (movilidad, masas, dolor, etc.)")
        ganglios = st.text_input("Ganglios palpables (submandibulares, cervicales, etc.)")
    with col_c2:
        piel = st.text_input("Estado de la piel (coloración, lesiones, hidratación)")
        mucosa = st.text_input("Mucosa oral (color, lesiones, sangrado, etc.)")
        labios = st.text_input("Labios (resequedad, heridas, simetría)")

    st.subheader("🦷 Exploración Oral Específica")
    lengua = st.text_input("Lengua (movilidad, tamaño, saburra, lesiones)")
    paladar = st.text_input("Paladar duro y blando (integridad, pigmentación)")
    piso_boca = st.text_input("Piso de boca (elevación, secreciones, lesiones)")
    carrillos = st.text_input("Carrillos (simetría, movilidad, presencia de lesiones)")
    atm = st.text_input("Articulación Temporomandibular (chasquido, dolor, apertura)")
    saliva = st.selectbox("Calidad de saliva", ["Normal", "Espesa", "Escasa", "Ausente", "Hiperflujo"])

    st.markdown("---")
    st.subheader("🦷 Exploración Intraoral Completa")
    col_o1, col_o2 = st.columns(2)
    with col_o1:
        encías = st.selectbox("Estado de las encías", ["Sanas", "Inflamadas", "Sangrantes", "Retracción", "Hipertrofia"])
        frenillos = st.text_input("Observaciones en frenillos (labial, lingual)")
        paladar_oral = st.text_input("Paladar (forma, pigmentación, lesiones)")
        lengua_intraoral = st.text_input("Lengua (movilidad, saburra, lesiones)")
    with col_o2:
        mucosa_yugal = st.text_input("Mucosa yugal (color, lesiones, úlceras)")
        piso_boca_intra = st.text_input("Piso de boca (secreciones, lesiones, elevación)")
        carrillos_intra = st.text_input("Carrillos (simetría, movilidad, lesiones)")
        observaciones_orales = st.text_area("Otras observaciones intraorales relevantes")

    st.markdown("---")
    st.subheader("🪥 Periodontograma Rápido")
    col_perio1, col_perio2 = st.columns(2)
    with col_perio1:
        sangrado_sondas = st.selectbox("Sangrado al sondaje", ["No", "Sí localizado", "Sí generalizado"])
        profundidad_bolsas = st.selectbox("Profundidad de bolsas", ["1-3 mm", "4-5 mm", "Más de 6 mm"])
        movilidad_general = st.selectbox("Movilidad dental general", ["Sin movilidad", "Grado I", "Grado II", "Grado III"])
    with col_perio2:
        placa = st.selectbox("Índice de placa", ["Bajo", "Moderado", "Alto"])
        calculo = st.selectbox("Presencia de cálculo", ["Ausente", "Ligero", "Moderado", "Abundante"])
        halitosis = st.selectbox("Halitosis (mal aliento)", ["No", "Leve", "Moderada", "Severa"])

    st.markdown("---")
    st.subheader("🧩 Odontograma Visual por Zona (Interactivo)")

    zonas = ["V", "L", "M", "D"]
    seleccion_dientes = {}

    def render_odontograma(dientes, fila):
        cols = st.columns(len(dientes))
        for i, d in enumerate(dientes):
            with cols[i]:
                st.markdown(f"**{fila} {d}**")
                seleccionadas = st.multiselect("Zonas", zonas, key=f"diente_{fila}_{d}")
                if seleccionadas:
                    seleccion_dientes[d] = seleccionadas

    st.markdown("**Arcada Superior**")
    render_odontograma(dientes_superior, "sup")
    st.markdown("**Arcada Inferior**")
    render_odontograma(dientes_inferior, "inf")

    st.markdown("⚠️ El odontograma visual permite registrar zonas afectadas por diente de forma interactiva.")
    st.markdown("---")
    st.subheader("🩺 Diagnóstico Clínico")
    diagnostico_presuntivo = st.text_area("Diagnóstico presuntivo (descripción clínica basada en hallazgos preliminares)")
    diagnostico_definitivo = st.text_area("Diagnóstico definitivo (basado en evaluación completa y exámenes complementarios)")

    st.markdown("---")
    st.subheader("🛠️ Plan de Tratamiento")
    plan_tratamiento = st.text_area("Plan de tratamiento propuesto (procedimientos, sesiones, tiempo estimado)")
    consentimiento = st.checkbox("El paciente acepta y entiende el plan de tratamiento explicado")

    st.markdown("---")
    st.subheader("✍️ Firmas y Fecha")
    firma_paciente = st.text_input("Nombre del paciente (firma digital)")
    firma_alumno = st.text_input("Nombre del alumno responsable (firma digital)")
    fecha_actual = date.today().strftime("%d/%m/%Y")

    submitted = st.form_submit_button("📄 Generar Historia Clínica PDF")

# ====================== GENERACIÓN DE PDF ======================
if submitted:
    if not isinstance(fecha_nacimiento, date):
        fecha_nacimiento = date.today()
    if not isinstance(fecha_ingreso, date):
        fecha_ingreso = date.today()
    if not isinstance(ultima_menstruacion, date):
        ultima_menstruacion = date.today()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "HISTORIA CLÍNICA ODONTOLÓGICA - UPEM", ln=True, align='C')
    pdf.set_font("Helvetica", '', 11)
    pdf.ln(5)

    def add_section(title):
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(0, 10, f"{title}", ln=True)
        pdf.set_font("Helvetica", '', 11)

    def add_text(text):
        pdf.multi_cell(0, 8, text)

    add_section("1. Datos del Alumno Responsable")
    add_text(f"Alumno: {nombre_alumno}\nMatrícula: {matricula_alumno}\nAsignatura: {asignatura}\nFecha de ingreso: {fecha_ingreso.strftime('%d/%m/%Y')}")

    add_section("2. Datos del Paciente")
    add_text(
        f"Nombre: {nombre_paciente}\nEdad: {edad} años\nSexo: {sexo}\nCURP: {curp}\n"
        f"Fecha de nacimiento: {fecha_nacimiento.strftime('%d/%m/%Y')}\nLugar de nacimiento: {lugar_nacimiento}\n"
        f"Estado civil: {estado_civil}\nReligión: {religion}\nEscolaridad: {escolaridad}\n"
        f"Ocupación: {ocupacion}\nDomicilio: {domicilio}\nTeléfono: {telefono}\nCorreo: {correo}"
    )

    add_section("3. Contexto Sociocultural y Generales")
    add_text(f"Grupo étnico: {grupo_etnico}\nIdioma indígena: {idioma_indigena}\nGrupo sanguíneo: {grupo_sanguineo}\n"
             f"Tipo de consulta: {tipo_consulta}\nSeguro médico: {seguro_medico}")

    add_section("4. Motivos de Consulta")
    add_text(f"Motivo principal:\n{motivo_consulta}\n\nSíntomas asociados:\n{sintomas_asociados}")

    add_section("5. Antecedentes Heredofamiliares")
    add_text(antecedentes_heredo)

    add_section("6. No Patológicos")
    add_text(f"Fuma: {'Sí' if fuma else 'No'}\nAlcohol: {'Sí' if alcohol else 'No'}\nDrogas: {'Sí' if drogas else 'No'}\n"
             f"Tatuajes: {'Sí' if tatuajes else 'No'}\nMascota: {'Sí' if tiene_mascota else 'No'} - {tipo_mascota}\n"
             f"Vivienda: {tipo_vivienda}\nPersonas en hogar: {personas_hogar}\nHigiene oral: {higiene_oral}")

    add_section("7. Patológicos")
    for sistema, enf in antecedentes_patologicos.items():
        if enf:
            add_text(f"{sistema}: {', '.join(enf)}")

    add_section("8. Gineco-Obstétricos")
    add_text(f"Embarazada: {embarazada}\nÚltima menstruación: {ultima_menstruacion.strftime('%d/%m/%Y') if isinstance(ultima_menstruacion, date) else 'No aplica'}\n"
             f"Alteraciones menstruales: {'Sí' if alteraciones_menstruales else 'No'}\nMétodo anticonceptivo: {metodo_anticonceptivo}")
    add_section("9. Exploración Física General")
    add_text(f"Conciencia: {estado_conciencia}\nNutrición: {nutricion}\nPostura: {postura}\nMarcha: {marcha}\nLenguaje: {lenguaje}\n"
             f"Actitud: {actitud}\nEstado de ánimo: {estado_animo}")

    add_section("10. Signos Vitales")
    add_text(f"Peso: {peso} kg\nTalla: {talla} m\nTA: {tension_arterial}\nTemperatura: {temperatura} °C\nPulso: {pulso} lpm\n"
             f"FR: {frecuencia_resp} rpm\nSaturación O₂: {saturacion}%")

    add_section("11. Exploración Regional / Intraoral")
    add_text(f"Cabeza: {cabeza}\nCuello: {cuello}\nGanglios: {ganglios}\nPiel: {piel}\nMucosa: {mucosa}\nLabios: {labios}\n"
             f"Lengua: {lengua}\nPaladar: {paladar}\nPiso de boca: {piso_boca}\nCarrillos: {carrillos}\nATM: {atm}\nSaliva: {saliva}\n"
             f"Encías: {encías}\nFrenillos: {frenillos}\nLengua (intraoral): {lengua_intraoral}\nPaladar oral: {paladar_oral}\n"
             f"Mucosa yugal: {mucosa_yugal}\nPiso de boca (intraoral): {piso_boca_intra}\nCarrillos (intraoral): {carrillos_intra}\n"
             f"Observaciones orales: {observaciones_orales}")

    add_section("12. Piezas Dentales con Condiciones")
    for diente, condiciones in seleccion_dental.items():
        add_text(f"Diente {diente}: {', '.join(condiciones)}")

    add_section("13. Periodontograma")
    add_text(f"Sangrado al sondaje: {sangrado_sondas}\nProfundidad bolsas: {profundidad_bolsas}\nMovilidad dental: {movilidad_general}\n"
             f"Índice placa: {placa}\nCálculo: {calculo}\nHalitosis: {halitosis}")

    add_section("14. Odontograma Interactivo")
    for diente, zonas in seleccion_dientes.items():
        add_text(f"Diente {diente}: zonas afectadas - {', '.join(zonas)}")

    add_section("15. Diagnóstico")
    add_text(f"Presuntivo: {diagnostico_presuntivo}\nDefinitivo: {diagnostico_definitivo}")

    add_section("16. Plan de Tratamiento")
    add_text(plan_tratamiento + ("\n✔ Aceptado por el paciente." if consentimiento else "\n✖ No confirmado por el paciente."))

    add_section("17. Firmas y Fecha")
    add_text(f"Paciente: {firma_paciente}\nAlumno: {firma_alumno}\nFecha de emisión: {fecha_actual}")

    # Exportar PDF
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    st.success("✅ PDF generado exitosamente.")
    st.download_button(
        label="📥 Descargar Historia Clínica PDF",
        data=pdf_buffer.getvalue(),
        file_name="historia_clinica_upem.pdf",
        mime="application/pdf"
    )
