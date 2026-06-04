import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

# ۱. تعریف فرمول ریاضی مایکلس-منتن برای فیت کردن داده‌ها
def michaelis_menten(S, Vmax, Km):
    return (Vmax * S) / (Km + S)

def main():
    print("--- Enzyme Kinetics Analyzer ---")
    
    # ۲. گرفتن نام فایل از کاربر
    file_name = input("Please enter the CSV file name (e.g., beta_gal_lactose.csv): ").strip()
    
    # بررسی اینکه آیا فایل وجود دارد یا خیر
    if not os.path.exists(file_name):
        print(f"❌ Error: The file '{file_name}' does not exist in this folder!")
        return

    # استخراج نام پایه فایل برای نام‌گذاری خروجی‌ها (مثلاً حذف پسوند .csv)
    base_name = os.path.splitext(file_name)[0]

    # ۳. خواندن داده‌های آزمایشگاهی از فایل وارد شده
    try:
        data = pd.read_csv(file_name)
        S_data = data['Substrate_Concentration'].values
        v_data = data['Reaction_Velocity'].values
        print(f"✅ Data from '{file_name}' loaded successfully.")
    except Exception as e:
        print(f"❌ Error reading the file: {e}")
        return

    # ۴. تخمین دقیق مقادیر Vmax و Km با الگوریتم غیرخطی Least Squares
    initial_guess = [max(v_data), np.median(S_data)]
    
    try:
        popt, _ = curve_fit(michaelis_menten, S_data, v_data, p0=initial_guess)
        Vmax_est, Km_est = popt
    except Exception as e:
        print(f"❌ Mathematical fitting failed. Check your data points! Error: {e}")
        return
    
    print(f"\n📊 Calculated Kinetics Parameters for [{base_name}]:")
    print(f"  - Vmax = {Vmax_est:.3f}")
    print(f"  - Km   = {Km_est:.3f}")

    # ۵. رسم منحنی فیت‌شده و ذخیره تصویر نمودار با نام اختصاصی
    plt.figure(figsize=(8, 5))
    plt.scatter(S_data, v_data, color='red', label='Experimental Data (Points)', zorder=5)
    
    S_fit = np.linspace(0, max(S_data) * 1.1, 200)
    v_fit = michaelis_menten(S_fit, Vmax_est, Km_est)
    
    plt.plot(S_fit, v_fit, color='blue', label=f'Michaelis-Menten Fit\n(Vmax={Vmax_est:.2f}, Km={Km_est:.2f})')
    plt.title(f'Enzyme Kinetics Analysis: {base_name}')
    plt.xlabel('Substrate Concentration [S]')
    plt.ylabel('Reaction Velocity (v)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    
    plot_filename = f'plot_{base_name}.png'
    plt.savefig(plot_filename, dpi=300)
    plt.close()
    print(f"✅ Kinetics curve graph saved as '{plot_filename}'.")

    # ۶. تولید خودکار گزارش نهایی PDF با نام اختصاصی پروژه
    pdf_filename = f'Report_{base_name}.pdf'
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, 750, "Enzyme Kinetics Analysis Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, 730, f"Project / Enzyme ID: {base_name}")
    c.line(50, 715, 550, 715)
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 680, "1. Estimated Parameters:")
    c.setFont("Helvetica", 12)
    c.drawString(70, 655, f"Maximum Velocity (Vmax):  {Vmax_est:.4f}")
    c.drawString(70, 635, f"Michaelis Constant (Km):   {Km_est:.4f}")
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 590, "2. Kinetics Saturation Curve:")
    
    # قرار دادن تصویر نمودار در فایل PDF
    c.drawImage(plot_filename, 50, 220, width=500, height=312)
    
    c.line(50, 150, 550, 150)
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 130, f"Report generated automatically from source file: {file_name}")
    
    c.save()
    print(f"✅ Final PDF report successfully generated as '{pdf_filename}'.")
    print(f"\n🎉 Analysis for '{base_name}' completed successfully!")

if __name__ == "__main__":
    main()