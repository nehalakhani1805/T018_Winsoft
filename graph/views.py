import json

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Input
from django.http import JsonResponse
from .forms import InputForm

# Create your views here.
dMessage = ''
ChineseBases = ''


@login_required
def post_new(request):
    global ChineseBases
    global dMessage
    if request.method == "POST":
        form = InputForm(request.POST)
        if form.is_valid():
            input = form.save(commit=False)
            input.user = request.user
            input.save()
            # data = 'Cnwvtus KuaiTaa rlodeeurethn  an Ia_mrhs baer oag ndC_a aeoat dLj lLdio_me  p  hagZLngan _'
            # data='TiushsrtsYT_ oe_i  _'

            data = input.enc_string
            key = input.key
            k_list = [key[i] for i in range(len(key))]
            k_ind_list = sorted(range(len(k_list)), key=lambda k: k_list[k])

            k_len = len(key)
            data_len = len(data)
            rows, cols = (data_len // k_len, k_len)

            code = [[0 for i in range(rows)] for j in range(cols)]

            ctr = 0
            for i in range(cols):
                for j in range(rows):
                    code[i][j] = data[ctr]
                    ctr += 1

            final_msg = []

            for i in range(len(k_ind_list)):
                for j in range(len(k_ind_list)):
                    if i == k_ind_list[j]:
                        final_msg.append(code[j])
                        break

            s = ""
            for i in range(rows):
                for j in range(len(final_msg)):
                    if final_msg[j] != 0:
                        s = s + final_msg[j][i]
            while '_' in s:
                s = s[:-1]
            dMessage = s

            data = dMessage.lower()
            data_dict = {
                'khardung la': 0,
                'lachulung la': 0,
                'sasser pass': 0,
                'gyong la': 0,
                'sia la': 0,
                'zoji la': 0,
                'indira col': 0,
                'rezang la': 0,
                'tanglang la': 0,
                'pensi la': 0,
                'marsimik la': 0,
                'not': 0,
                "haven't": 0,
                "didn't": 0,
                "couldn't": 0
            }
            not_words = ['not', "haven't", "didn't", "couldn't"]
            all_chini_places = ['khardung la', 'lachulung la', 'sasser pass', 'gyong la', 'sia la', 'zoji la',
                                'indira col', 'rezang la', 'tanglang la', 'pensi la', 'marsimik la']
            chini_places = []

            flag = 0

            for i in data_dict.keys():
                if i in data:
                    data_dict[i] += 1
                    chini_places.append(i)
                if i in data and i in not_words:
                    flag += 1

            if flag % 2 == 1:
                for place in all_chini_places:
                    if place in chini_places:
                        all_chini_places.remove(place)
                print(all_chini_places)


                ChineseBases = all_chini_places
            else:
                print(chini_places)
                ChineseBases = chini_places

    else:
        form = InputForm()
        ChineseBases = ''
        dMessage=''

    return render(request, 'graph/post_input.html', {'form': form, 'dMessage': dMessage, 'ChineseBases': ChineseBases})


@login_required
def view_graph(request):
    data_dict = {
        'khardung la': 0,
        'lachulung la': 0,
        'sasser pass': 0,
        'gyong la': 0,
        'sia la': 0,
        'zoji la': 0,
        'indira col': 0,
        'rezang la': 0,
        'tanglang la': 0,
        'pensi la': 0,
        'marsimik la': 0,
    }
    global ChineseBases
    sources = []
    goals = []
    for bases in ChineseBases:
        data_dict[bases.lower()] += 1
    for index, item in enumerate(data_dict.items()):
        if item[1] != 1:
            sources.append(index)
        else:
            goals.append(index)
    print(goals)
    print(sources)
    # goals.pop()
    data_dictionary = {
        'goals': goals,
        'sources': sources
    }
    dataJSON = json.dumps(data_dictionary)
    return render(request, 'graph/graph.html', {'data': dataJSON})

