from django.db import models
from django.utils.translation import gettext_lazy as _





class Company(models.Model):
    '''
    Every object have it's Company. 
    '''
    name = models.CharField(
        _("Company name"),
        max_length=256
        )
    ur_address = models.CharField(
        _("Legal address "),
        max_length=256
        )
    











class Status(models.TextChoices):
    # Choises for Modems and Devices
    NODATA = 'nodata', _('No Data')
    ACTIVE = 'active', _('Is set on Object')
    INACTIVE = 'inactive', _('On Reserve')
    LOST = 'lost', 'Have no info de hell it is!'


class Device(models.Model):
    '''
    Abstract Device whith it Abilities, what can exists.
    '''
    name = models.CharField(_("Name"), help_text="Just name of device. ex. Granit", max_length=50)
    plume_number = models.SmallIntegerField(_("Number of Plumes"), help_text=_("The ONLY ONE possible Plume Nuber for this Device."))
    is_lavina = models.BooleanField(_("Shown in Lavina"), default=True)
    is_usb = models.BooleanField(_("Have USB slot"), default=False)
    is_rerun  = models.BooleanField(_("Can be rerun"), default=False)
    is_lock = models.BooleanField(_("Plume can be Lock"), default=False)
    is_unlock = models.BooleanField(_("Plume can be UNLock"), default=False)
    is_remoteprogrammable = models.BooleanField(_("Can be Programmed remotely"), default=False)

    def get_full_name(self):
        return self.name + self.is_usb + self.is_lavina




class Object(models.Model):
    '''
    Our Cards are installed on some Objects. Here it is.
    '''
    name = models.CharField(_("Title"), max_length=256, help_text=_("Object Title"))
    address = models.CharField(_("Address"), max_length=256)
    company = models.ForeignKey(
        Company,
        verbose_name=_("Parent Company name"),
        on_delete=models.CASCADE
        )
    device = models.ForeignKey(
        Device,
        verbose_name=_("Device name"),
        null=True,
        on_delete=models.SET_NULL
        )




class DeviceReal(models.Model):
    '''
    Device, which is installed at object OR in reserve
    '''
    class Purposes(models.TextChoices):
        # What kinda device is installed
        ND = 'nd', 'Have no info de hell it is!'
        SECURE = 'sec', _('Security only.')
        FIRE = 'fir', _('Fire security only.')
        FIREANDSECURE = 'fas', _('Fire security and security.')

    device = models.ForeignKey(Device, verbose_name=_("Device title"), on_delete=models.CASCADE)
    object = models.ForeignKey(Object, verbose_name=_("Object where Device is."), null=True, on_delete=models.SET_NULL)
    status = models.CharField(_("Status"), max_length=10, choices=Status.choices, default=Status.NODATA)
    purpose = models.CharField(_("Device Purpose"), max_length=3, choices=Purposes.choices, default=Purposes.ND)
    plume_number = models.SmallIntegerField(_("Number of Plumes"), null=True, blank=True)
    # Количество шлейфов можно было бы вынести в отдельную таблицу OneToOne. Добавив им назначение если надо.




class SIMCard(models.Model):

    # SIM card operators
    PROVIDER = (
        ('0', 'NoData'),
        ('1', 'Megafon'),
        ('2', 'MTC'),
        ('3', 'Tele2'),
        ('4', 'Beeline'),
        )

    # Status of SIM-Card
    CARDSTATUS = (
        ('0', 'NoData'),
        ('1', 'Active'),
        ('2', 'Blocked'),
        ('3', 'Lost'),
        ('4', 'On Object'),
        ('5', 'On Reserve'),
        )

    # SIM card home city
    SIMCITY = (
         ('0', 'Pskov'),
         ('1', 'Saint-Peterburg'),
        )


    # My Model
    provider = models.SmallIntegerField(
        _("Operator"),
        choices = PROVIDER,
        default = 0
        )
    city = models.SmallIntegerField(
        _("City"),
        choices = SIMCITY,
        default = 0
        )
    number = models.CharField(
        _("Phone Numeber"),
        max_length=20
        )
    ICCID = models.CharField(
        "ICCID",
        max_length=20
        )
    status = models.SmallIntegerField(
        _("Status"),
        choices = CARDSTATUS,
        default = 0
        )
    is_rereleased = models.BooleanField(
        _("Was re-released"),
        default=False
        )
    date_rerelease = models.DateField(
        _("Re-Release date"),
        auto_now=False,
        auto_now_add=False
        )
    




class DeviceModem(models.Model):
    '''
    Modem installed inside Devices. One device can have 2 modems => we have device field here. 
    '''
    ver = models.SmallIntegerField(_("Version of Modem"), default=3)
    sim1 = models.ForeignKey(SIMCard, verbose_name=_("First SIM-Card"), related_name="FirstSIM", null=True, on_delete=models.SET_NULL)
    sim2 = models.ForeignKey(SIMCard, verbose_name=_("Second SIM-Card"), related_name="SEcondSIM", null=True, on_delete=models.SET_NULL)
    status = models.CharField(_("Status"), max_length=10, choices=Status.choices, default=Status.NODATA)
    device = models.ForeignKey(Device, verbose_name=_("Device, where it installed"), null=True,on_delete=models.SET_NULL)







class LavinaObject(models.Model):
    object = models.OneToOneField(
        Object,
        verbose_name=_("Object"),
        on_delete=models.CASCADE
        )    
    number = models.IntegerField(
        _("Lavina object Number")
        )

class LavinaDevice(models.Model):
    device = models.OneToOneField(
        Device,
        verbose_name=_("Device"),
        on_delete=models.CASCADE
        )
    numeber = models.IntegerField(_("Lavina Device Number"))