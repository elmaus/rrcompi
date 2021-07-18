from web.models import FormsActivation
from compi.forms import *
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from . models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, get_user_model, login, logout



def home(request):
    comps = Competition.objects.filter(is_open=True)
    context = {
        'title':'Competition',
        'comps':comps
    }
    return render(request, 'compi/home.html', context)

@login_required
def scoresheet_main(request):
    comp = Competition.objects.filter(is_open=True)
    user = RRUser.objects.filter(email=request.user.email).first()
    judge = Judge.objects.filter(user=user).first()

    if judge == None:
        logout(request)
        return redirect('web-login')
    print(judge)
        
    return render(request, 'compi/scoresheet-main.html', {'comp':comp})

@login_required
def scoresheet_list(request, id):
    comp = Competition.objects.filter(id=id).first()
    criterias = Criteria.objects.filter(competition=comp)
    contenders = Contender.objects.filter(competition=comp)
    user = RRUser.objects.filter(email=request.user.email).first()
    judge = Judge.objects.filter(user=user.id).first()

    if judge == None or judge.competition.id != comp.id:
        logout(request)
        return redirect('web-login')

    entries = []
    for c in contenders:
        entry = Entry.objects.filter(contender=c).first()
        if entry:
            scores = Score.objects.filter(entry=entry).filter(judge=judge)
            grade = 0
            for sc in scores:
                per = Criteria.objects.filter(name=sc.criteria.name, competition=comp).first()
                grade += round(per.percentage / 100 * sc.score, 2)
            entries.append({
                'contender':c,
                'title':entry.title,
                'score':grade,
                "entry_id":entry.id
            })

    context ={
        'entries':entries,
        'title':'Scoresheet',
        'comp_title':comp.title
    }
        
    # entries = Entry.objects.filter(competition=title)
    return render(request, 'compi/scoresheet-page.html', context)

@login_required
def scoresheet(request, entry_id):
    judge = Judge.objects.filter(user=request.user).first()
    comp = Competition.objects.filter(id=judge.competition.id).first()
    entry = Entry.objects.get(id=entry_id)
    scores = Score.objects.filter(entry=entry).filter(judge=judge)
    data = []

    if judge == None or judge.competition.id != comp.id:
        logout(request)
        return redirect('web-login')

    for s in scores:
        percentage = Criteria.objects.filter(name=s.criteria.name, competition=comp).first()
        data.append(
            {
                'score':s.score,
                'criteria':s.criteria.name,
                'percentage':percentage.percentage
            }
        )
    context = {
        'data':data,
        'need_to_comment':judge.need_comment,
        'comment':Comment.objects.filter(entry=entry, judge=judge).first(),
        'link':entry.link.replace('?channel=Copy-Link', '') + '/',
        'contender':entry.contender,
    }

    if request.method == "POST":
        criterias = Criteria.objects.filter(competition=comp)
        comment_qs = Comment.objects.filter(entry=entry, judge=judge).first()

        # updating judge's comment
        if judge.need_comment:
            comment_qs.comment = request.POST.get('comment')
            comment_qs.save()

        #updating judge's scores
        for i in criterias:
            s = Score.objects.filter(entry=entry, judge=judge, criteria=i).first()
            s.score = round(float(request.POST.get(i.name)), 2)
            s.save()

        return redirect('compi-scoresheet-list', comp.id)
        
    return render(request, 'compi/scoresheet.html', context)


def register_judge(request):
    active_form = FormsActivation.objects.all().first()

    context = {
        'active_form':active_form.judge_registration,
        'title':'Judge Registration Form',
        'comp':Competition.objects.filter(is_open=True)
    }
    if request.method == "POST":
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        name = request.POST.get('name')
        image = request.FILES.get('image')
        competition = request.POST.get('comp')

        context['name'] = name
        context['email'] = email
        context['ps1'] = password1
        context['ps2'] = password2
        
        comp = Competition.objects.filter(title=competition).first()

        if comp == None:
            context['title'] = "Response"
            context['feature'] = "Response"
            context['card-title'] = 'Invalid Input!'
            context['message'] = "You did not select any competition"
            context['linkto'] = 'compi-register-judge'

            return render(request, 'compi/response.html', context)

        user = RRUser.objects.filter(email=email)

        if user:
            context['title'] = "Response"
            context['feature'] = "Response"
            context['card-title'] = 'Registration Failed!'
            context['message'] = "{} is already registered".format(email)
            context['linkto'] = 'compi-register-judge'

            return render(request, 'compi/response.html', context)

        if password1 != password2:
            context['title'] = "Response"
            context['feature'] = "Response"
            context['card-title'] = 'Invalid Input!'
            context['message'] = "Passwords you provided did not matched!"
            context['linkto'] = 'compi-register-judge'

            return render(request, 'compi/response.html', context)

        new_user = RRUser(email=email, password=password1, title='judge')
        new_user.set_password(password1)
        new_user.save()

        new_judge = Judge(name=name, image=image, user=new_user, competition=comp)
        new_judge.save()

        context['title'] = 'Response'
        context['feature'] = "Response"
        context['ctitle'] = 'Registration Successful!'
        context['message'] = "You are now registered as {}'s Judge. Please ask our Comp Coordinator for more information".format(competition)
        context['linkto'] = 'compi-home'
        return render(request, 'compi/response.html', context)

    return render(request, 'compi/judge-registration-form.html', context)


