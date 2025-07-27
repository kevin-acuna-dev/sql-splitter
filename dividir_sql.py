import os
import sys
from datetime import datetime

# === Configuration Section ===

# Path to the original large SQL file to be split
archivo_original = "E:/Users/kevin/Documents/backup.sql"

# Output directory where split files will be saved
directorio_salida = "E:/divididos"

# Log file for errors during the process
log_errores = os.path.join(directorio_salida, "errores.log")

# Maximum size (in bytes) for each part (default: 500 MB)
tamano_parte = 500 * 1024 * 1024

# Block size used for reading/writing (default: 8 MB) – avoids memory overload
tamano_bloque = 8 * 1024 * 1024

# === Setup Output Directory ===

# Create output directory if it does not exist
os.makedirs(directorio_salida, exist_ok=True)

# === Resume Support ===

# List and sort existing parts in the output directory to detect progress
partes_existentes = sorted([
    f for f in os.listdir(directorio_salida)
    if f.startswith("parte_") and f.endswith(".sql")
])

# Set the current part number and calculate how many bytes were already processed
parte = len(partes_existentes) + 1
bytes_procesados = sum(os.path.getsize(os.path.join(directorio_salida, f)) for f in partes_existentes)

print(f"🔁 Resuming from byte {bytes_procesados} (part {parte:02})")

try:
    # Open the original file in binary mode and seek to the last processed byte
    entrada = open(archivo_original, 'rb')
    entrada.seek(bytes_procesados)

    # Open the output file in append binary mode for the current part
    salida = open(os.path.join(directorio_salida, f"parte_{parte:02}.sql"), 'ab')
    bytes_actuales = 0  # Tracks bytes written in the current part

    # === Progress Display Function ===
    def mostrar_progreso(parte, total_bytes):
        """
        Display real-time progress in MB for the current part.
        """
        mb = total_bytes / (1024 * 1024)
        sys.stdout.write(f"\r📦 Part {parte:02}: {mb:.2f} MB copied...")
        sys.stdout.flush()

    # === Main Loop: Read original file and write split parts ===
    while True:
        bloque = entrada.read(tamano_bloque)  # Read a block from the source file
        if not bloque:
            break  # End of file

        # If current block would exceed the part size, split it
        if bytes_actuales + len(bloque) > tamano_parte:
            restante = tamano_parte - bytes_actuales  # Calculate space left in current part
            salida.write(bloque[:restante])          # Write the remaining chunk
            salida.close()
            print(f"\n✅ Part {parte:02} ready ({tamano_parte / (1024**2):.2f} MB)")

            # Start a new part
            parte += 1
            salida = open(os.path.join(directorio_salida, f"parte_{parte:02}.sql"), 'wb')
            salida.write(bloque[restante:])          # Write remaining data in new file
            bytes_actuales = len(bloque) - restante  # Reset byte count for new part
        else:
            salida.write(bloque)
            bytes_actuales += len(bloque)

        mostrar_progreso(parte, bytes_actuales)

    # Finalize
    salida.close()
    entrada.close()
    print(f"\n✅ Part {parte:02} ready ({bytes_actuales / (1024**2):.2f} MB)")
    print("🏁 Splitting completed.")

# === Error Handling ===
except Exception as e:
    with open(log_errores, 'a', encoding='utf-8') as log:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log.write(f"[{timestamp}] ERROR: {str(e)}\n")
    print(f"\n❌ Error: {e}")
