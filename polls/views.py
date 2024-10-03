from datetime import date
from dateutil.relativedelta import relativedelta
from django.shortcuts import render
from .forms import DataCollectionForm
from django.http import JsonResponse
from .models import UserData
from django.db.models import Avg, F
from faker import Faker

def data_collection_view(request):
    if request.method == "POST":
        form = DataCollectionForm(request.POST)
        if form.is_valid():
            # Save the form data to the UserData model
            form.save()

            # Optionally, you can redirect to a success page or show a message
            return render(request, 'done.html')
    else:
        form = DataCollectionForm()
        max_date = date.today() - relativedelta(years=18)
        return render(request, 'data_collection.html', {'form': form, 'min_date': '1900-01-01', 'max_date': max_date.strftime('%Y-%m-%d')})
    
    # Assuming everyone is an adult
    max_date = date.today() - relativedelta(years=18)
    return render(request, 'data_collection.html', {'form': form, 'min_date': '1900-01-01', 'max_date': max_date.strftime('%Y-%m-%d')})

def create_dummy_data(request):
    fake = Faker()
    for _ in range(100):
        gender = fake.random.choice(['M', 'F'])
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=60)  # Adjust age range as needed
        year_joined = fake.year()
        unit_area = fake.random.choice([choice[0] for choice in UserData.DAS_CHOICES])
        function = fake.random.choice(['E', 'T', 'C', 'D'])

        user_data = UserData(
            gender=gender,
            birth_date=birth_date,
            year_joined=year_joined,
            unit_area=unit_area,
            function=function,
        )
        user_data.save()
    return render(request, 'done.html')

def graph_view(request):
    return render(request, 'graph.html')

def chart_data_questions(request):
    # Helper function to calculate age
    def calculate_age(birth_date):
        today = date.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    # Fetch all users
    users = UserData.objects.all()
    
    # Data structures to hold all the data for the charts
    data = {
        'decades': {area[0]: {} for area in UserData.DAS_CHOICES},
        'total_technicians': {area[0]: 0 for area in UserData.DAS_CHOICES},
        'average_age': {area[0]: {'total_age': 0, 'count': 0} for area in UserData.DAS_CHOICES},
        'before_2010': {area[0]: 0 for area in UserData.DAS_CHOICES},
        'gender_distribution': {area[0]: {'M': 0, 'F': 0} for area in UserData.DAS_CHOICES},
        'interns': {area[0]: 0 for area in UserData.DAS_CHOICES},
    }  

    min_decade, max_decade = 2030, 0
    
    # Populate data for each chart
    for user in users:
        
        if user.function == 'T':
            # 1. Technicians by Decades
            birth_year = user.birth_date.year
            decade = (birth_year // 10) * 10
            min_decade = min(decade, min_decade)
            max_decade = max(decade, max_decade)
            decade_str = f'{decade}s'
            if decade_str not in data['decades'][user.unit_area]:
                data['decades'][user.unit_area][decade_str] = 0
            data['decades'][user.unit_area][decade_str] += 1            

            # 2. Total Technicians per Unit Area
            data['total_technicians'][user.unit_area] += 1

            # 4. Technicians Joined Before 2010
            if user.year_joined < 2010:
                data['before_2010'][user.unit_area] += 1
        
        # 3. Average Age of Members per Area
        age = calculate_age(user.birth_date)
        data['average_age'][user.unit_area]['total_age'] += age
        data['average_age'][user.unit_area]['count'] += 1

        # 5. Gender Distribution in each area
        data['gender_distribution'][user.unit_area][user.gender] += 1

        # 6. Interns in each area
        if user.function == 'E':  # E stands for 'Estagiário' (Intern)
            data['interns'][user.unit_area] += 1

    for area in data['decades']:
        for decade in range(min_decade, max_decade + 1, 10):
            decade_str = f'{decade}s'
            if decade_str not in data['decades'][area]:
                data['decades'][area][decade_str] = 0
    
    # Calculate the average age for each unit
    for unit, values in data['average_age'].items():
        data['average_age'][unit] = values['total_age'] / values['count'] if values['count'] > 0 else 0

    return JsonResponse(data)