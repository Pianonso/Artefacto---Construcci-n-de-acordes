import tkinter as tk
from tkinter import ttk, messagebox

# =================================================================
# LÓGICA DE VALIDACIÓN DEL ARTEFACTO (Tu Código de Python)
# Versión: Retroalimentación Mínima (Fallo en Conteo)
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
    tercera_correcta = False
    quinta_correcta = False
    
    regla = REGLAS_ACORDES.get(tipoSolicitado)
    if not regla:
        return f"🛑 ERROR: El tipo de acorde '{tipoSolicitado}' no es válido."

    if not all(nota in MAPA_NOTAS for nota in [fundamental, tercera, quinta]):
        return [("🛑 ERROR DE ENTRADA: Una o más notas ('{fundamental}', '{tercera}', '{quinta}') no son válidas. Revise la notación.", "error_entrada")]

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
    
    # --- CHEQUEO 1: ORTOGRAFÍA ---
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
    retroalimentacion_parts.append(("--- ANÁLISIS DE LA CALIDAD DEL INTERVALO ---\n\n", "normal"))

    # --- CHEQUEO 2: TERCERA (Retroalimentación Mínima) ---
    if semitonos_3ra != regla['3ra']:
        es_correcto = False
        diferencia = semitonos_3ra - regla['3ra']
        
        retroalimentacion_parts.append((f"❌ **ERROR EN LA TERCERA:** Usaste {semitonos_3ra} semitonos.\n", "incorrecto"))
        retroalimentacion_parts.append((f"   * Requerido: {regla['nombre3ra']} ({regla['3ra']} semitonos).\n", "normal"))
        if diferencia > 0:
            retroalimentacion_parts.append((f"   * **Paso a seguir:** ¡Te **sobró** {diferencia} semitono(s)! Debes **bajar** la nota {diferencia} semitono(s).\n\n", "normal"))
        else:
            retroalimentacion_parts.append((f"   * **Paso a seguir:** ¡Te **faltó** {-diferencia} semitono(s)! Debes **subir** la nota {-diferencia} semitono(s).\n\n", "normal"))
    else:
        tercera_correcta = True
        retroalimentacion_parts.append((f"✅ **TERCERA CORRECTA:** {tercera} es la nota requerida, cumpliendo con la ortografía y los {regla['3ra']} semitonos.\n\n", "correcto"))

    # --- CHEQUEO 3: QUINTA (Retroalimentación Mínima) ---
    if semitonos_5ta != regla['5ta']:
        es_correcto = False
        diferencia = semitonos_5ta - regla['5ta']
        retroalimentacion_parts.append((f"❌ **ERROR EN LA QUINTA:** Usaste {semitonos_5ta} semitonos.\n", "incorrecto"))
        retroalimentacion_parts.append((f"   * Requerido: {regla['nombre5ta']} ({regla['5ta']} semitonos).\n", "normal"))
        if diferencia > 0:
            retroalimentacion_parts.append((f"   * **Paso a seguir:** ¡Te **sobró** {diferencia} semitono(s)! Debes **bajar** la nota {diferencia} semitono(s).\n\n", "normal"))
        else:
            retroalimentacion_parts.append((f"   * **Paso a seguir:** ¡Te **faltó** {-diferencia} semitono(s)! Debes **subir** la nota {-diferencia} semitono(s).\n\n", "normal"))
    else:
        quinta_correcta = True
        retroalimentacion_parts.append((f"✅ **QUINTA CORRECTA:** {quinta} es la nota requerida, cumpliendo con la ortografía y los {regla['5ta']} semitonos.\n\n", "correcto"))

    # --- Veredicto Final ---
    if es_correcto:
        return [("🌟🌟🌟 ¡CONSTRUCCIÓN CORRECTA! ¡Excelente trabajo! 🌟🌟🌟\n\n", "titulo_correcto")] + retroalimentacion_parts
    else:
        resumen_aciertos = []
        if tercera_correcta: resumen_aciertos.append("la Tercera")
        if quinta_correcta: resumen_aciertos.append("la Quinta")
            
        aciertos_msg = ""
        if not resumen_aciertos:
             aciertos_msg = ("😔 El error fue en la construcción de los intervalos. ¡Repasa el conteo de semitonos!\n", "normal")
        else:
            aciertos_msg = (f"🙌 **RECONOCIMIENTO POSITIVO:** Lograste que {' y '.join(resumen_aciertos)} fuera **correcta**.\n", "correcto")

        return [("🛑 **RESULTADO FINAL: ACORDE MAL CONSTRUIDO**\n\n", "incorrecto"), aciertos_msg, ("\n", "normal")] + retroalimentacion_parts


