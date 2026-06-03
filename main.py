import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# ۱. تعریف فرمول ریاضی مایکلس-منتن برای فیت کردن داده‌ها
def michaelis_menten(S, Vmax, Km):
    return (Vmax * S) / (Km + S)

def main():
    print("--- Enzyme Kinetics Analyzer ---")
    
    # ۲. خواندن داده‌های آزمایشگاهی از فایل CSV
    try:
        data = pd.read_csv('enzyme_data.csv')
        S_data = data['Substrate_Concentration'].values
        v_data = data['Reaction_Velocity'].values
        print("✅ Laboratory data loaded successfully.")
    except Exception as e:
        print(f"❌ Error loading 'enzyme_data.csv': {e}")
        return

    # ۳. تخمین دقیق مقادیر Vmax و Km با الگوریتم غیرخطی Least Squares
    # حدس اولیه: Vmax ماکزیمم سرعت داده‌ها و Km غلظت میانی است
    initial_guess = [max(v_data), np.median(S_data)]
    
    popt, _ = curve_fit(michaelis_menten, S_data, v_data, p0=initial_guess)
    Vmax_est, Km_est = popt
    
    print(f"\n📊 Calculated Kinetics Parameters:")
    print(f"  - Vmax = {Vmax_est:.3f}")
    print(f"  - Km   = {Km_est:.3f}")

    # ۴. رسم منحنی فیت‌شده و ذخیره تصویر نمودار
    plt.figure(figsize=(8, 5))
    plt.scatter(S_data, v_data, color='red', label='Experimental Data (Points)', zorder=5)
    
    # ساخت یک محور پیوسته برای رسم منحنی نرم مایکلس-منتن
    S_fit = np.linspace(0, max(S_data) * 1.1, 200)
    v_fit = michaelis_menten(S_fit, Vmax_est, Km_est)
    
    plt.plot(S_fit, v_fit, color='blue', label=f'Michaelis-Menten Fit\n(Vmax={Vmax_est:.2f}, Km={Km_est:.2f})')
    plt.title('Enzyme Kinetics: Reaction Velocity vs Substrate Concentration')
    plt.xlabel('Substrate Concentration [S]')
    plt.ylabel('Reaction Velocity (v)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    
    plot_filename = 'kinetics_plot.png'
    plt.savefig(plot_filename, dpi=300)
    plt.close()
    print(f"✅ Kinetics curve graph saved as '{plot_filename}'.")

    # ۵. تولید خودکار گزارش نهایی PDF
    pdf_filename = 'Enzyme_Kinetics_Report.pdf'
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, 750, "Enzyme Kinetics Analysis Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, 730, "Automated Evaluation using Michaelis-Menten Model")
    c.line(50, 715, 550, 715)
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 680, "1. Estimated Parameters:")
    c.setFont("Helvetica", 12)
    c.drawString(70, 655, f"Maximum Velocity (Vmax):  {Vmax_est:.4f}")
    c.drawString(70, 635, f"Michaelis Constant (Km):   {Km_est:.4f}")
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 590, "2. Kinetics Saturation Curve:")
    
    # قرار دادن تصویر نمودار تولید شده در داخل فایل PDF
    c.drawImage(plot_filename, 50, 220, width=500, height=312)
    
    c.line(50, 150, 550, 150)
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 130, "Report generated automatically by Enzyme Kinetics Analyzer project.")
    
    c.save()
    print(f"✅ Final PDF report successfully generated as '{pdf_filename}'.")
    print("\n🎉 All steps completed successfully!")

if __name__ == "__main__":
    main()