def register_contender(request):
    active_form = FormsActivation.objects.all().first()
    context = {
        'active_form':active_form.contender_registration,
        'title':"Contender Registration Form",
        'comp':Competition.objects.filter(is_open=True)
    }
    
    if request.method == "POST":
        smule_name = request.POST.get('smule-name')
        line_name = request.POST.get('line-name')
        smule_name = request.POST.get('smule-name')
        image = request.FILES.get('image')
        competition = request.POST.get('comp')
        comp = Competition.objects.filter(title=competition).first()

        con = Contender.objects.filter(smule_name=smule_name, competition=comp)
        if con:
            context['title'] = "Response"
            context['card-title'] = 'Registration Failed!'
            context['message'] = "{} is already registered".format(smule_name)
            context['linkto'] = 'compi-register-contender'

            return render(request, 'compi/response.html', context)

        new = Contender(smule_name=smule_name, line_name=line_name, image=image, competition=comp)
        new.save()
    
        context['title'] = 'Response'
        context['feature'] = "Response"
        context['ctitle'] = 'Registration Successful!'
        context['message'] = "You are now a legitimate {}'s contender. Please submit your entry corresponding your smule name and link of your recording entry before the deadline of submission. Please ask our Comp Coordinator for more information".format(competition)
        context['linkto'] = 'compi-home'
        return render(request, 'compi/response.html', context)

    return render(request, 'compi/contender-registration-form.html', context)

def entry_form(request):
    active_form = FormsActivation.objects.all().first()
    comps = Competition.objects.filter(is_open=True)
    context = {
        'active_form':active_form.entry_form,
        'comps':comps
    }

    if request.method == 'POST':
        link = request.POST.get('link')
        smule_name = request.POST.get('smule-name')
        title = request.POST.get('title')
        competition = request.POST.get('comp')
        comp = Competition.objects.filter(id=competition).first()
        if comp == None:
            context['title'] = 'Response'
            context['feature'] = "Response"
            context['ctitle'] = 'Submission Failed!'
            context['message'] = "Please Select Your competiton"
            context['linkto'] = 'compi-entry-form'
            return render(request, 'compi/response.html', context)

        contender = Contender.objects.filter(smule_name=smule_name,  competition=comp).first()
        if contender == None or contender.competition != comp:
            context['title'] = 'Response'
            context['feature'] = "Response"
            context['ctitle'] = 'Submission Failed!'
            context['message'] = "{} is not registered as contenders or no longer part of the competition. Please ask our Comp Coordinator for more information".format(smule_name)
            context['linkto'] = 'compi-entry-form'
            return render(request, 'compi/response.html', context)

        already = Entry.objects.filter(contender=contender, competition=comp).first()
        if already:
            context['title'] = 'Response'
            context['freature'] = 'Response'
            context['ctitle'] = 'Submission Failed!'
            context['message'] = 'You already submitted an entry. Please ask our Comp Coodinator for more info'
            context['linkto'] = 'compi-entry-form'

            return render(request, 'compi/response.html', context)

        new_entry = Entry(link=link, title=title, contender=contender)
        new_entry.save()

        criterias = Criteria.objects.filter(competition=comp)
        judges = Judge.objects.filter(competition=comp)
        for j in judges:
            for c in criterias:
                score = Score(entry=new_entry, criteria=c, judge=j)
                score.save()
            new_comment = Comment(comment="Your comment here...", entry=new_entry, judge=j)
            new_comment.save()
        
        context['title'] = 'Response'
        context['feature'] = "Response"
        context['ctitle'] = 'Submission Successful!'
        context['message'] = "Your entry has been submited. Please ask our Comp Coordinator for more information".format(comp)
        context['linkto'] = 'compi-home'
        return render(request, 'compi/response.html', context)

    return render(request, 'compi/entry-form.html', context)
    

