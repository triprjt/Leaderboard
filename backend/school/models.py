import secrets
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class School(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Section(models.Model):
    SECTIONS = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]
    name = models.CharField(max_length=50, choices=SECTIONS)  # increase max_length

    def __str__(self):
        return f"Section {self.name}"

    
class GlobalUniqueCounter(models.Model):
    last_roll_no = models.IntegerField(default=0)


class Student(models.Model):
    GRADES = [('9', '9th'), ('10', '10th'), ('11', '11th'), ('12', '12th')]
    school = models.ForeignKey(School, related_name='students', on_delete=models.CASCADE)
    section = models.ForeignKey(Section, related_name='students', on_delete=models.CASCADE)
    grade = models.CharField(max_length=2, choices=GRADES)
    roll_no = models.PositiveIntegerField(primary_key=True)
    name = models.TextField()
    points = models.IntegerField(default=0)
    friends = models.ManyToManyField('self', blank=True, symmetrical=True)
    updated_at = models.DateTimeField(auto_now_add=True)  

    def get_school_name(self):
        return self.school.name

    def get_section_name(self):
        return self.section.name
    def get_school_id(self):
        return self.school.id
    def get_section_id(self):
        return self.section.id    
    
    def update(self, **kwargs):
        if "points" in kwargs:
            self.points += kwargs.get('points')
        self.updated_at = timezone.now()
        self.save()



class PointTransaction(models.Model):
    student = models.ForeignKey(Student, related_name='transactions', on_delete=models.CASCADE)
    points = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
            self.student.updated_at = self.timestamp
            self.student.save()
            super().save(*args, **kwargs)
