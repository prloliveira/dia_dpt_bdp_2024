from datetime import date
from django.shortcuts import render
from .forms import DataCollectionForm
from django.http import JsonResponse
from .models import UserData
from django.db.models import Avg, Count, F
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
        return render(request, 'data_collection.html', {'form': form})
    
    return render(request, 'data_collection.html', {'form': form})




def graph_view(request):
    # a) Quantos técnicos da AFI nasceram na década de 1970?
    afi_1970s = UserData.objects.filter(unit_area='AFI', birth_date__year__gte=1970, birth_date__year__lt=1980).count()

    # b) Quantos técnicos existem no total (presentes) na ASB?
    asb_total = UserData.objects.filter(unit_area='ASB').count()

    # c) Idade média dos colaboradores da AAS? 
    current_year = date.today().year
    aas_mean_age = UserData.objects.filter(unit_area='AAS').annotate(
        age=current_year - F('birth_date__year')
    ).aggregate(mean_age=Avg('age'))['mean_age']

    # d) Quantos técnicos da AII entraram no Banco antes de 2010?
    aii_pre_2010 = UserData.objects.filter(unit_area='AII', year_joined__lt=2010).count()

    # e) Quantas mulheres/homens existem na UATP?
    uatp_women = UserData.objects.filter(unit_area='UATP', gender='F').count()
    uatp_men = UserData.objects.filter(unit_area='UATP', gender='M').count()

    # f) Em que ano entraram os membros da Direção para o Banco?
    direcao_years = UserData.objects.filter(unit_area='DIR').values_list('year_joined', flat=True)

    context = {
        'afi_1970s': afi_1970s,
        'asb_total': asb_total,
        'aas_mean_age': aas_mean_age,
        'aii_pre_2010': aii_pre_2010,
        'uatp_women': uatp_women,
        'uatp_men': uatp_men,
        'direcao_years': list(direcao_years),
    }
    return render(request, 'graph.html', context)

from django.http import JsonResponse
from django.db.models import Count

from django.http import JsonResponse
from django.db.models import Count


def bar_chart_data_view(request):
    # Available areas from the DAS_CHOICES field of the UserData model
    areas = [choice[0] for choice in UserData.DAS_CHOICES]

    # Define decades dynamically (1970, 1980, ..., 2020)
    decades = [(1970 + i * 10) for i in range(6)]  # From 1970 to 2020

    # Initialize a dictionary to store counts per area for each category
    data_per_area = {
        'decade': {},
        'department': {},
        'gender': {},
        'function': {},
    }

    # Calculate counts for decades
    for area in areas:
        counts_per_decade = []
        for decade in decades:
            count = UserData.objects.filter(
                unit_area=area,
                birth_date__year__gte=decade,
                birth_date__year__lt=decade + 10
            ).count()
            counts_per_decade.append(count)
        
        data_per_area['decade'][area] = counts_per_decade

    # Count users per department
    for area in areas:
        count = UserData.objects.filter(unit_area=area).count()
        data_per_area['department'][area] = count

    # Count users by gender
    for area in areas:
        data_per_area['gender'][area]['Masculino'] = UserData.objects.filter(gender='M', unit_area=area).count()
        data_per_area['gender'][area]['Feminino'] = UserData.objects.filter(gender='F', unit_area=area).count()
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    print(data_per_area)

    # Count users by function
    for func, func_name in [('E', 'Estagiário'), ('T', 'Técnico'), ('C', 'Coordenador'), ('D', 'Direção')]:
        for area in areas:
            data_per_area['function'][area][func_name] = UserData.objects.filter(function=func, unit_area=area).count()

    # Prepare the response data
    data = {
        'decades': decades,
        'data_per_area': data_per_area
    }

    return JsonResponse(data)



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


def chart_data_questions(request):
    # Helper function to calculate age
    def calculate_age(birth_date):
        today = date.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    
    direction_members = UserData.objects.filter(unit_area='DIR').order_by('year_joined')
    min_year, max_year = direction_members.first().year_joined, direction_members.last().year_joined

    # Data structures to hold all the data for the charts
    data = {
        'decades': {area[0]: {} for area in UserData.DAS_CHOICES},
        'total_technicians': {area[0]: 0 for area in UserData.DAS_CHOICES},
        'average_age': {area[0]: {'total_age': 0, 'count': 0} for area in UserData.DAS_CHOICES},
        'before_2010': {area[0]: 0 for area in UserData.DAS_CHOICES},
        'gender_distribution': {area[0]: {'M': 0, 'F': 0} for area in UserData.DAS_CHOICES},
        'interns': {area[0]: 0 for area in UserData.DAS_CHOICES},
        'direction_membership': {year: 0 for year in range(min_year, max_year+1)}
    }

    # Fetch all users
    users = UserData.objects.all()

    # Populate data for each chart
    for user in users:
        # 1. Technicians by Decades
        birth_year = user.birth_date.year
        decade = f'{(birth_year // 10) * 10}s'
        if decade not in data['decades'][user.unit_area]:
            data['decades'][user.unit_area][decade] = 0
        data['decades'][user.unit_area][decade] += 1

        # 2. Total Technicians per Unit Area
        data['total_technicians'][user.unit_area] += 1

        # 3. Average Age of Technicians per Area
        age = calculate_age(user.birth_date)
        data['average_age'][user.unit_area]['total_age'] += age
        data['average_age'][user.unit_area]['count'] += 1

        # 4. Technicians Joined Before 2010
        if user.year_joined < 2010:
            data['before_2010'][user.unit_area] += 1

        # 5. Gender Distribution in each area
        data['gender_distribution'][user.unit_area][user.gender] += 1

        # 6. Interns in each area
        if user.function == 'E':  # E stands for 'Estagiário' (Intern)
            data['interns'][user.unit_area] += 1

    for direction_member in direction_members:
        data['direction_membership'][direction_member.year_joined] += 1

    # Calculate the average age for each unit
    for unit, values in data['average_age'].items():
        data['average_age'][unit] = values['total_age'] / values['count'] if values['count'] > 0 else 0

    return JsonResponse(data)

