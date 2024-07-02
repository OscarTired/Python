print("Cantidad de productos:")
prods = int(input())
i=0
sub=0
while i<prods:
    print("Producto ",i+1," valor:")
    val = float(input())
    print("Cantidad")
    cant = float(input())
    subpro=val*cant
    sub=sub+subpro
    i+=1
IGV = sub * 0.18
total = sub + IGV
print("Se vendieron: ", prods," Productos")
print("Subtotal: s/.",sub)
print("IGV 18%: s/.", IGV)
print(f"Total: s/.{total:.2f}")
