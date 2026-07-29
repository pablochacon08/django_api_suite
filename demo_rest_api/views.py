from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False})  # Ejemplo de item inactivo

class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request, format=None):
        active_items = [item for item in data_list if item.get('is_active', False)]
        return Response(active_items, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        data = request.data.copy()

        if 'name' not in data or 'email' not in data:
            return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

        data['id'] = str(uuid.uuid4())
        data['is_active'] = True
        data_list.append(data)

        return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)


class DemoRestApiItem(APIView):
    name = "Demo REST API Item"

    def get_item(self, item_id):
        return next((item for item in data_list if item.get('id') == item_id), None)

    def put(self, request, item_id, format=None):
        data = request.data.copy()

        if 'id' not in data:
            return Response({'error': 'El campo "id" es obligatorio para PUT.'}, status=status.HTTP_400_BAD_REQUEST)

        if str(data['id']) != str(item_id):
            return Response({'error': 'El id del cuerpo no coincide con el id de la ruta.'}, status=status.HTTP_400_BAD_REQUEST)

        item = self.get_item(item_id)
        if item is None:
            return Response({'error': 'Recurso no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if 'name' not in data or 'email' not in data:
            return Response({'error': 'Faltan campos requeridos para reemplazar el recurso.'}, status=status.HTTP_400_BAD_REQUEST)

        new_item = {
            'id': item_id,
            'name': data['name'],
            'email': data['email'],
            'is_active': data.get('is_active', True)
        }
        data_list[data_list.index(item)] = new_item

        return Response({'message': 'Recurso reemplazado correctamente.', 'data': new_item}, status=status.HTTP_200_OK)

    def patch(self, request, item_id, format=None):
        item = self.get_item(item_id)
        if item is None:
            return Response({'error': 'Recurso no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        if 'id' in data and str(data['id']) != str(item_id):
            return Response({'error': 'El id del cuerpo no puede modificarse.'}, status=status.HTTP_400_BAD_REQUEST)

        for key, value in data.items():
            if key != 'id':
                item[key] = value

        return Response({'message': 'Recurso actualizado parcialmente.', 'data': item}, status=status.HTTP_200_OK)

    def delete(self, request, item_id, format=None):
        item = self.get_item(item_id)
        if item is None:
            return Response({'error': 'Recurso no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        item['is_active'] = False
        return Response({'message': 'Recurso eliminado lógicamente.', 'data': item}, status=status.HTTP_200_OK)
