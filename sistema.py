from CoolProp.CoolProp import PropsSI

"""
Dados de entrada
"""
Tamb=32+273
TRFR=5+273
ROT=60
VOL=10E-06
ETA_g=0.6
ETA_v=0.7
UAcomp=2
Tsup=3
UAcond=10
Tsub=3
e=0.8
UAevap=10
UARFR=1.2
"""
Chute inicial Tevap
"""
Tliminfevap=PropsSI("Ttriple","isobutane")
Tlimsupevap=TRFR
Tevap=(Tliminfevap+Tlimsupevap)/2
"""
Chute inicial Tcond
"""
Tliminfcond = Tamb
Tlimsupcond = 70+273
Tcond = (Tliminfcond+Tlimsupcond)/2
"""
Pressoes
"""
Pcond=PropsSI("P","T", Tcond,"Q",1,"isobutane")
Pevap=PropsSI("P","T", Tevap,"Q",1,"isobutane")
"""
Temperaturas
"""
T10=(Tevap+Tsup)+e*(Tcond-Tsub-(Tevap+Tsup))

"""
No compressor
"""
v1=1/PropsSI("D","P",Pevap,"T",T10,"isobutane")
mdot=(ROT*VOL*ETA_v)/v1
h1=PropsSI("H","P",Pevap,"T",T10,"isobutane")
s1=PropsSI("S","P",Pevap,"T",T10,"isobutane")
h2s=PropsSI("H","T",Tcond,"S",s1,"isobutane")
POT=mdot*(h2s-h1)/ETA_g
h2a=h1+POT/mdot
T2a=PropsSI("T","P",Pcond,"H",h2a,"isobutane")
Qcomp=UAcomp*(T2a-Tamb)
h2=h1+(POT-Qcomp)/mdot
"""
condensador
"""
T3=Tcond-Tsub
h3=PropsSI("H","T",T3 ,"P",Pcond,"isobutane")
QR=mdot*(h2-h3)
QAR=UAcond*(Tcond-Tamb)
while (abs(QR - QAR)/QR > 0.0001):
    if (QAR > QR):
        Tlimsupcond = Tcond
    else:
        Tliminfcond = Tcond
    Tcond = (Tliminfcond+Tlimsupcond)/2
    Pcond=PropsSI("P","T", Tcond,"Q",1,"isobutane")
    h2s=PropsSI("H","T",Tcond,"S",s1,"isobutane")
    POT=mdot*(h2s-h1)/ETA_g
    h2a=h1+POT/mdot
    T2a=PropsSI("T","P",Pcond,"H",h2a,"isobutane")
    Qcomp=UAcomp*(T2a-Tamb)
    h2=h1+(POT-Qcomp)/mdot
    T3=Tcond-Tsup
    h3=PropsSI("H","T",T3,"P",Pcond,"isobutane")
    QR=mdot*(h2-h3)
    QAR=UAcond*(Tcond-Tamb)

"""
evaporador
"""
Qevap=mdot*(h1-h3)
Qevap2=UAevap*(TRFR-Tevap)
while (abs(Qevap - Qevap2)/Qevap > 0.0001):
    if (Qevap > Qevap2):
        Tlimsupevap = Tevap
    else:
        Tliminfevap = Tevap
    Tevap=(Tliminfevap+Tlimsupevap)/2
    T5=Tevap+Tsup
    Pevap=PropsSI("P","T", Tevap,"Q",1,"isobutane")
    Pcond=PropsSI("P","T", Tcond,"Q",1,"isobutane")
    v1=1/PropsSI("D","P",Pevap,"T",T10,"isobutane")
    mdot=(ROT*VOL*ETA_v)/v1
    h1=PropsSI("H","P",Pevap,"T",T10,"isobutane")
    T3=Tcond-Tsup
    h3=PropsSI("H","T",T3,"P",Pcond,"isobutane")
    T1=T5+e*(T3-T5)
    Qevap=mdot*(h1-h3)
    Qevap2=UAevap*(TRFR-Tevap)
