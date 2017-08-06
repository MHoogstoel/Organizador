""" Ensemble des modèles exposé par l'API.
    Comprend les élèves, leurs contacts, les inscriptions ainsi que les présences aux cours.
"""
import calendar
from datetime import date, timedelta
from django.db import models

TAILLES_ABADA_CHOIX = (
    ('P', 'Petit'),
    ('M', 'Moyen'),
    ('G', 'Grand'),
    ('GG', 'Très grand')
)

CATEGORIES_COURS_CHOIX = (
    ('EVEIL', 'Éveil'),
    ('ENFANT', 'Enfant'),
    ('ADO', 'Adolescent'),
    ('ADULTE', 'Adulte')
)


class Personne(models.Model):
    """ Modèle représentant une personne: élève, contact ou parent."""

    prenom = models.CharField(max_length=50, db_index=True)
    nom = models.CharField(max_length=50, db_index=True)
    surnom = models.CharField(db_index=True, max_length=50)
    date_naissance = models.DateField(auto_now=False, auto_now_add=False)
    telephone = models.CharField(max_length=50)
    adresse = models.TextField(blank=True, null=True)

    categorie = models.CharField(
        choices=CATEGORIES_COURS_CHOIX, blank=True, null=True, max_length=10)
    corde = models.CharField(blank=True, null=True, max_length=20)
    taille_abada = models.CharField(blank=True, null=True, max_length=2,
                                    choices=TAILLES_ABADA_CHOIX)

    droit_image = models.BooleanField(default=False)
    contacts = models.ManyToManyField('self', blank=True)

    class Meta:
        """Meta definition for Personne."""

        verbose_name = 'Personne'
        verbose_name_plural = 'Personnes'

    def __str__(self):
        """Unicode representation of Personne."""
        return "{} {}".format(self.prenom, self.nom)


SEMAINE = (
    (calendar.MONDAY, 'Lundi'),
    (calendar.TUESDAY, 'Mardi'),
    (calendar.WEDNESDAY, 'Mercredi'),
    (calendar.THURSDAY, 'Jeudi'),
    (calendar.FRIDAY, 'Vendredi'),
    (calendar.SATURDAY, 'Samedi'),
    (calendar.SUNDAY, 'Dimanche')
)


class Cours(models.Model):
    """Model definition for Cours."""

    jour = models.SmallIntegerField(choices=SEMAINE)
    salle = models.CharField(max_length=50)
    categorie = models.CharField(choices=CATEGORIES_COURS_CHOIX, max_length=10)
    horaire = models.TimeField(auto_now=False, auto_now_add=False)
    dernier = models.DateField(auto_now=False, auto_now_add=False)

    class Meta:
        """Meta definition for Cours."""

        verbose_name = 'Cours'
        verbose_name_plural = 'Cours'

    def set_original(self):
        self.__original_jour = self.jour
        self.__original_dernier = self.dernier

    def __init__(self, *args, **kwargs):
        super(Cours, self).__init__(*args, **kwargs)
        self.set_original()

    @staticmethod
    def every_weekday(weekday, start, end):
        if start > end:
            return []
        date_ = start + timedelta(days=(weekday - start.weekday()) % 7)
        while date_ <= end:
            yield date_
            date_ += timedelta(days=7)

    def __str__(self):
        """Unicode representation of Cours."""
        return "Cours {} du {} {} à {}".format(
            self.get_categorie_display(),
            self.get_jour_display(),
            self.horaire,
            self.salle)

    @property
    def are_dates_to_be_updated(self):
        return self.pk is None \
            or self.__original_jour != self.jour \
            or self.__original_dernier != self.dernier

    def save(self, *args, **kwargs):
        """ Enregistre le cours actuelles et créent tout les dates liées """
        super(Cours, self).save(*args, **kwargs)
        if self.are_dates_to_be_updated:
            self.set_original()
            DateCours.objects.filter(cours=self)\
                .filter(date__gte=date.today())\
                .delete()
            for d in self.every_weekday(self.jour, date.today(), self.dernier):
                c = DateCours(cours=self, date=d)
                c.save()


class DateCours(models.Model):
    """Model definition for Cours."""

    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    date = models.DateField(db_index=True)

    class Meta:
        """Meta definition for Cours."""

        verbose_name = 'Date de cours'
        verbose_name_plural = 'Dates de cours'

    def __str__(self):
        """Unicode representation of Cours."""
        return "[{}] {}".format(str(self.cours), self.date)


class Presence(models.Model):
    """Model definition for Presence."""

    cours = models.ForeignKey(DateCours, on_delete=models.CASCADE)
    personne = models.ForeignKey(Personne, on_delete=models.CASCADE)
    present = models.BooleanField()

    class Meta:
        """Meta definition for Presence."""

        verbose_name = 'Presence'
        verbose_name_plural = 'Presences'

    def __str__(self):
        """Unicode representation of Presence."""
        return "{} {} à {}".format(str(self.personne),
                                   "est présent" if self.present else "n'est pas présent",
                                   str(self.cours))


class Inscription(models.Model):
    """Model definition for Inscription."""

    eleve = models.ForeignKey(Personne, on_delete=models.CASCADE)
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    photo = models.BooleanField(default=False)
    fiche_adhesion = models.BooleanField(default=False)
    certificat_medical = models.BooleanField(default=False)

    class Meta:
        """Meta definition for Inscriptions."""

        verbose_name = 'Inscription'
        verbose_name_plural = 'Inscriptions'

    def __str__(self):
        """Unicode representation of I nscriptions."""
        return "Inscription {} à {}".format(str(self.eleve), str(self.cours))


METHODE_PAIEMENT_CHOIX = (
    ('ESPECE', 'Éspèce'),
    ('CHÈQUE', 'Chèque')
)


class Paiement(models.Model):
    """Model definition for Paiement."""

    inscription = models.ForeignKey(Inscription)
    methode = models.CharField(max_length=10)
    encaissement = models.DateField()
    validite = models.DateField()
    encaisse = models.BooleanField(default=False)

    class Meta:
        """Meta definition for Paiement."""

        verbose_name = 'Paiement'
        verbose_name_plural = 'Paiements'

    def __str__(self):
        """Unicode representation of Paiement."""
        return "Paiement par {} pour {}".format(self.get_methode_display(), self.inscription)
