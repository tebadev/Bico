import os
from modules.recorder import AudioUtilidades, inicializador

# ── Configuración por defecto ──────────────────────────────────────────────────
FRECUENCIA   = 44100
CANALES      = 1
DIRECTORIO   = "grabaciones"
FORMATO      = "wav"

# ── Helpers de consola ─────────────────────────────────────────────────────────
def limpiar():
    os.system("cls" if os.name == "nt" else "clear")

def cabecera():
    print("╔══════════════════════════════╗")
    print("║          GRABADORA           ║")
    print("╚══════════════════════════════╝\n")

def seleccionar_microfono():
    """Muestra los micrófonos disponibles y deja elegir al usuario."""
    micros = AudioUtilidades.detectar_microfonos()

    if not micros:
        print("No se encontraron micrófonos.")
        return None

    print("Micrófonos disponibles:\n")
    for idx, nombre in micros:
        print(f"  [{idx}] {nombre}")

    print()
    while True:
        entrada = input("Elige un número (Enter = predeterminado): ").strip()
        if entrada == "":
            return None
        if entrada.isdigit() and int(entrada) in [i for i, _ in micros]:
            return int(entrada)
        print("  Número no válido, intenta de nuevo.")

# ── Flujo de grabación ─────────────────────────────────────────────────────────
def flujo_grabacion(dispositivo_id):
    """Maneja el ciclo grabar → pausar/reanudar → detener → guardar."""
    limpiar()
    cabecera()

    print("Iniciando grabación… (Ctrl+C para cancelar)\n")
    grabadora = inicializador(FRECUENCIA, CANALES, dispositivo_id)
    print("Grabando\n")

    try:
        while True:
            print("Opciones:  [p] Pausar   [r] Reanudar   [s] Detener y guardar")
            cmd = input("→ ").strip().lower()

            if cmd == "p":
                grabadora.pausar()
                print("Pausado\n")

            elif cmd == "r":
                grabadora.reanudar()
                print("Grabando\n")

            elif cmd == "s":
                grabadora.detener()
                print("\nGrabación detenida.")
                break

            else:
                print("Comando no reconocido.\n")

    except KeyboardInterrupt:
        grabadora.detener()
        print("\n  Grabación cancelada.")
        return

    # ── Guardar archivo ────────────────────────────────────────────────────────
    if not grabadora.archivo_temporal or not os.path.exists(grabadora.archivo_temporal):
        print("  No hay audio para guardar.")
        return

    nombre = input("\nNombre del archivo (sin extensión): ").strip()
    if not nombre:
        nombre = "grabacion"
    FORMATOS = ["wav", "flac", "ogg", "mp3"]
    print("\nFormatos disponibles: " + ", ".join(FORMATOS))
    formato = input("Formato (Enter = wav): ").strip().lower()
    if formato not in FORMATOS:
        formato = "wav"

    AudioUtilidades.guardar_archivo(
        ruta_origen=grabadora.archivo_temporal,
        directorio_destino=DIRECTORIO,
        nombre_final=nombre,
        formato=formato,
    )
    print(f"\nGuardado en: {DIRECTORIO}/{nombre}.{FORMATO}\n")

# ── Menú principal ─────────────────────────────────────────────────────────────
def menu():
    dispositivo_id = None   # Se elige una vez y se reutiliza

    while True:
        limpiar()
        cabecera()
        print(f"  Dispositivo : {'Predeterminado' if dispositivo_id is None else dispositivo_id}")
        print(f"  Directorio  : {DIRECTORIO}")
        print(f"  Formato     : {FORMATO}\n")
        print("  [1] Nueva grabación")
        print("  [2] Cambiar micrófono")
        print("  [3] Salir\n")

        opcion = input("→ ").strip()

        if opcion == "1":
            flujo_grabacion(dispositivo_id)
            input("Pulsa Enter para continuar…")

        elif opcion == "2":
            limpiar()
            cabecera()
            dispositivo_id = seleccionar_microfono()

        elif opcion == "3":
            print("\nHasta luego.\n")
            break

        else:
            print("  Opción no válida.\n")

# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    menu()
