import streamlit as st

# =================================================================
# LÓGICA DE VALIDACIÓN
# =================================================================

MAPA_NOTAS = {
    'Do': 0, 'Re': 2, 'Mi': 4, 'Fa': 5, 'Sol': 7, 'La': 9, 'Si': 11,
    'Do#': 1, 'Reb': 1, 'Re#': 3, 'Mib': 3, 'Mi#': 5, 'Fa#': 6, 
    'Solb': 6, 'Sol#': 8, 'Lab': 8, 'La#': 10, 'Sib': 10, 'Si#': 0, 
    'DoX': 2, 'ReX': 4, 'MiX': 6, 'FaX': 7, 'SolX': 9, 'LaX': 11, 'SiX': 1,
    'Dobb': 10, 'Rebb': 0, 'Mibb': 2, 'Fabb': 3, 'Solbb': 5, 'Labb': 7, 'Sibb': 9 
}

MAPA_ORDEN = {
    'Do': 0, 'Re': 1, 'Mi': 2, 'Fa': 3, 'Sol': 4, 'La': 5, 'Si': 6, 
    'Do#': 0, 'Reb': 1, 'Re#': 1, 'Mib': 2, 'Mi#': 2, 'Fa#': 3, 'Solb': 4, 'Sol#': 4, 'Lab': 5, 'La#': 5, 'Sib': 6, 'Si#': 6, 
    'DoX': 0, 'ReX': 1, 'MiX': 2, 'FaX': 3, 'SolX': 4, 'LaX': 5, 'SiX': 6,
    'Dobb': 0, 'Rebb': 1, 'Mibb': 2, 'Fabb': 3, 'Solbb': 4, 'Labb': 5, 'Sibb': 6
}

REGLAS_ACORDES = {
    'Mayor': {'3ra': 4, '5ta': 7, 'nombre3ra': "3ra Mayor", 'nombre5ta': "5ta Justa"},
    'Menor': {'3ra': 3, '5ta': 7, 'nombre3ra': "3ra menor", 'nombre5ta': "5ta Justa"},
    'Aumentado': {'3ra': 4, '5ta': 8, 'nombre3ra': "3ra Mayor", 'nombre5ta': "5ta Aumentada"},
    'Disminuido': {'3ra': 3, '5ta': 6, 'nombre3ra': "3ra menor", 'nombre5ta': "5ta Disminuida"}
}

def limpiar_nota(nota):
    if not nota:
        return ''
    nota = nota.strip()
    limpia = nota.capitalize()
    if limpia.endswith('x'):
        limpia = limpia[:-1] + 'X'
    return limpia

