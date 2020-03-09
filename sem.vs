wait(2)
wait(1)
signal(0) S + 1
wait(1)
# nao bloqueia

S = 0
A                       B
opA                 wait(S)
signal(S)             opB


S1 = 0          S2 = 0
A                     B
opA                 wait(S2)
signal(S2)          opB
wait(S1)            signal(S1)
opA                 wait(S2)
Signal(S2)          opB


S1 = 0          S2 = 0          S3 = 0
P1              P2              P3
print(S)      wait(S2)      wait(S3)
signal(S2)    print(J)      print(F)
wait(S1)      signal(S3)    signal(S1)
print(OK)     wait(S2)      wait(S3)
signal(S2)    print(OK)     print(OK)
              signal(S3)



