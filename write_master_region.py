lines = 749

def printDetails(numberArray, nameArray, coordinateArray, coretypeArray):
    while True:
        target = str(input("Enter number of target to print details, or enter 0 to break: "))
        
        if int(target) == 0:
            return False
        else:
            TF = False    
            for index in range(lines):
                if numberArray[index] == target:
                    print("Number: " + str(target))
                    print("Name: " + str(nameArray[index]))
                    print("Coordinates: " + str(coordinateArray[index]))
                    print("Coretype: " + str(coretypeArray[index]) + "\n")
                    TF = True
                    break
            if TF == False:
                print("Target not found.\n")
                
            return printDetails(numberArray, nameArray, coordinateArray, coretypeArray)

            
filename = "J_A+A_584_A91_tablea1.dat.gz.txt"

number_temp = [x.split('|')[0] for x in open(filename).readlines()]
name = [x.split('|')[1] for x in open(filename).readlines()]
coordinates_temp = [x.split('|')[2] for x in open(filename).readlines()]
coretype_temp = [x.split('|')[3] for x in open(filename).readlines()]

number, coordinates, coretype = [], [], []

for eachElement in number_temp:
    number.append(eachElement.strip())
    
for eachElement in coordinates_temp:
    coordinates.append(eachElement[:11].replace(' ', ':') + eachElement[11:12].replace(' ', ',') + eachElement[12:].replace(' ', ':'))

for eachElement in coretype_temp:
    coretype.append(eachElement.strip())

with open("master.reg", 'w') as master_region:
    master_region.write("# Region file format: DS9 version 4.1 \n")
    master_region.write("global color=green dashlist=8 3 width=1 font=\"helvetica 10 normal roman\" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1 \n")
    master_region.write("fk5 \n")

    for i in range(lines):
        master_region.write("{:<40} {:<24} {:<13}".format("point(" + coordinates[i] + ") # point=X", "text={" + coretype[i] + ", " + number[i] + "}", "color={red}"))
        master_region.write("\n")

master_region.close()

printDetails(number, name, coordinates, coretype)