def validar_acorde(tipoSolicitado, fundamental, tercera, quinta):
    fundamental = limpiar_nota(fundamental)
    tercera = limpiar_nota(tercera)
    quinta = limpiar_nota(quinta)
    tipoSolicitado = tipoSolicitado.capitalize()

    retroalimentacion_parts = []
    es_correcto = True
    
    regla = REGLAS_ACORDES.get(tipoSolicitado)
    if not regla:
        return [("🛑 ERROR: El tipo de acorde no es válido.", "error_entrada")]

    if not all(nota in MAPA_NOTAS for nota in [fundamental, tercera, quinta]):
        return [("🛑 ERROR DE ENTRADA: Una o más notas no son válidas. Revise la notación.", "error_entrada")]

    index_F = MAPA_NOTAS[fundamental]
    index_3 = MAPA_NOTAS[tercera]
    index_5 = MAPA_NOTAS[quinta]
    orden_F = MAPA_ORDEN[fundamental]
    orden_3 = MAPA_ORDEN[tercera]
    orden_5 = MAPA_ORDEN[quinta]
    
    semitonos_3ra = (index_3 - index_F + 12) % 12
    semitonos_5ta = (index_5 - index_F + 12) % 12
    distancia_3ra = (orden_3 - orden_F + 7) % 7
    distancia_5ta = (orden_5 - orden_F + 7) % 7
    
    # CHEQUEO 1: ORTOGRAFÍA
    if distancia_3ra != 2 or distancia_5ta != 4:
        retroalimentacion_parts.append(("🛑 **ERROR DE ORTOGRAFÍA MUSICAL**\n\n", "incorrecto"))
        if distancia_3ra != 2:
            retroalimentacion_parts.append((f"❌ La nota **{tercera}** es la {distancia_3ra + 1}a de {fundamental} (Debería ser la 3ra).\n", "incorrecto"))
            retroalimentacion_parts.append(("   * **Paso a seguir:** La tercera de un acorde está a **dos pasos ordinales** de la fundamental (ej: Do -> Mi).\n\n", "normal"))
        if distancia_5ta != 4:
            retroalimentacion_parts.append((f"❌ La nota **{quinta}** es la {distancia_5ta + 1}a de {fundamental} (Debería ser la 5ta).\n", "incorrecto"))
            retroalimentacion_parts.append(("   * **Paso a seguir:** La quinta de un acorde está a **cuatro pasos ordinales** de la fundamental (ej: Do -> Sol).\n\n", "normal"))
        return [("🛑 **RESULTADO FINAL: ACORDE MAL CONSTRUIDO por ORTOGRAFÍA**\n\n", "incorrecto")] + retroalimentacion_parts
    
    retroalimentacion_parts.append((f"✅ **ORTOGRAFÍA CORRECTA:** La construcción por terceras es válida ({fundamental}, {tercera}, {quinta}).\n\n", "correcto"))

    # CHEQUEO 2: TERCERA
    if semitonos_3ra != regla['3ra']:
        es_correcto = False
        diferencia = semitonos_3ra - regla['3ra']
        retroalimentacion_parts.append((f"❌ **ERROR EN LA TERCERA:** Usaste {semitonos_3ra} semitonos.\n", "incorrecto"))
        retroalimentacion_parts.append((f"   * Requerido: {regla['nombre3ra']} ({regla['3ra']} semitonos).\n", "normal"))
        if diferencia > 0:
            retroalimentacion_parts.append((f"   * **Paso a seguir:** ¡Te **sobró** {diferencia} semitono(s)! Debes **bajar** la nota.\n\n", "normal"))
        else:
            retroalimentacion_parts.append((f"   * **Paso a seguir:** ¡Te **faltó** {-diferencia} semitono(s)! Debes **subir** la nota.\n\n", "normal"))
    else:
        retroalimentacion_parts.append((f"✅ **TERCERA CORRECTA:** {tercera} cumple con los {regla['3ra']} semitonos.\n\n", "correcto"))

    # CHEQUEO 3: QUINTA
    if semitonos_5ta != regla['5ta']:
        es_correcto = False
        diferencia = semitonos_5ta - regla['5ta']
        retroalimentacion_parts.append((f"❌ **ERROR EN LA QUINTA:** Usaste {semitonos_5ta} semitonos.\n", "incorrecto"))
        retroalimentacion_parts.append((f"   * Requerido: {regla['nombre5ta']} ({regla['5ta']} semitonos).\n", "normal"))
        if diferencia > 0:
            retroalimentacion_parts.append((f"   * **Paso a seguir:** ¡Te **sobró** {diferencia} semitono(s)! Debes **bajar** la nota.\n\n", "normal"))
        else:
            retroalimentacion_parts.append((f"   * **Paso a seguir:** ¡Te **faltó** {-diferencia} semitono(s)! Debes **subir** la nota.\n\n", "normal"))
    else:
        retroalimentacion_parts.append((f"✅ **QUINTA CORRECTA:** {quinta} cumple con los {regla['5ta']} semitonos.\n\n", "correcto"))

    if es_correcto:
        return [("🌟🌟🌟 ¡CONSTRUCCIÓN CORRECTA! ¡Excelente trabajo! 🌟🌟🌟\n\n", "titulo_correcto")] + retroalimentacion_parts
    else:
        return [("🛑 **RESULTADO FINAL: ACORDE MAL CONSTRUIDO**\n\n", "incorrecto")] + retroalimentacion_parts

# =================================================================
# INTERFAZ WEB (STREAMLIT)
# =================================================================

st.set_page_config(page_title="Validador de Acordes", page_icon="🎵")

if 'last_attempt' not in st.session_state:
    st.session_state.last_attempt = {"chord": None, "failed": False}

st.title("🎵 Validador de Acordes Tríadas")
st.markdown("Ingresa las notas de tu acorde para verificar si está correctamente construido.")

col1, col2 = st.columns([1, 2])

with col1:
    tipo = st.selectbox("Tipo de Acorde", ["Mayor", "Menor", "Aumentado", "Disminuido"])

with col2:
    fundamental = st.text_input("1. Fundamental (Ej: Do)")
    tercera = st.text_input("2. Tercera (Ej: Mi)")
    quinta = st.text_input("3. Quinta (Ej: Sol)")

if st.button("VALIDAR ACORDE", type="primary"):
    current_chord_tuple = (tipo, fundamental, tercera, quinta)
    resultado_parts = validar_acorde(tipo, fundamental, tercera, quinta)
    
    is_correct = resultado_parts[0][1] == "titulo_correcto"
    mostrar_todo = False
    
    if is_correct:
        st.session_state.last_attempt = {"chord": None, "failed": False}
        mostrar_todo = True
        st.balloons()
    else:
        if st.session_state.last_attempt["failed"] and st.session_state.last_attempt["chord"] == current_chord_tuple:
            mostrar_todo = True
            st.session_state.last_attempt = {"chord": None, "failed": False}
        else:
            st.session_state.last_attempt["failed"] = True
            st.session_state.last_attempt["chord"] = current_chord_tuple
            st.warning("🤔 ¡Casi! Hay un detalle por corregir. Revisa la ortografía o el conteo de semitonos y vuelve a intentar.")
            st.info("💡 PISTA: Si fallas de nuevo, te mostraré el análisis completo.")

    if mostrar_todo:
        st.divider()
        for text, tag in resultado_parts:
            if tag == "titulo_correcto":
                st.success(text)
            elif tag == "incorrecto":
                st.error(text)
            elif tag == "correcto":
                st.markdown(f":green[{text}]")
            else:
                st.markdown(text)