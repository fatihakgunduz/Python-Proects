from persons import Person
loop = True

list = []

while loop:

    print("\n1-Yeni Kayıt\n2-Kayıtlar\n3-Kayıt Sil\n4-Çıkış\n")
    option = int(input("Seçenek -> "))

    if option == 1:
        person = Person(input("Enter name: "), input("Enter surname:  "), int(input("Enter Number: ")))
        list.append(person)
    elif option == 2:
        num = 1
        for kisi in list:
            print(str(num) + "-" + kisi.name + " " + kisi.surname + " " + str(kisi.number))
            num+=1
    elif option == 3:
        n_del = input("Enter the name and surname of person you want to delete\n")
        for n in list:
            if n_del == (n.name+" "+n.surname):
                list.pop(list.index(n))
    else:
        loop = False
