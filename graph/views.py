import json

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Input, Vertex, Edge
from django.http import JsonResponse
from .forms import InputForm, AddNodeForm, DeleteNodeForm, AddEdgeForm, DeleteEdgeForm


# Create your views here.

dMessage = ''
ChineseBases = ''

def home(request):
    return render(request, 'graph/home.html')

#  data = dMessage.lower()
#             predictor = flair.data.Sentence(data)
#             flair_sentiment.predict(predictor)
#             total_sentiment = predictor.labels
#             data_dict = {
#                 'khardung la': 0,
#                 'lachulung la': 0,
#                 'sasser pass': 0,
#                 'gyong la': 0,
#                 'sia la': 0,
#                 'zoji la': 0,
#                 'indira col': 0,
#                 'rezang la': 0,
#                 'tanglang la': 0,
#                 'pensi la': 0,
#                 'marsimik la': 0,
#                 'not': 0,
#                 "haven't": 0,
#                 "didn't": 0,
#                 "couldn't": 0
#             }
#             not_words = ['not', "haven't", "didn't", "couldn't"]
#             vertices=Vertex.objects.all()
#             all_chini_places = []
#             for vertex in vertices:
#                 temps = str(vertex.name).lower()
#                 all_chini_places.append(temps)
#             # all_chini_places = ['khardung la', 'lachulung la', 'sasser pass', 'gyong la', 'sia la', 'zoji la',
#                                 # 'indira col', 'rezang la', 'tanglang la', 'pensi la', 'marsimik la']
#             chini_places = []

#             flag = 0
#             if("POSITIVE" in str(total_sentiment[0])):
#                 print("Positive sentiment detected")
#                 flag = 1
#                 for i in all_chini_places:
#                     if i in data:
#                         chini_places.append(i)
#                 # for i in data_dict.keys():
#                 #     if i in data:
#                 #         data_dict[i] += 1
#                 #         chini_places.append(i)
#             elif("NEGATIVE" in str(total_sentiment[0])):
#                 print("Negative sentiment detected")
#                 flag = 1
#             print(chini_places)
#             # for i in data_dict.keys():
#             #     if i in data:
#             #         data_dict[i] += 1
#             #         chini_places.append(i)
#             #     if i in data and i in not_words:
#             #         flag += 1
@login_required
def post_new(request):
    import flair
    flair_sentiment = flair.models.TextClassifier.load('en-sentiment')
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
            predictor = flair.data.Sentence(data)
            flair_sentiment.predict(predictor)
            total_sentiment = predictor.labels

            vertices=Vertex.objects.all()
            all_chini_places = []
            for vertex in vertices:
                all_chini_places.append(str(vertex.name).lower())
            # all_chini_places = ['khardung la', 'lachulung la', 'sasser pass', 'gyong la', 'sia la', 'zoji la',
                                # 'indira col', 'rezang la', 'tanglang la', 'pensi la', 'marsimik la']
            chini_places = []
            other_places = []
            for i in all_chini_places:
                if i in data:
                    chini_places.append(i)
                else:
                    other_places.append(i)
            flag = 0
            if("POSITIVE" in str(total_sentiment[0])):
                print("Positive sentiment detected")
                flag = 0
            elif("NEGATIVE" in str(total_sentiment[0])):
                print("Negative sentiment detected")
                flag = 1

            if flag % 2 == 1:
                print(other_places)
                ChineseBases = other_places
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
    vertices=Vertex.objects.all()
    v=[] 
    labels=[] 
    ch=65
    for vertex in vertices:
        v1=[]
        v1.append(vertex.x_val)
        v1.append(vertex.y_val)
        v.append(v1)
        labels.append(str(vertex.code))
        ch=ch+1
    #labels.sort()
    print(v)
    print(labels)
    edges=Edge.objects.all()
    ed=[]
    for edge in edges:
        e=[]
        e.append(labels.index(str(edge.v_one)))
        e.append(labels.index(str(edge.v_two)))
        e.append(int(edge.diff))
        #e.append(ord(str(edge.v_one))-65)
        #e.append(ord(str(edge.v_two))-65)
        ed.append(e)
    print(ed)

    # # data_dict = {
    #     'khardung la': 0,
    #     'lachulung la': 0,
    #     'sasser pass': 0,
    #     'gyong la': 0,
    #     'sia la': 0,
    #     'zoji la': 0,
    #     'indira col': 0,
    #     'rezang la': 0,
    #     'tanglang la': 0,
    #     'pensi la': 0,
    #     'marsimik la': 0,
    # }
    global ChineseBases
    sources = []
    goals = []
    codes = []
    for bases in ChineseBases:
        for vertex in Vertex.objects.filter(name=bases.title()):
            codes.append(vertex.code)
    print(codes)
        # data_dict[bases.lower()] += 1
    # for index, item in enumerate(data_dict.items()):
        # if item[1] != 1:
    for code in codes:
        for i in range(len(labels)):
            if labels[i] == code:
                goals.append(i)
    
    for i in range(len(labels)):
        if i not in goals:
            sources.append(i)
    labels2=[]
    for i in range(len(labels)):
        labels2.append(str(Vertex.objects.filter(code=labels[i]).first().name))
    #print("labels2"+labels2)
    print(sources)
    #goals.pop()
    pr=[]
    sz=[]
    for i in range(len(v)):
        #pr.append(v[i])
        pr.append(i)
        sz.append(1)
    for i in range(len(ed)):
        #union(pr,ed[i][0],ed[i][1],v)
        union(pr,ed[i][0],ed[i][1],sz)

    #for i in len(pr):
    print("pr values")
    print(pr)
    flag=False
    print("goals[0]")
    print(goals)
    temp=pr[goals[0]]
    for i in range(len(goals)):
        if pr[goals[i]]!=temp:
            flag=True
            break
    diction={}
    if flag==True:
        for i in range(len(goals)):
            if pr[goals[i]] in diction:
                diction[pr[goals[i]]].append(goals[i])
            else:
                diction[pr[goals[i]]]=[]
                diction[pr[goals[i]]].append(goals[i])
        maxi=0
        max_key=0
        for key in diction:
            if len(diction[key])>maxi:
                maxi=len(diction[key])
                max_key=key
        goals=diction[max_key]
        sources=[]
        for i in range(len(labels)):
            if i not in goals:
                sources.append(i)
    data_dictionary = {
        'V': v,
        'E':ed,
        'labels':labels,
        'labels2':labels2,
        'goals': goals,
        'sources': sources
    }
    print("goals")
    print(goals)
    dataJSON = json.dumps(data_dictionary)
    return render(request, 'graph/graph.html', {'data': dataJSON})

