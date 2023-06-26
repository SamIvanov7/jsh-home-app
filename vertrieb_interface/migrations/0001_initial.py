# Generated by Django 4.2.2 on 2023-06-22 11:52

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="VertriebAngebot",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("angebot_id", models.CharField(max_length=255, unique=True)),
                ("current_date", models.DateField(auto_now_add=True)),
                ("is_locked", models.BooleanField(default=False)),
                ("zoho_id", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("angenommen", "angenommen"),
                            ("bekommen", "bekommen"),
                            ("in Kontakt", "in Kontakt"),
                            ("Kontaktversuch", "Kontaktversuch"),
                            ("abgelehnt", "abgelehnt"),
                            ("abgelaufen", "abgelaufen"),
                            ("on Hold", "on Hold"),
                            ("storniert", "storniert"),
                        ],
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "status_change_date",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "telefon_festnetz",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "telefon_mobil",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "zoho_kundennumer",
                    models.CharField(max_length=255, primary_key=True, serialize=False),
                ),
                ("email", models.EmailField(blank=True, max_length=255, null=True)),
                (
                    "name_display_value",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "vertriebler_display_value",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "vertriebler_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "adresse_pva_display_value",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "angebot_bekommen_am",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "anfrage_vom",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "postanschrift_latitude",
                    models.CharField(
                        blank=True, default="00000", max_length=255, null=True
                    ),
                ),
                (
                    "postanschrift_longitude",
                    models.CharField(
                        blank=True, default="00000", max_length=255, null=True
                    ),
                ),
                ("notizen", models.TextField(blank=True, null=True)),
                ("pva_klein", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "b2b_partner",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "name_prefix",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "name_last_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "name_suffix",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "name_first_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "leadstatus",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("ausstehend", "ausstehend"),
                            ("reklamiert", "reklamiert"),
                            ("akzeptiert", "akzeptiert"),
                            ("abgelehnt", "abgelehnt"),
                        ],
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "anfrage_ber",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "empfohlen_von",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "termine_text",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("termine_id", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "ablehnungs_grund",
                    models.CharField(
                        blank=True,
                        choices=[
                            (
                                "Abweichende Kundenvorstellung zum Thema PVA",
                                "Kundenvorstellung zum Thema PVA unterscheidet sich",
                            ),
                            ("Gebäude ungeeignet", "Das Gebäude ist nicht geeignet"),
                            (
                                "Günstigerer Mitbewerber",
                                "Ein Konkurrent bietet günstigere Optionen",
                            ),
                            (
                                "Investition lohnt sich nicht",
                                "Eine Investition lohnt sich nicht",
                            ),
                            (
                                "Investition zu teuer",
                                "Die Investitionskosten sind zu hoch",
                            ),
                            (
                                "Kunde hat kein Interesse mehr",
                                "Der Kunde hat kein Interesse mehr",
                            ),
                            (
                                "Kunde ist zu alt",
                                "Der Kunde ist nicht mehr interessiert",
                            ),
                            (
                                "Kunde möchte 3-phasige Notstromversorgung",
                                "Der Kunde benötigt eine 3-phasige Notstromversorgung",
                            ),
                            (
                                "Kunde möchte deutsche Produkte",
                                "Der Kunde bevorzugt deutsche Produkte",
                            ),
                            (
                                "Kunde möchte erst später bauen",
                                "Der Kunde möchte zu einem späteren Zeitpunkt bauen",
                            ),
                            (
                                "Kunde möchte Förderung abwarten",
                                "Der Kunde möchte auf Fördermittel warten",
                            ),
                            (
                                "Kunde möchte lokalen Ansprechpartner",
                                "Der Kunde wünscht einen Ansprechpartner vor Ort",
                            ),
                            (
                                "Kunde möchte PVA nur mieten",
                                "Der Kunde möchte die PVA-Anlage nur mieten",
                            ),
                            (
                                "Kunde war nicht erreichbar",
                                "Der Kunde war nicht erreichbar",
                            ),
                        ],
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "anrede",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Familie", "Familie"),
                            ("Firma", "Firma"),
                            ("Herr", "Herr"),
                            ("Herr Dr.", "Herr Dr."),
                            ("Herr Prof.", "Herr Prof."),
                            ("Frau", "Frau"),
                        ],
                        max_length=20,
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=100)),
                ("firma", models.CharField(blank=True, max_length=100)),
                ("strasse", models.CharField(blank=True, max_length=100)),
                ("ort", models.CharField(blank=True, max_length=100)),
                (
                    "anlagenstandort",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "verbrauch",
                    models.FloatField(
                        default=0.0,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "grundpreis",
                    models.FloatField(
                        default=9.8,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "arbeitspreis",
                    models.FloatField(
                        default=28.6,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "prognose",
                    models.FloatField(
                        default=2.2,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                ("zeitraum", models.PositiveIntegerField(default=5)),
                (
                    "bis10kWp",
                    models.FloatField(
                        default=8.2,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "bis40kWp",
                    models.FloatField(
                        default=7.1,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                ("speicher", models.BooleanField(default=False)),
                ("anz_speicher", models.PositiveIntegerField(default=0)),
                ("wallbox", models.BooleanField(default=False)),
                (
                    "ausrichtung",
                    models.CharField(
                        choices=[("Süd", "Süd"), ("Ost/West", "Ost/West")],
                        default="Ost/West",
                        max_length=10,
                    ),
                ),
                (
                    "komplex",
                    models.CharField(
                        choices=[
                            (
                                "einfach, einfach erreichbar",
                                "einfach, einfach erreichbar",
                            ),
                            (
                                "einfach, schwer erreichbar",
                                "einfach, schwer erreichbar",
                            ),
                            (
                                "komplex, einfach erreichbar",
                                "komplex, einfach erreichbar",
                            ),
                            (
                                "komplex, schwer erreichbar",
                                "komplex, schwer erreichbar",
                            ),
                            ("sehr komplex", "sehr komplex"),
                        ],
                        default="sehr komplex",
                        max_length=30,
                    ),
                ),
                (
                    "solar_module",
                    models.CharField(
                        choices=[
                            (
                                "Phono Solar PS420M7GFH-18/VNH",
                                "Phono Solar PS420M7GFH-18/VNH",
                            ),
                            (
                                "Jinko Solar Tiger Neo N-type JKM420N-54HL4-B",
                                "Jinko Solar Tiger Neo N-type JKM420N-54HL4-B",
                            ),
                        ],
                        default="Phono Solar PS420M7GFH-18/VNH",
                        max_length=100,
                    ),
                ),
                ("modulleistungWp", models.PositiveIntegerField(default=420)),
                (
                    "modulanzahl",
                    models.PositiveIntegerField(
                        default=6,
                        validators=[django.core.validators.MinValueValidator(6)],
                    ),
                ),
                (
                    "garantieWR",
                    models.CharField(
                        choices=[
                            ("keine", "keine"),
                            ("15 Jahre", "15 Jahre"),
                            ("20 Jahre", "20 Jahre"),
                        ],
                        default="keine",
                        max_length=10,
                    ),
                ),
                ("eddi", models.BooleanField(default=False)),
                ("notstrom", models.BooleanField(default=False)),
                ("optimizer", models.BooleanField(default=False)),
                ("anzOptimizer", models.PositiveIntegerField(default=0)),
                (
                    "wallboxtyp",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Pulsar Plus", "Pulsar Plus"),
                            (
                                "Pulsar Plus inkl. Power Boost",
                                "Pulsar Plus inkl. Power Boost",
                            ),
                            ("Commander 2", "Commander 2"),
                            (
                                "Commander 2 Inkl. Power Boost",
                                "Commander 2 Inkl. Power Boost",
                            ),
                        ],
                        max_length=100,
                        null=True,
                    ),
                ),
                ("wallbox_anzahl", models.PositiveIntegerField(default=0)),
                (
                    "kabelanschluss",
                    models.FloatField(
                        default=10.0,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                ("hub_included", models.BooleanField(default=False)),
                (
                    "module_ticket",
                    models.CharField(
                        blank=True,
                        choices=[
                            (
                                "Phono Solar PS420M7GFH-18/VNH",
                                "Phono Solar PS420M7GFH-18/VNH",
                            ),
                            (
                                "Jinko Solar Tiger Neo N-type JKM420N-54HL4-B",
                                "Jinko Solar Tiger Neo N-type JKM420N-54HL4-B",
                            ),
                        ],
                        max_length=100,
                        null=True,
                    ),
                ),
                ("modul_anzahl_ticket", models.PositiveIntegerField(default=0)),
                ("optimizer_ticket", models.PositiveIntegerField(default=0)),
                ("batteriemodule_ticket", models.PositiveIntegerField(default=0)),
                ("notstrom_ticket", models.PositiveIntegerField(default=0)),
                ("eddi_ticket", models.PositiveIntegerField(default=0)),
                ("indiv_price_included", models.BooleanField(default=False)),
                (
                    "indiv_price",
                    models.FloatField(
                        default=0.0,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "solar_module_angebot_price",
                    models.FloatField(
                        default=0.0,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "batteriespeicher_angebot_price",
                    models.FloatField(
                        default=0.0,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "wallbox_angebot_price",
                    models.FloatField(
                        default=0.0,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "notstrom_angebot_price",
                    models.FloatField(
                        default=0.0,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "eddi_angebot_price",
                    models.FloatField(
                        default=0.0,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "optimizer_angebot_price",
                    models.FloatField(
                        default=0.0,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "angebotsumme",
                    models.FloatField(
                        default=0.0,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "fullticketpreis",
                    models.FloatField(
                        default=0.0,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
