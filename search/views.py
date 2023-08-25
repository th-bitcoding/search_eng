import nltk
from .models import *
import concurrent.futures
from .serializers import *
from functools import reduce
from collections import deque
from django.db.models import Q
from django.db.models import F
from collections import Counter
from collections import defaultdict
from rest_framework import viewsets
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class SearchengineAPIView(APIView):
    pagination_class = StandardResultsSetPagination

    def get(self, request):

        my_deque = deque()

        def append_json_to_list(json_data):
            my_deque.append(json_data.sub_objects)

        result_list = []

        search_value = request.query_params.get("search_data")
        print("search_value===============", search_value)
        keyword_list = search_value.split()
        print("keyword_list===============", keyword_list)

        # search_queries = [Q(sub_objects__lower__trigram_similar=term) for term in keyword_list]
        vector = SearchVector("sub_objects")
        print("vector===========================", vector)
        query_for_full_kw = SearchQuery(search_value)
        result_for_full_keyword = SubObjectJSON.objects.annotate(
            rank=SearchRank(vector, query_for_full_kw)
        ).order_by("-rank")
        print(
            "result_for_full_keyword===========================",
            result_for_full_keyword,
        )

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor1:
            # Submit each JSON data to the executor
            future_to_data = {
                executor1.submit(append_json_to_list, json_data): json_data.sub_objects
                for json_data in result_for_full_keyword
            }
            print("future_to_data===========================", future_to_data)

        # Wait for all futures to complete
        concurrent.futures.wait(future_to_data.keys())
        for kw in keyword_list:
            query = SearchQuery(kw)
            result_for_sep_words = SubObjectJSON.objects.annotate(
                rank=SearchRank(vector, query)
            ).order_by("-rank")
            print("result_for_sep_words==================", result_for_sep_words)

            for i in result_for_full_keyword:
                pass
                # index = defaultdict(list)
                # for doc_id, doc in enumerate(i.sub_objects):
                #     print("doc_id, doc=============================", doc_id, doc)
                #     tokens = nltk.word_tokenize(doc['content'])
                #     doc_ids = set(index.get(token.lower(), []) for token in tokens)
                #     doc_ids = [doc_id for doc_id_list in doc_ids for doc_id in doc_id_list]
                #     doc_counts = Counter(doc_ids)
                #     results = [i.sub_objects for doc_id, count in doc_counts.most_common()]
                #     print("results=================", results)

            # for data in result_for_sep_words:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor2:
                # Submit each JSON data to the executor2
                future_to_data = {
                    executor2.submit(
                        append_json_to_list, json_data
                    ): json_data.sub_objects
                    for json_data in result_for_sep_words
                }
            # Wait for all futures to complete
            concurrent.futures.wait(future_to_data.keys())

        # result = SubObjectJSON.objects.filter(reduce(lambda x, y: x | y, search_queries)).values()

        # Paginate the results
        paginator = self.pagination_class()
        paginated_result_list = paginator.paginate_queryset(result_list, request)
        # return paginator.get_paginated_response(paginated_result_list)

        return Response(list(my_deque))

    
class DiffereSol(APIView):
    def get(self, request):
        pass
        # search_value = self.request.GET.get("search", None)
        # if search_value:
        #     sub_objects = SubObjectJSON.objects.all()
        #     for obj in sub_objects:
        #         try:
        #             obj_dict = json.loads(obj.sub_objects)
        #             if search_value.lower() in obj_dict['name'].lower():
        #                 results.append(obj_dict)
        #         except:
        #             pass
        
        # return Response(results)
    
# class MyModelSearchView(generics.ListAPIView):
#     serializer_class = SubObjectJSONSerializer

#     def get_queryset(self):
#         keywords = str(self.request.query_params.get('search', '')).split()
#         print(keywords)
#         q_objects = Q()
#         for keyword in keywords:
#             q_objects |= Q(sub_objects__icontains=keyword)
#         return SubObjectJSON.objects.filter(q_objects)
    
# class MyModelSearchView(generics.ListAPIView):
#     serializer_class = SubObjectJSONSerializer

#     def get_queryset(self):
#         keywords = self.request.query_params.get('search', '').split()
#         suffixes = ['s', 'es', 'ed', 'ing']
#         q_objects = Q()
#         for keyword in keywords:
#             q_objects |= Q(sub_objects__icontains=keyword)
#             for suffix in suffixes:
#                 q_objects |= Q(sub_objects__icontains=keyword + suffix)
#                 q_objects |= Q(sub_objects__icontains=keyword[:-1] + suffix)
#         return SubObjectJSON.objects.filter(q_objects)
    
# class MyModelSearchView(generics.ListAPIView):
#     serializer_class = SubObjectJSONSerializer

#     def get_queryset(self):
#         keywords = self.request.query_params.get('search', '').split()
#         suffixes = ['s', 'es', 'ed', 'ing']
#         q_objects = Q()
#         for keyword in keywords:
#             keyword_q_objects = Q()
#             for suffix in suffixes:
#                 keyword_q_objects |= Q(sub_objects__icontains=keyword + suffix)
#                 keyword_q_objects |= Q(sub_objects__icontains=keyword[:-1] + suffix)
#             q_objects |= keyword_q_objects
#         return SubObjectJSON.objects.filter(q_objects)
    
# class SearchengineViewSet(viewsets.ModelViewSet):
#     serializer_class = SubObjectJSONSerializer

#     def search(self, query):
#         return SubObjectJSON.objects.filter(
#             Q(sub_objects__icontains=query)
#         )

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         query = self.request.query_params.get('search', None)
#         if query:
#             queryset = self.search(query)
#         return queryset