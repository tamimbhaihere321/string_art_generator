import numpy as np
import cv2

def line_pixels(p1,p2,size):
    mask=np.zeros((size,size),np.uint8)
    cv2.line(mask,p1,p2,255,1)
    return np.where(mask>0)

def generate_string_art(img,pins,max_lines,darkness,thickness,progress_callback=None):

    size=img.shape[0]

    max_x=max(p[1] for p in pins)
    max_y=max(p[2] for p in pins)

    pin_pts=[(
        int(p[1]/max_x*(size-1)),
        int(p[2]/max_y*(size-1))
    ) for p in pins]

    # ---- CACHE LINES ----
    cache={}
    for i in range(len(pin_pts)):
        for j in range(i+1,len(pin_pts)):
            cache[(i,j)]=line_pixels(pin_pts[i],pin_pts[j],size)

    canvas=np.ones_like(img)
    threads=[]
    current=0

    LIVE_INTERVAL=max(1,max_lines//200)

    for step in range(max_lines):

        best=None
        best_err=0

        for j in range(len(pin_pts)):
            if j==current:
                continue

            key=(min(current,j),max(current,j))
            ys,xs=cache[key]

            err=np.sum(img[ys,xs]-canvas[ys,xs])

            if err>best_err:
                best_err=err
                best=j

        if best is None:
            break

        ys,xs=cache[(min(current,best),max(current,best))]
        canvas[ys,xs]-=darkness
        canvas=np.clip(canvas,0,1)

        threads.append((step,current,best))
        current=best

        # ---- LIVE UPDATE ----
        if progress_callback and (step % LIVE_INTERVAL==0 or step==max_lines-1):

            preview=(canvas*255).astype(np.uint8)
            preview=cv2.cvtColor(preview,cv2.COLOR_GRAY2RGB)

            progress_callback((step+1)/max_lines, preview, step+1)

    preview=(canvas*255).astype(np.uint8)
    preview=cv2.cvtColor(preview,cv2.COLOR_GRAY2RGB)

    return preview,threads
  
