import requests
import time

class APIRequest:
    def __init__(self, base_url: str, auth_url: str, username: str, password: str):
        self.base_url = base_url
        self.auth_url = auth_url
        self.username = username
        self.password = password
        self.token = None
        self.token_time = 0  # Timestamp da última obtenção do token
        self.token_expiration = 1800  # Tempo de expiração do token (30 min padrão)

    def _get_token(self):
        response = requests.post(
            self.auth_url,
            data={"username": self.username, "password": self.password}
        )

        if response.status_code == 200:
            data = response.json()
            self.token = data.get("access_token")
            self.token_time = time.time()  # Atualiza o tempo da última obtenção do token
        else:
            raise Exception(f"Erro ao obter token: {response.text}")

    def _ensure_token_valid(self):
        if not self.token or (time.time() - self.token_time) > self.token_expiration:
            self._get_token()

    def get(self, endpoint: str, params=None):
        self._ensure_token_valid()
        headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.get(f"{self.base_url}{endpoint}", headers=headers, params=params)

        return response.json()

    def post(self, endpoint: str, data: dict):
        self._ensure_token_valid()
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

        response = requests.post(f"{self.base_url}{endpoint}", json=data, headers=headers)

        return response.json()
