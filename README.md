# Django Inventory Management
A deliberately simple Django app for managing inventory at an IT enterprise. This app produces straight-forward HTML with very simple CSS.  It is meant to be plugged in to Django's admin or similar backend database management app.

## Installing
Clone the repo into a Django project.

```
git clone https://github.com/checarlos87/django-inventory-management.git
```

Rename the cloned directory as "inventory".
```
mv django-inventory-management inventory
```

Add the app to your project's INSTALLED_APPS (in settings.py).
```
INSTALLED_APPS = [ 
    'inventory.apps.InventoryConfig',
    ...
]
```

Migrate the app's models.
```
python manage.py makemigrations inventory
python manage.py migrate
```

(optional) If you're going to run the code in production (not in Django's development server), you'll want to make sure you've created a static/ directory to hold static files (stylesheets, in the case of this app) and then you'll want to collect those static files into the static/ directory using manage.py.
```
python manage.py collectstatic
```
  
  * More details on Django's handling of static files in Django's [docs](https://docs.djangoproject.com/en/1.9/howto/static-files/#deployment).

## Model
The model defines a base Equipment class from which many other classes inherit, including the Host class.  The Host class also has its own subclasses: PhysHost and VMHost for representing physical and virtual hosts, respectively.  The model makes no assumption about which hypervisor may actually be used for the VMHosts.  

The model also provides an abstract class CloudMember which is meant to be used to group hosts together in "clouds".  An example subclass BaculaCloudMember (for keeping record of hosts in a Bacula infrastructure cloud) is provided. 

The rest of the classes are small and closely bound to the Equipment classes.  The Netiface class deserves special explanation.  It is a table for holding data about a host's public network interface.  Since it is so closely bound to the Host table, Netiface would be thought of as a weak entity in a database ER diagram.  The current model only uses one Netiface per host, but the way it is implemented allows for associating more than one Netiface relation with a single host.

Finally, the Service class is meant to keep services that hosts may run such as ssh, apache, nginx, django, etc.

Here is a full listing of the model classes:
* Equipment
  * PC
  * Misc
  * Switch
  * Jbod
  * Host
    * PhysHost
    * VMHost
* CloudMember (abstract)
  * BaculaCloudMember
* Employee
* MiscType
* Building
* WebSite
* Netiface
* Service
* HostOS
* SwitchOS

## View/Templates
The views and templates are very simple.  They provide list and detail views of various models.  You can think of them as a "read-only" version of the Django admin app.