# =================================================================
# CÓDIGO DE INTERFAZ GRÁFICA (TKINTER)
# =================================================================

# --- Paleta de Colores y Fuentes ---
PALETA = {
    "fondo": "#F0F0F0",      # Gris claro estándar
    "fondo_widget": "#FFFFFF", # Blanco
    "texto": "#000000",      # Negro
    "primario": "#007ACC",
    "exito": "#28A745",
    "error": "#DC3545",
    "texto_exito": "#155724", # Verde oscuro
    "texto_error": "#721c24",  # Rojo oscuro
    "texto_widget": "#000000" # Negro
}

# --- Variables de Estado para Retroalimentación Pedagógica ---
last_attempt = {"chord": None, "failed": False}


def ejecutar_validacion():
    """Toma los datos de la GUI, llama a la función validar_acorde y muestra el resultado."""
    try:
        tipo = tipo_var.get()
        fundamental = fundamental_entry.get()
        tercera = tercera_entry.get()
        quinta = quinta_entry.get()

        current_chord_tuple = (tipo, fundamental, tercera, quinta)
        resultado_parts = validar_acorde(tipo, fundamental, tercera, quinta)
        is_correct = resultado_parts[0][1] == "titulo_correcto"
        
        # Configurar tags de color
        resultado_text.tag_configure("normal", foreground=PALETA['texto'])
        resultado_text.tag_configure("correcto", foreground=PALETA['texto_exito'])
        resultado_text.tag_configure("incorrecto", foreground=PALETA['texto_error'])
        resultado_text.tag_configure("titulo_correcto", foreground=PALETA['texto_exito'], font=(FONT_FAM, FONT_SIZE, 'bold'))
        resultado_text.tag_configure("pista", foreground=PALETA['primario'], font=(FONT_FAM, FONT_SIZE, 'bold'))

        # Limpiar el cuadro de texto
        resultado_text.delete('1.0', tk.END)

        if is_correct:
            # Si es correcto, mostrar feedback positivo y resetear estado
            for texto, tag in resultado_parts:
                resultado_text.insert(tk.END, texto, tag)
            last_attempt["failed"] = False
            last_attempt["chord"] = None
        else:
            # Si es incorrecto, aplicar lógica pedagógica
            if last_attempt["failed"] and last_attempt["chord"] == current_chord_tuple:
                # Segundo fallo consecutivo: mostrar retroalimentación completa
                for texto, tag in resultado_parts:
                    resultado_text.insert(tk.END, texto, tag)
                # Resetear estado después de dar la respuesta completa
                last_attempt["failed"] = False
                last_attempt["chord"] = None
            else:
                # Primer fallo: dar solo una pista
                is_spelling_error = "ORTOGRAFÍA" in resultado_parts[0][0]
                pista_msg = "Puede ser un error al contar los semitonos."
                if is_spelling_error:
                    pista_msg = "Parece que hay un error en la ortografía del acorde (construcción por terceras)."
                
                resultado_text.insert(tk.END, "🤔 ¡Casi! Hay un detalle por corregir.\n\n", "pista")
                resultado_text.insert(tk.END, f"PISTA: {pista_msg}\n\n", "normal")
                resultado_text.insert(tk.END, "Revisa tu construcción y presiona 'VALIDAR' de nuevo.", "normal")
                last_attempt["failed"] = True
                last_attempt["chord"] = current_chord_tuple

    except Exception as e:
        messagebox.showerror("Error de Ejecución", f"Ocurrió un error inesperado: {e}")

def limpiar_campos():
    """Limpia todos los campos de entrada y el área de resultados."""
    fundamental_entry.delete(0, tk.END)
    tercera_entry.delete(0, tk.END)
    quinta_entry.delete(0, tk.END)
    resultado_text.delete('1.0', tk.END)
    tipo_var.set("Mayor")
    # Restablecer el color de fondo original del cuadro de texto
    resultado_text.config(background=PALETA['fondo_widget'], foreground=PALETA['texto'])
    fundamental_entry.focus() # Pone el cursor en el primer campo
    
