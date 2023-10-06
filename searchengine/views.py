from django.shortcuts import render
from django.views import generic
from searchindex.query import run_query
from searchengine.models import Document
from searchengine.summarise import summarise
from searchindex.query_completion import complete_query
from django.http import JsonResponse
from searchindex.spellcheck import correct_spelling
from django.utils import timezone
import re

# Create your views here.

class Index(generic.TemplateView):
    template_name = "search.html"

class Search(generic.ListView):
    template_name = "search.html"
    context_object_name = "searchresults"
    paginate_by = 30
    num_results = 0

    def get_queryset(self):
        query = self.request.GET['query']
        results = run_query(query)[:200]
        self.num_results = len(results)
        
        docs = [Document.objects.get(doc_id=doc_id) for doc_id in results]
        formatted_docs = []
        for doc in docs:
            formatted_docs.append(format_doc(doc))
        
        return formatted_docs or ["No Results"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_results'] = self.num_results
        context['spelling_correction'] = correct_spelling(self.request.GET['query'])
        return context

def format_doc(doc):
    result = f'<h5><a href="https://ai.stackexchange.com/questions/{doc.doc_id}" class="title">{doc.title}</a></h5>'
    text = re.sub("<[^>]*>", "", doc.text)[:600] + " ..."
    result += f"<p class='body'>{text}</p>"
    
    return result

def complete(request):
    query = request.GET['q']
    completions = complete_query(query)
    return JsonResponse(completions, safe=False)