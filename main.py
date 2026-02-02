import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os

class ParquetConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Parquet to CSV Converter")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        # Variables
        self.parquet_path = tk.StringVar()
        self.csv_path = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Title
        title = ttk.Label(self.root, text="Cisco Parquet to CSV Converter", font=("Arial", 16, "bold"))
        title.pack(pady=20)

        # Input Parquet
        ttk.Label(self.root, text="Input Parquet File:").pack(anchor="w", padx=40, pady=(10,5))
        ttk.Entry(self.root, textvariable=self.parquet_path, width=60).pack(padx=40)
        ttk.Button(self.root, text="Browse...", command=self.browse_parquet).pack(pady=5)

        # Output CSV
        ttk.Label(self.root, text="Output CSV File:").pack(anchor="w", padx=40, pady=(15,5))
        ttk.Entry(self.root, textvariable=self.csv_path, width=60).pack(padx=40)
        ttk.Button(self.root, text="Browse...", command=self.browse_csv).pack(pady=5)

        # Convert Button
        ttk.Button(self.root, text="Convert Parquet → CSV", 
                  command=self.convert, style="Accent.TButton").pack(pady=25)

    def browse_parquet(self):
        filename = filedialog.askopenfilename(
            title="Select Parquet File",
            filetypes=[("Parquet files", "*.parquet *.parq")]
        )
        if filename:
            self.parquet_path.set(filename)
            # Auto-suggest CSV output name
            default_csv = os.path.splitext(filename)[0] + ".csv"
            self.csv_path.set(default_csv)

    def browse_csv(self):
        filename = filedialog.asksaveasfilename(
            title="Save CSV As",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if filename:
            self.csv_path.set(filename)

    def convert(self):
        parquet_file = self.parquet_path.get()
        csv_file = self.csv_path.get()

        if not parquet_file:
            messagebox.showerror("Error", "Please select a Parquet file")
            return
        if not csv_file:
            messagebox.showerror("Error", "Please select output CSV location")
            return

        try:
            self.root.config(cursor="watch")
            self.root.update()

            df = pd.read_parquet(parquet_file)
            df.to_csv(csv_file, index=False)

            messagebox.showinfo("Success", 
                f"Successfully converted!\n\n"
                f"Rows: {len(df):,}\n"
                f"Columns: {list(df.columns)}\n\n"
                f"Saved to:\n{csv_file}")

        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed:\n\n{str(e)}")
        finally:
            self.root.config(cursor="")

if __name__ == "__main__":
    root = tk.Tk()
    app = ParquetConverter(root)
    root.mainloop()