# --- Configuración de la Ventana Principal ---
root = tk.Tk()
root.title("Validador de Acordes Tríadas")

# Configurar estilo para que se vea mejor
style = ttk.Style()
style.theme_use('clam') # Un tema base más moderno

# Configuraciones globales de estilo
FONT_FAM = "Segoe UI"
FONT_SIZE = 12

style.configure(".", background=PALETA['fondo'], foreground=PALETA['texto'], font=(FONT_FAM, FONT_SIZE))
style.configure("TFrame", background=PALETA['fondo'])
style.configure("TLabel", padding=5, background=PALETA['fondo'], foreground=PALETA['texto'])
style.configure("TButton", padding=8, font=(FONT_FAM, FONT_SIZE, 'bold'), background=PALETA['primario'], foreground='white')
style.map("TButton", background=[('active', '#005f9e')])

style.configure("TEntry", fieldbackground=PALETA['fondo_widget'], foreground=PALETA['texto_widget'], borderwidth=0)
style.configure("TCombobox", fieldbackground=PALETA['fondo_widget'], foreground=PALETA['texto_widget'], borderwidth=0)

# Para que el menú desplegable también tenga el estilo oscuro
root.option_add('*TCombobox*Listbox.background', PALETA['fondo_widget'])
root.option_add('*TCombobox*Listbox.foreground', PALETA['texto'])
root.option_add('*TCombobox*Listbox.selectBackground', PALETA['primario'])

# Variables de control
tipo_var = tk.StringVar(root)
tipo_var.set("Mayor") 

# Frame principal con padding
main_frame = ttk.Frame(root, padding="25")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
main_frame.columnconfigure(1, weight=1) # Permite que la columna de entradas se expanda

# --- Elementos de la GUI ---

# 1. Tipo de Acorde (Dropdown)
ttk.Label(main_frame, text="Acorde a Construir:").grid(row=0, column=0, sticky=tk.W, pady=5)
tipos_acordes = ["Mayor", "Menor", "Aumentado", "Disminuido"]
tipo_menu = ttk.Combobox(main_frame, textvariable=tipo_var, values=tipos_acordes, state="readonly", font=(FONT_FAM, FONT_SIZE))
tipo_menu.grid(row=0, column=1, sticky=(tk.W, tk.E))

# 2. Fundamental (Campo de entrada)
ttk.Label(main_frame, text="1. Fundamental: (Ej: Do)").grid(row=1, column=0, sticky=tk.W, pady=5)
fundamental_entry = ttk.Entry(main_frame, font=(FONT_FAM, FONT_SIZE))
fundamental_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))

# 3. Tercera (Campo de entrada)
ttk.Label(main_frame, text="2. Tercera: (Ej: Mi)").grid(row=2, column=0, sticky=tk.W, pady=5)
tercera_entry = ttk.Entry(main_frame, font=(FONT_FAM, FONT_SIZE))
tercera_entry.grid(row=2, column=1, sticky=(tk.W, tk.E))

# 4. Quinta (Campo de entrada)
ttk.Label(main_frame, text="3. Quinta: (Ej: Sol)").grid(row=3, column=0, sticky=tk.W, pady=5)
quinta_entry = ttk.Entry(main_frame, font=(FONT_FAM, FONT_SIZE))
quinta_entry.grid(row=3, column=1, sticky=(tk.W, tk.E))

# 5. Botones de Acción en un frame propio
button_frame = ttk.Frame(main_frame)
button_frame.grid(row=4, column=0, columnspan=2, pady=20, sticky=(tk.W, tk.E))
button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(1, weight=1)

ttk.Button(button_frame, text="VALIDAR", command=ejecutar_validacion).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
ttk.Button(button_frame, text="Limpiar", command=limpiar_campos, style="TButton").grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))

# 6. Área de Resultados (Caja de Texto)
ttk.Label(main_frame, text="Retroalimentación:").grid(row=5, column=0, sticky=tk.W, pady=5)
resultado_text = tk.Text(main_frame, height=17, width=80, padx=10, pady=10, font=(FONT_FAM, FONT_SIZE), relief="flat",
                         background=PALETA['fondo_widget'], foreground=PALETA['texto'], borderwidth=0)
resultado_text.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E))

# Iniciar el bucle de la aplicación
root.mainloop()