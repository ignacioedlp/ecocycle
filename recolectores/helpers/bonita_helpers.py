import requests
from decimal import Decimal

# Base URL y credenciales
base_url = "http://192.168.0.224:8080/bonita" #Si usan docker quizas en vez de localhost usen la ip de la maquina
username = "walter.bates"
password = "bpm"

# Funciones auxiliares
def authenticate():
    url = "/loginservice"

    payload = f'username={username}&password={password}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(base_url + url, data=payload, headers=headers)

    if response.status_code == 204:
        bonita_token = response.cookies.get('X-Bonita-API-Token')
        session_id = response.cookies.get('JSESSIONID')
        if bonita_token:
            print("Autenticación exitosa.")
            return bonita_token, session_id
        else:
            print("No se encontró el token X-Bonita-API-Token en la respuesta.")
            raise KeyError("No se encontró el token X-Bonita-API-Token en la respuesta.")
    else:
        print(f"Error de autenticación: {response.status_code}, {response.text}")
        raise Exception(f"Error de autenticación: {response.status_code}, {response.text}")

def getProcessId(token, session_id, processName):
    url = "/API/bpm/process?s=" + processName
    headers = {
        'X-Bonita-API-Token': token,
        'Cookie': f'JSESSIONID={session_id}; X-Bonita-API-Token={token}'
    }
    
    response = requests.request("GET", base_url + url, headers=headers)
    
    if response.content:
        return response.json()[0]['id'] if response.json() else None
    else:
        raise ValueError("Empty response received from the server")

def initProcess(token, session_id, processId):
    url = "/API/bpm/process/" + processId + "/instantiation"
    headers = {
        'X-Bonita-API-Token': token,
        'Cookie': f'JSESSIONID={session_id}; X-Bonita-API-Token={token}'
    }
    response = requests.request("POST", base_url + url, headers=headers)
    return response.json()['caseId'] if response.json() else None

def getTaskByCase(token, session_id, caseId):
    url = f"/API/bpm/task?f=caseId={caseId}"
    headers = {
        'X-Bonita-API-Token': token,
        'Cookie': f'JSESSIONID={session_id}; X-Bonita-API-Token={token}'
    }

    response = requests.get(base_url + url, headers=headers)

    if response.status_code == 200:
        try:
            json_data = response.json()
            if isinstance(json_data, list) and len(json_data) > 0:
                return json_data[0]['id']
            else:
                raise ValueError("La respuesta no contiene tareas asociadas al caseId.")
        except (ValueError, KeyError) as e:
            raise ValueError(f"Error al procesar la respuesta JSON: {e}")
    else:
        raise Exception(f"Error al obtener la tarea por caseId: {response.status_code}, {response.text}")

def assignVariableByTaskAndCase(token, session_id, caseId, variableName, variableValue, variableType):
    url = f"/API/bpm/caseVariable/{caseId}/{variableName}"
    headers = {
        'X-Bonita-API-Token': token,
        'Cookie': f'JSESSIONID={session_id}; X-Bonita-API-Token={token}',
        'Content-Type': 'application/json'
    }

    if isinstance(variableValue, Decimal):
        variableValue = str(variableValue)

    payload = {
        "type": variableType,
        "value": variableValue
    }

    response = requests.put(base_url + url, headers=headers, json=payload)

    if response.status_code == 200 or response.status_code == 204:
        print(f"Variable {variableName} asignada correctamente.")
    else:
        print(f"Error al asignar la variable {variableName}: {response.status_code}, {response.text}")

    if response.content:
        return response.json()
    else:
        return None

def getUserIdByUsername(token, session_id):
    url = f"/API/identity/user?s={username}"
    headers = {
        'X-Bonita-API-Token': token,
        'Cookie': f'JSESSIONID={session_id}; X-Bonita-API-Token={token}'
    }

    response = requests.get(base_url + url, headers=headers)

    if response.status_code == 200:
        try:
            json_data = response.json()
            if isinstance(json_data, list) and len(json_data) > 0:
                return json_data[0]['id']
            else:
                raise ValueError("La respuesta no contiene tareas asociadas al caseId.")
        except (ValueError, KeyError) as e:
            raise ValueError(f"Error al procesar la respuesta JSON: {e}")
    else:
        raise Exception(f"Error al obtener la tarea por caseId: {response.status_code}, {response.text}")

def assignUserToTask(token, session_id, taskId, userId):
    url = "/API/bpm/userTask/" + str(taskId)
    headers = {
        'X-Bonita-API-Token': token,
        'Cookie': f'JSESSIONID={session_id}; X-Bonita-API-Token={token}',
        'Content-Type': 'application/json'
    }
    payload = {"assigned_id": userId}

    response = requests.put(base_url + url, headers=headers, json=payload)

    if response.status_code == 200 or response.status_code == 204:
        if response.content:
            return response.json()
        else:
            return None
    else:
        print(f"Error en la solicitud: {response.status_code}, {response.text}")
        raise Exception(f"Error al asignar usuario a la tarea: {response.status_code}, {response.text}")

def completeTask(token, session_id, taskId):
    url = f"/API/bpm/userTask/{taskId}/execution"
    headers = {
        'X-Bonita-API-Token': token,
        'Cookie': f'JSESSIONID={session_id}; X-Bonita-API-Token={token}'
    }
    response = requests.request("POST", base_url + url, headers=headers)

    if response.status_code == 200 or response.status_code == 204:
        if response.content:
            return response.json()
        else:
            return None
    else:
        print(f"Error en la solicitud: {response.status_code}, {response.text}")
        raise Exception(f"Error al completar la tarea: {response.status_code}, {response.text}")