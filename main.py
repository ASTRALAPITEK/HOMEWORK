import random
import logging


brands_of_car = {
    "BMW": {"fuel": 100, "strength": 100, "consumption": 6},
    "Lada": {"fuel": 50, "strength": 40, "consumption": 10},
    "Volvo": {"fuel": 70, "strength": 150, "consumption": 8},
    "Audi": {"fuel": 70, "strength": 150, "consumption": 8},
    "Ferrari": {"fuel": 80, "strength": 120, "consumption": 14}
}
logging.basicConfig(filename='sims.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.info("PROJECT INFORMATION")
logger.info("Loading the cars...")
#
brands_of_car = {
    "BMW": {"fuel": 100, "strength": 100, "consumption": 6},
    "Lada": {"fuel": 50, "strength": 40, "consumption": 10},
    "Volvo": {"fuel": 70, "strength": 150, "consumption": 8},
    "Audi": {"fuel": 70, "strength": 150, "consumption": 8},
    "Ferrari": {"fuel": 80, "strength": 120, "consumption": 14}
}
#
logger.info(list(brands_of_car))
logger.info("Loading the jobs...")
#
job_list = {
    "Java dev": {"salary": 50, "gladness_less": 10},
    "Python dev": {"salary": 40, "gladness_less": 3},
    "C++ dev": {"salary": 45, "gladness_less": 25},
    "Rust dev": {"salary": 70, "gladness_less": 1}
}
#
logger.info(list(job_list))
logger.info("Creating a character...")
class Human:
    def __init__(self, name="Human", job=None, home=None, car=None, pet=None):
        self.name = name
        self.money = 100
        self.gladness = 50
        self.satiety = 50
        self.job = job
        self.car = car
        self.home = home
        self.pet = pet

    def get_home(self):
        self.home = House()
        logger.info(f"{self.name} got a home")

    def get_car(self):
        self.car = Auto(brands_of_car)
        logger.info(f"{self.name} got a car")

    def get_job(self):
        if self.car.drive():
            self.job = Job(job_list)
            logger.info(f"{self.name} got a job as a {self.job.job} with a salary of {self.job.salary}")
        else:
            self.to_repair()
            return

    def get_pet(self):
        self.pet = Pet()
        logger.info(f"{self.name} got a pet")

    def eat(self):
        if self.home.food <= 0:
            self.shopping("food")
        else:
            if self.satiety >= 100:
                self.satiety = 100
                return
            self.satiety += 5
            self.home.food -= 5

    def work(self):
        if self.car.drive():
            self.money += self.job.salary
            self.gladness -= self.job.gladness_less
            self.satiety -= 4
        else:
            if self.car.fuel < 20:
                self.shopping("fuel")
            else:
                self.to_repair()
                logger.warning(f"{self.name}'s car broke down and needs repair.")

    def shopping(self, manage):
        if self.car.drive():
            if manage == "fuel":
                print("I bought fuel")
                self.money -= 100
                self.car.fuel += 100
                logger.info(f"{self.name} bought fuel")
            elif manage == "food":
                print("Bought food")
                self.money -= 50
                self.home.food += 50
                logger.info(f"{self.name} bought food")
            elif manage == "delicacies":
                print("Hooray! Delicious")
        else:
            if self.car.fuel < 20:
                manage = "fuel"
            else:
                self.to_repair()
                return

    def chill(self):
        self.gladness += 10
        self.home.mess += 5

    def clean_home(self):
        self.gladness -= 5
        self.home.mess = 0

    def to_repair(self):
        self.car.strength += 100
        self.money -= 50
        logger.warning(f"{self.name}'s car needed repair and was repaired. Money spent: 50")

    def days_indexes(self, day):
        day = f"Today the {day} of the {self.name} life"
        print(f"{day:=^50}", "\n")
        human_indexes = self.name + "'s indexes"
        print(f"{human_indexes:^50}", "\n")
        print(f"Money - {self.money}")
        print(f"Satiety - {self.satiety}")
        print(f"Gladness - {self.gladness}")
        home_indexes = "Home indexes"
        print(f"{home_indexes:^50}", "\n")
        print(f"Food - {self.home.food}")
        print(f"Mess - {self.home.mess}")
        car_indexes = f"{self.car.brand} car indexes"
        print(f"{car_indexes:^50}", "\n")
        print(f"Fuel - {self.car.fuel}")
        print(f"Strength - {self.car.strength}")
        pet_indexes = "Pet indexes"
        print(f"{pet_indexes:^50}", "\n")
        print(f"Pet happiness - {self.pet.happiness}")

    def is_alive(self):
        if self.gladness < 0:
            print("Depression")
            logger.error(f"{self.name} is in depression.")
            return False
        if self.satiety < 0:
            print("Dead")
            logger.error(f"{self.name} is dead.")
            return False
        if self.money < -500:
            print("Bankrupt")
            logger.error(f"{self.name} went bankrupt.")
            return False
        return True

    def live(self, day):
        if not self.is_alive():
            return False
        if self.home is None:
            print("Settled in the house")
            logger.info(f"{self.name}, settled new home")
            self.get_home()
        if self.car is None:
            self.get_car()
            print(f"I bought a {self.car.brand} car")
            logger.info(f"{self.name}, bought new car")
        if self.job is None:
            self.get_job()
            print(f"I don't have a job, going to get a job: {self.job.job} with salary {self.job.salary}")
            logger.info(f"{self.name}, don't have a job, going to get a job: {self.job.job} with salary {self.job.salary}")
            
        if self.pet is None:
            self.get_pet()
            print("I have a new pet!")
            logger.info(f"{self.name}, have new pet")
        self.days_indexes(day)
        dice = random.randint(1, 4)
        if self.satiety < 20:
            print("I will go eat")
            self.eat()
        elif self.gladness < 20:
            if self.home.mess > 15:
                print("I want to chill but there is so much mess\nSo I will clean the house")
                self.clean_home()
                logger.info(f"{self.name} cleaned the house")
            else:
                print("Let's chill")
                logger.info(f"{self.name}, start chillll")
                self.chill()
        elif self.money < 0:
            print("Start working")
            logger.info(f"{self.name}, startworking")
            self.work()
        elif self.car.strength < 15:
            print("I need to repair the car")
            logger.info(f"{self.name}, repaired car")

            self.to_repair()
        elif dice == 1:
            print("Let's chill")
            logger.info(f"{self.name}, started chill")
            self.chill()
        elif dice == 2:
            print("Start working")
            logger.info(f"{self.name}, start working")
            self.work()
        elif dice == 3:
            print("Cleaning time!")
            logger.info(f"{self.name}, go to cleaning hose")
        elif dice == 4:
            print("Time for treats!")
            logger.info(f"{self.name}, go to buy delicasies")
            self.shopping(manage="delicacies")
        self.pet.live()
        return True
logger.info("Character created succesfuly!")

class Auto:
    def __init__(self, brand_list):
        self.brand = random.choice(list(brand_list))
        self.fuel = brand_list[self.brand]["fuel"]
        self.strength = brand_list[self.brand]["strength"]
        self.consumption = brand_list[self.brand]["consumption"]

    def drive(self):
        if self.strength > 0 and self.fuel >= self.consumption:
            self.fuel -= self.consumption
            self.strength -= 1
            return True
        else:
            print("The car cannot move")
            return False
logger.info("Cars have been initiated")

class House:
    def __init__(self):
        self.mess = 0
        self.food = 0


class Pet:
    def __init__(self):
        self.happiness = 50
        self.names = ["Layl", "Karl", "Noman"]

    def live(self):
        dice = random.randint(1, 4)
        if dice == 1:
            print("Your pet is playing happily!")
            self.happiness += 10
        elif dice == 2:
            print("Your pet is sleeping.")
        elif dice == 3:
            print("Your pet is hungry.")
            self.happiness -= 5
        elif dice == 4:
            print("Your pet wants to go for a walk.")
            self.happiness += 5





class Job:
    def __init__(self, job_list):
        self.job = random.choice(list(job_list))
        self.salary = job_list[self.job]["salary"]
        self.gladness_less = job_list[self.job]["gladness_less"]


nick = Human(name="Nick")

for day in range(380):
    if not nick.live(day):
        break