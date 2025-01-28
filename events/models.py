# from django.db import models

# # Create your models here.


# class Employee(models.Model):
#     name= models.CharField(max_length=100)
#     email = models.EmailField(unique=True)

#     def __str__(self):
#         return self.name


# class Event(models.Model):
#     project = models.ForeignKey(
#         "Project", 
#         on_delete=models.CASCADE,
#         default=1
#         )
#     assigned_to = models.ManyToManyField(Employee, related_name='events')
    
#     title = models.CharField(max_length=250)
#     description = models.TextField()
#     due_date = models.DateField()
#     is_completed = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)







# class EventDetail(models.Model):
#     HIGH = 'H'
#     MEDIUM = 'M'
#     LOW = 'L'
#     PRIORITY_OPTIONS = (
#         (HIGH, 'High'),
#         (MEDIUM, 'Medium'),
#         (LOW, 'Low')
#     )
#     event = models.OneToOneField(
#         Event, 
#         on_delete=models.CASCADE,
#         related_name='details'
#     )
#     assigned_to = models.CharField(max_length=100)
#     priority = models.CharField(max_length=1, 
#                                 choices=PRIORITY_OPTIONS, default=LOW)






# class Project(models.Model):
#     name = models.CharField(max_length=100)
#     start_date = models.DateField()


from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField(auto_now_add=True)
    location = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Participant(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    events = models.ManyToManyField(Event)

    def __str__(self):
        return self.name