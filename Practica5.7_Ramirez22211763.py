"""
Práctica 1: Diseño de controladores
﻿
Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México
﻿
Nombre del alumno: Porfirio Emmanuel Ramirez Barajas
Número de control: 22211763
Correo institucional: l22211763@tectijuana.edu.mx
﻿
Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
# !pip install control
# !pip install slycot


# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import math as m 
import matplotlib.pyplot as plt
import control as ctrl


# Datos de la simulación

x0, t0, tend, dt, w, h = 0,0,10, 1E-3, 7, 3.5
n = round ((tend - t0)/dt) + 1
t = np.linspace(t0, tend, n)
#u1 = np.ones(n)
u = np.zeros(n); u [round(1/dt):round (2/dt)]=1
#u3 = t/tend 
#u4 = np.sin(m.pi/2*t)

def muscle(a,Cs,Cp,R):
    num = [Cs*R,1-a]
    den = [R*(Cs+Cp), 1]
    sys = ctrl.tf(num,den)    
    return sys

#Funcion de transferencia: Control
a,Cs,Cp,R = 0.25, 10E-6, 100E-6,100
syscontrol = muscle(a,Cs,Cp,R)
print(f'Funcion de transferencia de control: {syscontrol}')

#Funcion de transferencia: Caso
a,Cs,Cp,R = 0.25, 10E-6, 100E-6,10E3
syscaso = muscle(a,Cs,Cp,R)
print(f'Funcion de transferencia de control: {syscaso}')

#Respuestas en lazo abierto
_,Pp0 = ctrl.forced_response(syscontrol,t,u,x0)
_,Pp1 = ctrl.forced_response(syscaso,t,u,x0)

clr1 = np.array([0,0,0])/255
clr2 = np.array([50,20,177])/255
clr3 = np.array([115,158,201])/255
clr4 = np.array([100,175,219])/255

fg1 = plt.figure()
plt.plot(t,Pp0,'-',linewidth=1,color=clr1,label= 'Fs1. Control')
plt.plot(t,Pp1,'-',linewidth=1,color= clr2,label= 'Fs2. Caso')
plt.plot(t,u,'-',linewidth=1,color=clr3,label= 'Fs. Impulso')
plt.grid(False)
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(-0.6,1.4); plt.yticks(np.arange(-0.6,1.6,0.2))
plt.xlabel('F(t) [V]')
plt.ylabel('t [s]')
plt.legend(bbox_to_anchor=(0.5,-0.2),loc='center',ncol=3)
plt.show()
fg1.set_size_inches(w,h)
fg1.tight_layout()
fg1.savefig('sistema musculoesqueletico lazo abierto python.png',dpi=600,bbox_inches='tight')
fg1.savefig('sistema musculoesqueletivo python.pdf')

#Controlador PI
def controlador(kP,kI,sys):
    Cr=1E-6
    Re = 1/(kI*Cr)
    Rr = kP*Re
    numPI = [Rr*Cr,1]
    denPI = [Re*Cr,0]
    PI = ctrl.tf(numPI,denPI)
    X = ctrl.series(PI,sys)
    sysPI = ctrl.feedback(X,1,sign=-1)
    return sysPI

PID = controlador(0.221570830487689,3595.7467274765,syscaso)

#Respuestas en lazo cerrado
_,Pp3 = ctrl.forced_response(PID,t,u,x0)


fg2 = plt.figure()
plt.plot(t,Pp0,'-',linewidth=1,color=clr1,label= 'Fs1. Control')
plt.plot(t,Pp1,'-',linewidth=1,color= clr2,label= 'Fs2. Caso')
plt.plot(t,u,'-',linewidth=1,color=clr3,label= 'Fs. Impulso')
plt.plot(t,Pp3,'-',linewidth=1,color= clr4,label= 'PI')

plt.grid(False)
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(-0.6,1.4); plt.yticks(np.arange(-0.6,1.6,0.2))
plt.xlabel('Pp(t) [V]')
plt.ylabel('t [s]')
plt.legend(bbox_to_anchor=(0.5,-0.2),loc='center',ncol=3)
plt.show()
fg2.set_size_inches(w,h)
fg2.tight_layout()
fg2.savefig('sistema cardiovascular Lazo cerrado python.png',dpi=600,bbox_inches='tight')
fg2.savefig('sistema cardiovascular Lazo cerrado python.pdf')