def root(pr,r):#,v):
    r2=r
    while pr[r2]!=r2:
        #v[r]=p[r]
        #pr[r]=pr[pr[r]]
        r2=pr[r2]
    
    while r != r2:
        node_in_way = pr[r]
        pr[r] = r2
        r = node_in_way

    #return v[r]
    return r2
def union(pr,q,r,sz):
    r1=root(pr,q)#,v)
    r2=root(pr,r)#,v)
    
    if(r1!=r2):
        if sz[r1]>sz[r2]:
            pr[r2]=r1
            sz[r1]+=sz[r2]
        else:
            pr[r1]=r2
            sz[r2]+=sz[r1]
@login_required
def add_node(request):
    vertices=Vertex.objects.all()
    v=[]
    labels=[]
    for vertex in vertices:
        v1=[]
        v1.append(vertex.x_val)
        v1.append(vertex.y_val)
        v.append(v1)
        labels.append(str(vertex.code))
    #labels.sort()
    print(v)
    print(labels)
    edges=Edge.objects.all()
    ed=[]
    for edge in edges:
        e=[]
        e.append(labels.index(str(edge.v_one)))
        e.append(labels.index(str(edge.v_two)))
        #e.append(ord(str(edge.v_one))-65)
        #e.append(ord(str(edge.v_two))-65)
        ed.append(e)
    print(ed)
    labels2=[]
    for i in range(len(labels)):
        labels2.append(str(Vertex.objects.filter(code=labels[i]).first().name))
    print("labels2")
    print(labels2)
    data_dictionary = {
        'V': v,
        'E':ed,
        'labels':labels,
        'labels2':labels2
    }
    dataJSON = json.dumps(data_dictionary)
    if request.method == "POST":
        form = AddNodeForm(request.POST)
        if form.is_valid():
            print("form valid")
            input = form.save(commit=False)
            vertices=Vertex.objects.all()
            maxi=0
            for vertex in vertices:
                if ord(str(vertex.code))>maxi:
                    maxi=ord(str(vertex.code))
            temp=chr(maxi+1)
            input.code = temp
            input.save()
            return redirect('add_node')
    else:
        print("form not valid")
        form = AddNodeForm()
    return render(request, 'graph/post_addnode.html', {'form': form,'data':dataJSON})


@login_required
def delete_node(request):
    vertices=Vertex.objects.all()
    v=[]
    labels=[]
    for vertex in vertices:
        v1=[]
        v1.append(vertex.x_val)
        v1.append(vertex.y_val)
        v.append(v1)
        labels.append(str(vertex.code))
    #labels.sort()
    print(v)
    print(labels)
    edges=Edge.objects.all()
    ed=[]
    for edge in edges:
        e=[]
        e.append(labels.index(str(edge.v_one)))
        e.append(labels.index(str(edge.v_two)))
        #e.append(ord(str(edge.v_one))-65)
        #e.append(ord(str(edge.v_two))-65)
        ed.append(e)
    print(ed)
    labels2=[]
    for i in range(len(labels)):
        labels2.append(str(Vertex.objects.filter(code=labels[i]).first().name))
    print("labels2")
    print(labels2)
    data_dictionary = {
        'V': v,
        'E':ed,
        'labels':labels,
        'labels2':labels2
    }
    dataJSON = json.dumps(data_dictionary)
    if request.method == "POST":
        print("request is post")
        form = DeleteNodeForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            print(form.cleaned_data['name'])
            Vertex.objects.filter(name=form.instance.name).first().delete()
            return redirect('delete_node')
        else:
            print("form not valid")
    else:
        
        form = DeleteNodeForm()
        
    return render(request, 'graph/post_deletenode.html', {'form': form,'data':dataJSON})

