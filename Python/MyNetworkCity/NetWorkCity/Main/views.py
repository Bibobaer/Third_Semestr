from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from Main.Database import *
import asyncio
# Create your views here.

def hash_func(data: str) -> str:
    sum = 0
    for i in data:
        sum += ord(i)
    return hex(sum)

def index(request):
    request.session['username'] = None

    try:
        datebase = DataBase()
        asyncio.run(datebase.initialize_connection())
    except Exception:
        print("Not connect")
    
    cnt_users = asyncio.run(datebase.get_count_students())
    cnt_sub = asyncio.run(datebase.get_count_subjects())

    print(cnt_users, cnt_sub)

    return render(request, "index.html", {'users' : cnt_users, 
                                          'subjects' : cnt_sub})

def MyDiary(request):
    user_data = request.session.get('username')
    if (user_data is None):
        return redirect('login')
    
    db = DataBase()
    asyncio.run(db.initialize_connection())

    grades = asyncio.run(db.get_grade_of_student(user_data))

    subjects = list(grades.keys())
    dates = sorted(set(date for tup in grades.values() for date, _ in tup))
    
    table_data = {subject: {date: '' for date in dates} for subject in subjects}
    
    for subject, lis in grades.items():
        for (date, grade) in lis:
            table_data[subject][date] = grade

    context = {
        'username' : user_data,
        'table_data': table_data,
        'subjects': subjects,
        'dates': dates
    }

    return render(request, 'mydiary.html', context)

def Login(request):
    request.session['username'] = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        hash_pswd = hash_func(password)

        try:
            db = DataBase()
            asyncio.run(db.initialize_connection())
        except:
            print("123")

        if (asyncio.run(db.is_user_exists(username, hash_pswd))):
            request.session['username'] = username 
            if (asyncio.run(db.is_teacher(username))):
                return HttpResponseRedirect('elecdiary') 
            return HttpResponseRedirect('mydiary')
        else:
            return render(request, 'login.html', {'error': 'Неверный логин или пароль'})
    return render(request, 'login.html')

def ElectronicDiary(request):
    user_data = request.session.get('username')
    if (user_data is None):
        return redirect('login')
    db = DataBase()
    asyncio.run(db.initialize_connection())
    all_students_login = asyncio.run(db.get_students_login())

    dict_of_students = {}
    for elem in all_students_login:
        dict_of_students[elem] = asyncio.run(db.get_grade_of_student(elem))

    for i,v in dict_of_students.items():
        for k in v.keys():
            dict_of_students[i][k] = list(dict_of_students[i][k])

    result_list = []

    for k, grades in dict_of_students.items():
        context = {}
        subjects = list(grades.keys())
        dates = sorted(set(date for tup in grades.values() for date, _ in tup))

        table_data = {subject: {date: '0' for date in dates} for subject in subjects}
    
        for subject, lis in grades.items():
            for (date, grade) in lis:
                table_data[subject][date] = str(grade)

        context[k] = {  'table_data': table_data,
                        'subjects': subjects,
                        'dates': dates
                    }
        result_list.append(context)

    if request.method == 'POST':
        for user in result_list:
            for login, some_dict in user.items():
                for subject in some_dict['subjects']:
                    for date in some_dict['dates']:
                        for key, grade in some_dict['table_data'][subject].items():
                            result_req = login+"_"+subject+"_"+grade+"_"+date
                            mark = request.POST.get(result_req)
                            if mark is None or mark =='':
                                continue

                            log_id = asyncio.run(db.get_id_by_login(login))
                            sub_id = asyncio.run(db.get_id_by_subject(subject))
                            
                            
                            if (grade == '0'):
                                if (asyncio.run(db.is_grade_exists(log_id, sub_id, int(mark), date))):
                                    continue
                                asyncio.run(db.add_grade(log_id, sub_id, int(mark), date))
                                some_dict['table_data'][subject][key] = mark
                                continue

                            if (asyncio.run(db.is_new_grade(log_id, sub_id, int(mark), date))):
                                print(1, login, subject, mark, date)
                                asyncio.run(db.update_grade(log_id, sub_id, int(mark), date))

                            some_dict['table_data'][subject][key] = mark
                            

        render(request, 'elecdiary.html', {'lists': result_list, 'username' : user_data})

    #print(result_list)
    return render(request, 'elecdiary.html', {'lists' : result_list, 'username' : user_data})