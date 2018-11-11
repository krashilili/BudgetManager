from django.db import models
from django.utils.text import slugify
from django.utils import timezone

# Create your models here.


class BankStatementDocument(models.Model):
    owner = models.CharField(max_length=255)
    bank = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='doc/', blank=True)
    uploaded_at = models.DateTimeField(editable=False)
    slug = models.SlugField(max_length=63, unique=True, blank=True)

    def __str__(self):
        return f"{self.owner} + {self.file}"

    def _get_unique_slug(self):
        """
        Create a unique slug for the bank statement doc
        :return:
        """
        text = f"{self.owner} {self.bank} {self.file}"
        slug = slugify(text)
        unique_slug = slug
        num = 1
        while BankStatementDocument.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        # on save, update timestamps
        if not self.id:
            self.uploaded_at = timezone.now()

        return super().save(*args, **kwargs)


class BankStatement(models.Model):
    """
    The field name shall be the same as the column names in the uploaded csv files.
    """
    owner = models.CharField(max_length=30, null=True,verbose_name='Owner')
    bank_name = models.CharField(max_length=30,null=True,verbose_name='Bank')
    date = models.DateField(verbose_name='Trans. Date', max_length=30, null=True)
    post = models.CharField(verbose_name='Post Date', max_length=30)
    description = models.CharField(verbose_name='Description',max_length=255)
    amount = models.CharField(verbose_name='Amount', max_length=30)
    category = models.CharField(verbose_name='Category',max_length=30)
    statement_source = models.CharField(max_length=200,null=True)
    slug = models.SlugField(max_length=63, unique=True)

    def _get_unique_slug(self):
        """
        Create a unique slug for the bank statement doc
        :return:
        """
        text = f"{self.date} {self.bank_name} {self.amount} {self.description[:4]}"
        slug = slugify(text)
        unique_slug = slug
        num = 1
        while BankStatement.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()

        return super().save(*args, **kwargs)

    def __unicode__(self):
        return f"{self.owner}: {self.bank_name}- {self.statement_source}"

    def __str__(self):
        return self.description