@login_required
def add_edges(request):
    vertices=Vertex.objects.all()
    v=[]
    labels=[]
    for vertex in vertices:
        v1=[]
        v1.append(vertex.x_val)
        v1.append(vertex.y_val)
        v.append(v1)
        labels.append(str(vertex.code))
    #labels.sort()
    print(v)
    print(labels)
    edges=Edge.objects.all()
    ed=[]
    for edge in edges:
        e=[]
        e.append(labels.index(str(edge.v_one)))
        e.append(labels.index(str(edge.v_two)))
        #e.append(ord(str(edge.v_one))-65)
        #e.append(ord(str(edge.v_two))-65)
        ed.append(e)
    print(ed)
    labels2=[]
    for i in range(len(labels)):
        labels2.append(str(Vertex.objects.filter(code=labels[i]).first().name))
    print("labels2")
    print(labels2)
    data_dictionary = {
        'V': v,
        'E':ed,
        'labels':labels,
        'labels2':labels2
    }
    dataJSON = json.dumps(data_dictionary)
    if request.method == "POST":
        form = AddEdgeForm(request.POST)
        if form.is_valid():
            #print(form.cleaned_data['VertexOne'])
            v_one = Vertex.objects.filter(name=form.cleaned_data['VertexOne']).first()
            v_two = Vertex.objects.filter(name=form.cleaned_data['VertexTwo']).first()
            diff = form.cleaned_data['diff']
            Edge(v_one=v_one, v_two=v_two, diff=diff).save()
            return redirect('add_edge')
    else:
        form = AddEdgeForm()
    return render(request, 'graph/post_addedge.html', {'form': form,'data':dataJSON})


@login_required
def delete_edges(request):
    vertices=Vertex.objects.all()
    v=[]
    labels=[]
    for vertex in vertices:
        v1=[]
        v1.append(vertex.x_val)
        v1.append(vertex.y_val)
        v.append(v1)
        labels.append(str(vertex.code))
    #labels.sort()
    print(v)
    print(labels)
    edges=Edge.objects.all()
    ed=[]
    for edge in edges:
        e=[]
        e.append(labels.index(str(edge.v_one)))
        e.append(labels.index(str(edge.v_two)))
        #e.append(ord(str(edge.v_one))-65)
        #e.append(ord(str(edge.v_two))-65)
        ed.append(e)
    print(ed)
    labels2=[]
    for i in range(len(labels)):
        labels2.append(str(Vertex.objects.filter(code=labels[i]).first().name))
    print("labels2")
    print(labels2)
    data_dictionary = {
        'V': v,
        'E':ed,
        'labels':labels,
        'labels2':labels2
    }
    dataJSON = json.dumps(data_dictionary)
    if request.method == "POST":
        form = DeleteEdgeForm(request.POST)
        if form.is_valid():
            v_one = vtwo = Vertex.objects.filter(name=form.cleaned_data['VertexOne']).first()
            v_two = vone = Vertex.objects.filter(name=form.cleaned_data['VertexTwo']).first()
            if Edge.objects.filter(v_one=v_one, v_two=v_two):
                Edge.objects.filter(v_one=v_one, v_two=v_two).first().delete()
            else:
                Edge.objects.filter(v_one=vone, v_two=vtwo).first().delete()
            return redirect('delete_edge')
    else:
        form = DeleteEdgeForm()
    return render(request, 'graph/post_deleteedge.html', {'form': form,'data':dataJSON})


@login_required
def edit_graph(request):
    vertices=Vertex.objects.all()
    v=[]
    labels=[]
    for vertex in vertices:
        v1=[]
        v1.append(vertex.x_val)
        v1.append(vertex.y_val)
        v.append(v1)
        labels.append(str(vertex.code))
    #labels.sort()
    print(v)
    print(labels)
    edges=Edge.objects.all()
    ed=[]
    for edge in edges:
        e=[]
        e.append(labels.index(str(edge.v_one)))
        e.append(labels.index(str(edge.v_two)))
        #e.append(ord(str(edge.v_one))-65)
        #e.append(ord(str(edge.v_two))-65)
        ed.append(e)
    print(ed)
    labels2=[]
    for i in range(len(labels)):
        labels2.append(str(Vertex.objects.filter(code=labels[i]).first().name))
    print("labels2")
    print(labels2)
    data_dictionary = {
        'V': v,
        'E':ed,
        'labels':labels,
        'labels2':labels2
    }
    dataJSON = json.dumps(data_dictionary)
    return render(request, 'graph/edit_graph.html',{'data':dataJSON})