def submit_entry(request, id):
    active_form = FormsActivation.objects.all().first()
    comp = Competition.objects.filter(id=id).first()
    context = {
        'active_form':active_form.entry_form,
        'deadline':str(comp.submission_date).replace("pm", 'GMT+8')
    }

    if request.method == 'POST':
        link = request.POST.get('link')
        smule_name = request.POST.get('smule-name')
        title = request.POST.get('title')
        competition = request.POST.get('comp')

        contender = Contender.objects.filter(smule_name=smule_name,  competition=comp).first()
        if contender == None or contender.competition != comp:
            context['title'] = 'Response'
            context['feature'] = "Response"
            context['ctitle'] = 'Submission Failed!'
            context['message'] = "{} is not registered as contenders or no longer part of the competition. Please ask our Comp Coordinator for more information".format(smule_name)
            context['linkto'] = 'compi-entry-form'
            return render(request, 'compi/response.html', context)

        already = Entry.objects.filter(contender=contender, competition=comp).first()
        if already:
            context['title'] = 'Response'
            context['freature'] = 'Response'
            context['ctitle'] = 'Submission Failed!'
            context['message'] = 'You already submitted an entry. Please ask our Comp Coodinator for more info'
            context['linkto'] = 'compi-entry-form'

            return render(request, 'compi/response.html', context)

        new_entry = Entry(link=link, title=title, contender=contender, competition=comp)
        new_entry.save()

        criterias = Criteria.objects.filter(competition=comp)
        judges = Judge.objects.filter(competition=comp)
        for j in judges:
            for c in criterias:
                score = Score(entry=new_entry, criteria=c, judge=j)
                score.save()
            new_comment = Comment(entry=new_entry, judge=j)
            new_comment.save()
        
        context['title'] = 'Response'
        context['feature'] = "Response"
        context['ctitle'] = 'Submission Successful!'
        context['message'] = "Your entry has been submited. Please ask our Comp Coordinator for more information".format(comp)
        context['linkto'] = 'compi-home'
        return render(request, 'compi/response.html', context)

    return render(request, 'compi/entry-form.html', context)
    


def competition_result(request, id):
    comp = Competition.objects.filter(id=id).first()
    contenders = Contender.objects.filter(competition=comp)
    judges = Judge.objects.filter(competition=comp)

    all_score_by_judges = [] # for every entry/ 2 dimmentional list
    all_score_by_judges_ordered = []

    judges_name = []
    for j in judges:
        judges_name.append(j.name)

    for contender in contenders:
        entry = Entry.objects.filter(contender=contender).first()
        if entry != None:
            judges_scores = []
            average = 0
            for judge in judges:
                scores = Score.objects.filter(entry=entry, judge=judge)
                total = 0
                for score in scores:
                    percentage = score.criteria.percentage
                    grade = percentage / 100 * score.score
                    total += grade
                judges_scores.append({
                    'judge':judge.name,
                    'score':round(total,  2)
                })
                average += total
            all_score_by_judges.append({
                'name':contender.smule_name,
                'average':round(average / len(judges), 2),
                'judges_score':judges_scores,
                'entry_id':entry.id,
                'immage':contender.immage.url
            })

    highest = None
    while len(all_score_by_judges) > 0:
        for i in range(len(all_score_by_judges)):
            if i == 0:
                highest = all_score_by_judges[0]
                continue
            if all_score_by_judges[i]['average'] > highest['average']:
                highest = all_score_by_judges[i]
        all_score_by_judges.pop(all_score_by_judges.index(highest))
        all_score_by_judges_ordered.append(highest)

    # creating list for ranking model
    ranking_model = []
    for r in all_score_by_judges_ordered:
        if r['average'] not in ranking_model:
            ranking_model.append(r['average'])


    for one in all_score_by_judges_ordered:
        for i in range(len(ranking_model)):
            if one['average'] == ranking_model[i]:
                one['rank'] = i + 1

    context = {
        'scores':all_score_by_judges_ordered,
        'judges':judges_name,
        'comp_title':comp.title
    }

    return render(request, 'compi/competition-result.html', context)


def result_info(request, entry_id):
    entry = Entry.objects.filter(id=entry_id).first()
    comp = entry.competition
    judges = Judge.objects.filter(competition=comp)
    contender = entry.contender.smule_name
    scores = Score.objects.filter(entry=entry)

    data = []
    criterias = []
    for judge in judges:
        judge_scores = Score.objects.filter(entry=entry, judge=judge)
        all_score = []
        for score in judge_scores:
            if score.criteria.name not in criterias:
                criterias.append(score.criteria.name)
            all_score.append({
                'grade':score.score,
                'percentage':score.criteria.percentage,
                'score':round(score.criteria.percentage / 100 * score.score, 2)
            })
        total = 0
        for all in all_score:
            total += all['score']
        data.append({
            'info':all_score,
            'total':total,
            'judge':judge.name
        })
    grand_total = 0
    for d in data:
        grand_total += d['total']
    
    spacing = []
    for i in criterias:
        spacing.append('-')

    all_comments = Comment.objects.filter(entry=entry)
    comments = []
    for comment in all_comments:
        if comment.comment != None:
            comments.append(comment)

    context = {
        'data':data,
        'criterias':criterias,
        'spacing':spacing,
        'total':round(grand_total / len(judges), 2),
        'comments':comments,
        'contender':contender
    }

            
    return render(request, 'compi/result-info.html',  context)

