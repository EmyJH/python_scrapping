# print("hello world")
# a=2
# print (a)
print("2+3=",2+3) # commentaire
### comme doc java ####
x=2
x = 3.9 * x * (1 - x)
x=3
print(x)


def main():
    choix= str("oui")
    while choix != "non" :
        celsius = float(input("What is the Celsius temperature? "))
        fahrenheit = (9.0/5.0) * celsius + 32
        print ("The temperature is ",fahrenheit," degrees Fahrenheit.")
        choix=str(input("voulez-vous continuez(oui/non)?"))

main()

