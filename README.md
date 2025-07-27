# 🔨 SQL File Splitter (Efficient Large File Divider)

A Python script to efficiently split extremely large `.sql` files (10–100+ GB) into smaller chunks (default: 500 MB) **without loading the file into memory**, and with **safe reusability and resumability**. Ideal for handling broken USBs, unstable disks, or large import/export workflows.

---

## ⚙️ Features

- ✅ Efficient block-based reading and writing (default: 8 MB per I/O operation)
- ✅ Splits by bytes, not lines — no memory overload
- ✅ Automatic resume support if process is interrupted
- ✅ Progress displayed in real time
- ✅ Customizable part size (default: 500 MB)
- ✅ Error logging on write failures
- ✅ Compatible with `.sql`, `.csv`, `.txt`, or any large plain text file

---

## 📈 Why is it efficient?

This script is optimized for both performance and reliability:

| Design Decision               | Benefit                                   |
|------------------------------|-------------------------------------------|
| Binary I/O (`rb`/`wb`)       | Maximum performance, avoids encoding overhead |
| Block reads (8 MB)           | Reduces system calls, increases throughput |
| No full memory loading       | Can process files over 100 GB safely       |
| Resume via part detection    | Prevents reprocessing or corruption        |
| Progress tracking            | Real-time feedback per chunk               |

---

## 💻 Usage

### Requirements
- Python 3.6+

---

### Configuration (inside the script)

```python
archivo_original = "E:/path/to/your/backup.sql"
directorio_salida = "E:/divided_parts"
tamano_parte = 500 * 1024 * 1024  # 500 MB
tamano_bloque = 8 * 1024 * 1024   # 8 MB
```

You can customize:
- `archivo_original`: Input file path
- `directorio_salida`: Output directory
- `tamano_parte`: Max size per part (default: 500 MB)
- `tamano_bloque`: Read/write block size (default: 8 MB)

---

### Run the script

```bash
python dividir_sql.py
```

Parts will be generated as:

```
parte_01.sql, parte_02.sql, parte_03.sql, ...
```

in the output directory you specified.

---

## 🔁 Resume Support

If the script is interrupted (e.g., system crash, power loss, USB disconnection), you can re-run it and it will automatically:

- Detect already-created `.sql` parts
- Calculate how many bytes were successfully copied
- Resume from the last completed byte
- Avoid duplications or corruption

---

## 🧪 Example Use Case

You have a damaged or unstable USB drive that crashes after writing more than 2 GB.  
This script allows you to copy small parts (e.g., 500 MB) safely, eject the USB, reconnect, and continue the process part by part — with zero corruption risk.

---

## 📄 Output

- `parte_01.sql`, `parte_02.sql`, ..., until the file ends
- `errores.log`: If write failures or I/O exceptions occur, details will be logged here

---

## 🛡️ Limitations

- ❗ Not SQL syntax-aware — the file is split by **byte size**, not by SQL statements
- ⚠️ Use caution if your `.sql` contains multi-line transactions (e.g., large `INSERT` blocks), as splitting may occur mid-statement

---

## 📚 License

MIT License. Use freely. Contributions welcome.

---

## 👤 Author

Created by `kevin-acuna-dev`.  
Feedback or improvements are welcome through issues or pull requests.
