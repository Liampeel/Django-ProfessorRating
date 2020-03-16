from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.


class Professor(models.Model):
    professor_id = models.CharField(primary_key=True, max_length=3)
    name = models.CharField(max_length=25)

    def __str__(self):
        output = "{name} {professor_id}".format(
            name=self.name,

            professor_id=self.professor_id)

        return output


class Module(models.Model):
    module_code = models.CharField('Module Code', primary_key=True, max_length=10)
    module_name = models.CharField('Module Name', max_length=30)

    def __str__(self):
        output = "{module_code}. {module_name}".format(module_code=self.module_code,
                                                       module_name=self.module_name)

        return output


class ModuleInstance(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    year = models.CharField(max_length=4)
    semester = models.PositiveSmallIntegerField(choices=[[1, 1], [2, 2]])
    professor = models.ManyToManyField(Professor)

    def __str__(self):
        output = "{module} {professor}  {year} : {semester}".format(module=self.module,
                                                                    professor=self.professor,
                                                                    year=self.year,
                                                                    semester=self.semester)
        return output


class Rating(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, null=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True)
    year = models.CharField(max_length=4)
    semester = models.PositiveSmallIntegerField(choices=[[1, 1], [2, 2]])
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        output = "{module} {professor} {year} {semester} : {rating}".format(module=self.module,
                                                                            professor=self.professor,
                                                                            year=self.year,
                                                                            semester=self.semester,
                                                                            rating=self.rating)
        return output
