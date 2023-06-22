import random
from django.db import transaction
from datetime import datetime
from vertrieb_interface.models import VertriebAngebot


def load_vertrieb_angebot(data, user, kurz):
    try:
        with transaction.atomic():
            for item in data:
                if not VertriebAngebot.objects.filter(zoho_id=item["zoho_id"]).exists():
                    if not item.get("zoho_kundennumer"):
                        print(
                            f"Missing zoho_kundennumer for {item['name']}, skipping..."
                        )
                        continue
                    print(f"Creating VertriebAngebot for {item['name']}...")
                    item["user"] = user
                    item["angebot_id"] = generate_angebot_id(
                        item.get("anfrage_vom"), kurz
                    )
                    email = item.get("email")
                    if not email:
                        item["email"] = "keine@email.com"
                    if (
                        "ü" in item.get("email")
                        or "ö" in item.get("email")
                        or "ä" in item.get("email")
                        or "_" in item.get("email")
                        or item.get("email")[1] == "."
                    ):
                        item["email"] = (
                            item.get("email")
                            .replace("ö", "o")
                            .replace("ä", "a")
                            .replace("ü", "u")
                            .replace("_", "-")
                        )
                    termine_text = item.get("termine_text")

                    try:
                        instance = VertriebAngebot(**item)
                        instance.full_clean()
                        instance.save()
                    except:
                        item["email"] = "keine@email.com"
                        instance = VertriebAngebot(**item)
                        instance.full_clean()
                        instance.save()

                    print(f"VertriebAngebot for {item['name']} created successfully")

        return "All data has been successfully processed."

    except Exception as e:
        print(f"An error occurred: {e}")


def generate_angebot_id(date_string, kurz):
    if not date_string:
        date_string = random.randint(100000, 999999)
        random_number = random.randint(100000, 999999)
        return f"AN-{kurz}{date_string}-{random_number}"
    else:
        anfrage_vom_date = datetime.strptime(date_string, "%d-%b-%Y")
        random_number = random.randint(100000, 999999)
        return f"AN-{kurz}{anfrage_vom_date.strftime('%d%m%Y')}-{random_number}"
