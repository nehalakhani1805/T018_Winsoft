from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Input
from django.http import JsonResponse
from .forms import InputForm


# Create your views here.

@login_required
def post_new(request):
    dMessage = ''
    if request.method == "POST":
        form = InputForm(request.POST)
        if form.is_valid():
            input = form.save(commit=False)
            input.user = request.user
            input.save()
            # data = 'Cnwvtus KuaiTaa rlodeeurethn  an Ia_mrhs baer oag ndC_a aeoat dLj lLdio_me  p  hagZLngan _'  # input()
            # data='TiushsrtsYT_ oe_i  _'

            # key = "delhi"  # input()
            data = input.enc_string
            key = input.key
            k_list = [key[i] for i in range(len(key))]
            k_ind_list = sorted(range(len(k_list)), key=lambda k: k_list[k])

            # print(k_list)
            # print(k_ind_list)

            k_len = len(key)
            data_len = len(data)
            rows, cols = (data_len // k_len, k_len)

            # print(k_len,data_len)

            code = [[0 for i in range(rows)] for j in range(cols)]
            # rowXcol==dataXkey
            ctr = 0
            for i in range(cols):
                for j in range(rows):
                    code[i][j] = data[ctr]
                    ctr += 1

            # print(code)

            final_msg = []

            for i in range(len(k_ind_list)):
                for j in range(len(k_ind_list)):
                    if i == k_ind_list[j]:
                        final_msg.append(code[j])
                        break

            # print('\n\n',final_msg)

            s = ""
            for i in range(rows):
                for j in range(len(final_msg)):
                    if final_msg[j] != 0:
                        s = s + final_msg[j][i]
            dMessage = s

    else:
        form = InputForm()
    return render(request, 'graph/post_input.html', {'form':form, 'dMessage':dMessage})

@login_required
def view_graph(request):
    return render(request, 'graph/graph.html')