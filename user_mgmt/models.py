from django.db import models
from admin_console.models import User
from indian_cities.dj_city import cities  # Ensure this package is installed

def get_city_state_choices():
    choices = []
    for state_tuple in cities:
        state_name = state_tuple[0]
        for city_tuple in state_tuple[1]:
            city_name = city_tuple[0]
            choices.append((city_name, f"{city_name}, {state_name}"))
    return choices

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)  # Use primary key from User
    mobile_number = models.CharField(max_length=10, unique=True, default=None)
    address = models.CharField(max_length=255, default=None)
    city = models.CharField(choices=get_city_state_choices(), max_length=100, default=None)
    state = models.CharField(max_length=100, blank=True)  # State field can be blank initially
    country = models.CharField(max_length=50, default='India')  # Default to India

    def save(self, *args, **kwargs):
        # Automatically set state based on selected city
        if self.city:
            # Extract the state from the city selection
            city_state = dict(get_city_state_choices())
            state_name = city_state.get(self.city, '').split(', ')[-1]
            self.state = state_name  # Set the state
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.firstname}'s Profile"  # Assuming firstname is the display name
