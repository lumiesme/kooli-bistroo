from django.db import models
from django.urls import reverse

class Category(models.Model):
    number = models.IntegerField(null=True, blank=True, default=0)
    name = models.CharField(max_length=255, unique=True, verbose_name="Uue kategooria nimetus")

    def __str__(self):
        return self.name

class menuDate(models.Model):
    kuupaev = models.DateTimeField(null=False, blank=False)

class MenuCategory(models.Model):
    date = models.DateField(null=False, blank=False, unique=True, verbose_name="kirjutage kuupqev")
    teema_paev = models.CharField(max_length=255, null=True, blank=True, unique=True, verbose_name="Teemapäeva nimetus")
    peakokk = models.CharField(max_length=500, null=True, blank=True, unique=True, verbose_name="Peakokk soovitab")
    kes_tegid = models.CharField(max_length=1000, null=True, blank=True, unique=True, verbose_name="Toidud tegid")
    #date = models.ForeignKey(menuDate, on_delete=models.CASCADE, null=True, blank=True)


    class Meta:
        ordering = ['-date']

    def get_absolute_url(self):
        return reverse('app_admin:todays_menu_list')
    def __str__(self):
        return f'{self.date.strftime("%d.%m.%Y")}'

class FoodsListing(models.Model):
    toidu_nimetus = models.CharField(max_length=255, verbose_name="Sisesta toidu nimetus")
    taishind = models.FloatField(null=False, blank=False)
    poolhind = models.FloatField(null=True, blank=True)
    kategooria = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, verbose_name="Kategooria")

    def get_absolute_url(self):
        return reverse('app_admin:foods_name_listing', kwargs={'pk': self.pk})

    def __str__(self):
        return self.toidu_nimetus

class MenuData(models.Model):
    date = models.ForeignKey(menuDate, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Valige menu kuupaev")
    kategooria = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, default=None,
                                   verbose_name="Kategooria")

    class Meta:
        ordering = ['date__kuupaev', 'kategooria']

    def get_absolute_url(self):
        return reverse('app_admin:todays_menu_update', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.date} - {self.kategooria}'

class Menu(models.Model):
    #menuu = models.ForeignKey(MenuData, on_delete=models.CASCADE, related_name='menuu')
    andmed = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, verbose_name="menucategory")
    #foods = models.ForeignKey(FoodsListing, on_delete=models.CASCADE, null=True, blank=True, default=None)
    toit = models.CharField(max_length=255, verbose_name="Sisesta toidu nimetus")
    t_hind = models.DecimalField(max_digits=4, decimal_places=2, null=False, blank=False)
    p_hind = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    naita_menuus = models.BooleanField(default=True)

    class Meta:
        ordering = ['andmed']

    def __str__(self):
        return f'{self.andmed.date.strftime("%d.%m.%Y")}'
