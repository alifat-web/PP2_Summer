class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

#Use the Person class to create an object, and then execute the printname method:

class Student(Person):
  def __init__(self, fname, lname):
    Person.__init__(self, fname, lname)


x = Person("John", "Doe")
x.printname()

x = Student("Mike", "Olsen")
x.printname()