"""
iteração
"""
print("T1=", T1)
print("T10=", T10)
while(abs(T1 - T10)/T1 > 0.0001):
    print("entreii")
    print("T1=", T1)
    if (T1 > T10):
        Tliminfcond = Tcond
        Tlimsupevap = Tevap
        print("if")
    else:
        Tliminfevap = Tevap
        Tlimsupcond = Tcond
    Tevap=(Tliminfevap+Tlimsupevap)/2
    Tcond = (Tliminfcond+Tlimsupcond)/2
    Pcond=PropsSI("P","T", Tcond,"Q",1,"isobutane")
    Pevap=PropsSI("P","T", Tevap,"Q",1,"isobutane")
    print("Tevap=", Tevap)
    print("Tcond=", Tcond)
    T10=(Tevap+Tsup)+e*(Tcond-Tsub-(Tevap+Tsup))
    print("T10=", T10)
    v1=1/PropsSI("D","P",Pevap,"T",T10,"isobutane")
    mdot=(ROT*VOL*ETA_v)/v1
    h1=PropsSI("H","P",Pevap,"T",T10,"isobutane")
    s1=PropsSI("S","P",Pevap,"T",T10,"isobutane")
    h2s=PropsSI("H","T",Tcond,"S",s1,"isobutane")
    POT=mdot*(h2s-h1)/ETA_g
    h2a=h1+POT/mdot
    T2a=PropsSI("T","P",Pcond,"H",h2a,"isobutane")
    Qcomp=UAcomp*(T2a-Tamb)
    h2=h1+(POT-Qcomp)/mdot
    """
    condensador
    """
    T3=Tcond-Tsub
    h3=PropsSI("H","T",T3 ,"P",Pcond,"isobutane")
    QR=mdot*(h2-h3)
    QAR=UAcond*(Tcond-Tamb)
    print("QR=", QR)
    print("QAR=", QAR)
    while (abs(QR - QAR)/QR > 0.09):
        if (QAR > QR):
            Tlimsupcond = Tcond
            print("if")
        else:
            Tliminfcond = Tcond
        Tcond = (Tliminfcond+Tlimsupcond)/2
        Pcond=PropsSI("P","T", Tcond,"Q",1,"isobutane")
        h2s=PropsSI("H","T",Tcond,"S",s1,"isobutane")
        POT=mdot*(h2s-h1)/ETA_g
        h2a=h1+POT/mdot
        T2a=PropsSI("T","P",Pcond,"H",h2a,"isobutane")
        Qcomp=UAcomp*(T2a-Tamb)
        h2=h1+(POT-Qcomp)/mdot
        T3=Tcond-Tsup
        h3=PropsSI("H","T",T3,"P",Pcond,"isobutane")
        QR=mdot*(h2-h3)
        QAR=UAcond*(Tcond-Tamb)

    """
    evaporador
    """
    Qevap=mdot*(h1-h3)
    Qevap2=UAevap*(TRFR-Tevap)
    while (abs(Qevap - Qevap2)/Qevap > 0.1):
        if (Qevap > Qevap2):
            Tlimsupevap = Tevap
        else:
            Tliminfevap = Tevap
        Tevap=(Tliminfevap+Tlimsupevap)/2
        T5=Tevap+Tsup
        Pevap=PropsSI("P","T", Tevap,"Q",1,"isobutane")
        Pcond=PropsSI("P","T", Tcond,"Q",1,"isobutane")
        v1=1/PropsSI("D","P",Pevap,"T",T10,"isobutane")
        mdot=(ROT*VOL*ETA_v)/v1
        h1=PropsSI("H","P",Pevap,"T",T10,"isobutane")
        T3=Tcond-Tsup
        h3=PropsSI("H","T",T3,"P",Pcond,"isobutane")
        Qevap=mdot*(h1-h3)
        Qevap2=UAevap*(TRFR-Tevap)
    T1=T5+e*(T3-T5)
print("T1=", T1-273)
print("T5=", T5-273)
print("T3=", T3-273)
print("Tcond=", Tcond-273)
print("Tevap=", Tevap-273)
