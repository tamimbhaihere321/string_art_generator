import numpy as np

def generate_pin_layout(w,h,margin,count,layout):

    pins=[]

    if layout=="circular":

        cx=w/2
        cy=h/2
        r=min(w,h)/2-margin

        angles=np.linspace(0,2*np.pi,count,endpoint=False)
        angles=(angles-np.pi/2)%(2*np.pi)  # start top center clockwise

        for i,a in enumerate(angles):
            x=cx+r*np.cos(a)
            y=cy+r*np.sin(a)
            pins.append((i,x,y,np.degrees(a)))

    else:

        per=2*((w-2*margin)+(h-2*margin))
        distances=np.linspace(0,per,count,endpoint=False)

        for i,d in enumerate(distances):

            if d < (w-2*margin):
                x=margin+d
                y=margin

            elif d < (w-2*margin)+(h-2*margin):
                x=w-margin
                y=margin+(d-(w-2*margin))

            elif d < 2*(w-2*margin)+(h-2*margin):
                x=w-margin-(d-(w-2*margin)-(h-2*margin))
                y=h-margin

            else:
                x=margin
                y=h-margin-(d-2*(w-2*margin)-(h-2*margin))

            pins.append((i,x,y,0))

    return pins
