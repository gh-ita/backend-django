from django.db import migrations

def populate_coverage_types(apps, schema_editor):
    Coverage_type = apps.get_model('analysis', 'Coverage_type')  

    coverage_choices = [
        ('bodily_injury_liability', 'Bodily Injury Liability'),
        ('personal_injury_protection', 'Personal Injury Protection'),
        ('property_damage_liability', 'Property Damage Liability'),
        ('collision', 'Collision'),
        ('comprehensive', 'Comprehensive'),
    ]

    for coverage in coverage_choices:
        Coverage_type.objects.get_or_create(name=coverage[0])

class Migration(migrations.Migration):

    dependencies = [
        ("analysis", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(populate_coverage_types),
    ]

