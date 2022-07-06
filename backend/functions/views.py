import json
from rest_framework.views import APIView
from rest_framework.response import Response
from .functions import *
import pandas as pd
import os
from django.conf import settings
from django.http import FileResponse, HttpResponse


# All views are simple request/response constructs, taking 
# parameters from the frontend, calculating something and returning it


class UploadView(APIView):
    def post(self, request, *args, **kwargs):
        response, success = try_upload(self.request.data['upload'])
        return Response(status=200, data={"success": success, "response": response})

class InfoView(APIView):
    def post(self, request, *args, **kwargs):
        data = handle_upload(self.request.data['upload'])
        if data is False:
            return Response(status=204)
        headers = column_headers(data)
        ids = get_fish_ids(data)
        behaviors = data.behavior.unique()
        return_data = {
                "headers": headers,
                "ids": ids,
                "behaviors": behaviors,
                "categories": data.behavioral_category.unique(),
                }

        return Response(status=200, data=return_data)

class InteractionView(APIView):
    def post(self, request, *args, **kwargs):
        data = handle_upload(self.request.data['upload'])
        if data is False:
            return Response(status=204)
        min_edge_count = json.loads(self.request.data['min_edge_count'])
        return_data = {"graph": interaction_network(data, min_edge_count)}
        return Response(status=200, data=return_data)

class BehaviorPlotView(APIView):
    def post(self, request, *args, **kwargs):
        data = handle_upload(self.request.data['upload'])
        if data is False:
            return Response(status=204)
        behavior = self.request.data['behavior']
        return_data = {"plot": dataplot(data, behavior)}
        return Response(status=200, data=return_data)

class TransitionView(APIView):
    def post(self, request, *args, **kwargs):
        data = handle_upload(self.request.data['upload'])
        if data is False:
            return Response(status = 204)
        option = self.request.data['option']
        if (option == 'false'):
            option = 'behavior'
        else: 
            option = 'behavioral_category'
        min_edge_count = json.loads(self.request.data['min_edge_count'])
        with_status = json.loads(self.request.data['with_status'])
        normalized = json.loads(self.request.data['normalized'])
        colored = json.loads(self.request.data['colored'])
        colored_edge_thickness = json.loads(self.request.data['colored_edge_thickness'])
        color_hue = json.loads(self.request.data['color_hue'])
        node_color_map = self.request.data['node_color_map']
        node_size_map = self.request.data['node_size_map']
        node_label_map = self.request.data['node_label_map']
        return_data = {
                "graph": transition_network(
                    data,
                    option,
                    min_edge_count,
                    with_status,
                    normalized,
                    colored,
                    colored_edge_thickness,
                    color_hue,
                    node_color_map,
                    node_size_map,
                    node_label_map
                    )
                }
        return Response(status=200, data=return_data)
