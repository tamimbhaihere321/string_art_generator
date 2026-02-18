import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

def export_pins_csv(pins):
    lines=["pin_number,x_mm,y_mm,angle_deg"]
    for p in pins:
        lines.append(f"{p[0]},{p[1]:.2f},{p[2]:.2f},{p[3]:.2f}")
    return "\n".join(lines)

def export_threads_csv(threads):
    lines=["step,from_pin,to_pin"]
    for s,f,t in threads:
        lines.append(f"{s},{f},{t}")
    return "\n".join(lines)

def export_instructions_txt(threads):
    lines=[]
    for s,f,t in threads:
        lines.append(f"Step {s+1}: Pin {f} → Pin {t}")
    return "\n".join(lines)

def generate_drill_template(w,h,pins):

    fig=plt.figure(figsize=(w/100,h/100),dpi=100)
    ax=fig.add_subplot(111)

    ax.set_xlim(0,w)
    ax.set_ylim(h,0)
    ax.set_facecolor("white")

    ax.set_xticks(np.arange(0,w,10))
    ax.set_yticks(np.arange(0,h,10))
    ax.grid(True,linewidth=0.3)

    for p in pins:
        ax.plot(p[1],p[2],'o',markersize=3)
        ax.text(p[1],p[2],str(p[0]),fontsize=4)

    ax.set_title("Drill Template (mm scale)")
    ax.set_aspect('equal')

    buf=BytesIO()
    plt.savefig(buf,format="png",bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()
