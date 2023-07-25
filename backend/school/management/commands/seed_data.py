from django.core.management.base import BaseCommand
from school.models import School, Student, Section, PointTransaction, GlobalUniqueCounter
import random
import csv
from django.utils import timezone
from datetime import timedelta

NAMES = [
    "Buck Auer", "Niko Bosco", "Dale Rohan", "Dee Rau", "Lura Ortiz", "Emil Hills", "Tiana Ward",
    "Ryley Beer", "Dean Lang", "Mara Crona", "Era Heaney", "Avery Batz", "Deja Lemke", "Keanu Yost",
    "Sim Parker", "Gabe Stamm", "Bell Walsh", "Cale Lang", "Ottis Torp", "Franz Huel", "Kale Moen",
    "Rod Cremin", "Zane Runte", "Neva Batz", "Dee Hand", "Adan Rohan", "Rae Mills", "Ana Metz",
    "Jose Nolan", "Mavis Jast", "Jena Mraz", "Judy Hills", "Lia Ferry", "Mina Feil", "Jade Kihn",
    "Tod Hintz", "Retha Toy", "Ari Feeney", "Lacey Hahn", "Dora O'Kon", "Pat Hirthe", "Larue Metz",
    "Josie Rau", "Velva Lind", "Clay Cole", "Lilla Beer", "Rene Smith", "Erna Huels", "Nova Haag",
    "Tom Jacobs", "Nico Dare", "Lola Purdy", "Nakia Hane", "Vince Fay", "Dena Purdy", "Vida Wyman",
    "Eva Hammes", "Elena Lind", "Wendy Mohr", "Lelah Wiza", "Rex Jacobi", "Kacey Mohr", "Angie Beer",
    "Guy Ward", "Felipa Von", "Wade Ebert", "Tina Smith", "Janae Mohr", "Devin Mann", "Mia Mraz",
    "Fleta Batz", "Eva Lakin", "Kira Walsh", "Jan Little", "Vada Koss", "Brad Walsh", "Tom Lakin",
    "Alene Hane", "Kylee Wolf", "Mya Rath", "Dixie Beer", "Lloyd Koch", "Ted Rogahn", "Aylin Kihn",
    "Russ Lang", "Cory Roob", "Velva Rowe", "Fern Moen", "Arvid Bode", "Rod Carter", "Vita Price",
    "Ayden Moen", "Kody Morar", "Alba Bosco", "Dovie Jast", "Myra Runte", "Cora Mills", "Vidal King",
    "Luis Haley", "Roel Jones"
]

class Command(BaseCommand):
    help = 'Create random students'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of students to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        students_per_school = 100

        # Create Section objects before referencing them in Students
        for i in range(1, 5):
            Section.objects.create(name=f'Section {i}')

        # Create 10 Schools
        for i in range(1, 11):
            School.objects.create(name=f'School {i}')

        # Get all created schools and sections
        schools = School.objects.all()
        sections = Section.objects.all()

        # Variable to keep track of the roll number
        # roll_no_counter = 1

        # Generate students for each school
        counter, _ = GlobalUniqueCounter.objects.get_or_create(id=1) # Using a fixed id to ensure only one instance

        for school in schools:
            for i in range(students_per_school):
                student = Student.objects.create(
                    grade=random.choice([9, 10, 11, 12]),
                    roll_no=counter.last_roll_no + 1,  # Increasing roll number for each student
                    name=random.choice(NAMES),
                    points=random.randint(0, 100),
                    school=school,  # assign student to the current school
                    section=random.choice(sections)  # choose a random section from the list
                )
                counter.last_roll_no += 1
                counter.save()

                # Create a PointTransaction for the student
                time_difference = timedelta(
                    days=random.randint(0, 60),  # random number of days in the last 2 months
                    hours=random.randint(0, 23),  # random hour
                    minutes=random.randint(0, 59),  # random minute
                    seconds=random.randint(0, 59),  # random second
                )
                PointTransaction.objects.create(
                    student=student,
                    points=student.points,
                    timestamp=timezone.now() - time_difference,
                )

                # roll_no_counter += 1


        students = Student.objects.all()
        for student in students:
            num_friends = random.randint(1, min(5, total-1))
            friends = random.sample([s for s in students if s != student], num_friends)
            student.friends.add(*friends)
        
        with open('students.csv', 'w', newline='') as csvfile:
            fieldnames = ['roll_no', 'grade', 'name', 'points', 'school', 'section', 'friends', 'updated_at']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for student in Student.objects.all():
                friends = ', '.join(str(friend.roll_no) for friend in student.friends.all())
                writer.writerow({
                    'roll_no': student.roll_no,
                    'grade': student.grade,
                    'name': student.name,
                    'points': student.points,
                    'school': student.school,
                    'section': student.section,
                    'friends': friends,
                    'updated_at': student.updated_at,
                })

        with open('sections.csv', 'w', newline='') as csvfile:
            fieldnames = ['id', 'name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for section in Section.objects.all():
                writer.writerow({
                    'id': section.id,
                    'name': section.name,
                })

        with open('schools.csv', 'w', newline='') as csvfile:
            fieldnames = ['id', 'name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for school in School.objects.all():
                writer.writerow({
                    'id': school.id,
                    'name': school.name,
                })
        with open('point_transactions.csv', 'w', newline='') as csvfile:
            fieldnames = ['id', 'student_id', 'points', 'timestamp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for transaction in PointTransaction.objects.all():
                writer.writerow({
                    'id': transaction.id,
                    'student_id': transaction.student_id,
                    'points': transaction.points,
                    'timestamp': transaction.timestamp,
                })



        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
