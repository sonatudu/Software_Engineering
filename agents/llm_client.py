"""
Unified LLM Client Interface supporting 100% Free AI Providers:
1. Google Gemini (Free Tier: gemini-2.0-flash, gemini-1.5-flash)
2. Groq Cloud (Free Tier: Llama 3.3 70B, DeepSeek-R1 Distill, Llama 3.1 8B)
3. Local Ollama (100% Free & Offline: Llama 3.2, DeepSeek-R1, Mistral, Qwen)
"""
import os
import json
import re
import requests
from typing import Optional, Dict, Any, List, Tuple

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


GEMINI_MODELS = [
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash-lite",
    "gemini-3.8-flash",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
]

GROQ_MODELS = [
    "llama-3.3-70b-versatile",
    "deepseek-r1-distill-llama-70b",
    "llama-3.1-8b-instant",
    "gemma2-9b-it",
]

DEFAULT_OLLAMA_MODELS = [
    "llama3.2:latest",
    "llama3.1:8b",
    "deepseek-r1:1.5b",
    "mistral:latest",
    "qwen2.5:latest",
]


def clean_json_string(raw: str) -> Optional[Any]:
    """Robustly strips markdown fences and parses JSON object or array."""
    if not raw or not isinstance(raw, str):
        return None
    cleaned = raw.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except Exception:
        # Regex search for JSON object or array
        match = re.search(r'(\{.*\}|\[.*\])', cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except Exception:
                pass
    return None


_VALIDATED_CACHE = {}


class LLMClient:
    def __init__(
        self,
        provider: str = "gemini",
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        self.provider = provider.lower().strip()
        self.last_error = ""
        self._validated = False
        self.base_url = (base_url or "").strip()

        if self.provider == "gemini":
            raw_key = api_key if api_key is not None else os.environ.get("GEMINI_API_KEY", "")
            self.api_key = raw_key.strip() if raw_key else ""
            self.active_model = model or GEMINI_MODELS[0]
            self.client = None
            if GENAI_AVAILABLE and self.api_key:
                try:
                    self.client = genai.Client(api_key=self.api_key, http_options={"timeout": 15000})
                except Exception as e:
                    self.last_error = str(e)
                    self.client = None

            # Fast cache lookup to avoid repeating network validation
            cache_k = (self.provider, self.api_key)
            if cache_k in _VALIDATED_CACHE:
                self.active_model = _VALIDATED_CACHE[cache_k]
                self._validated = True

        elif self.provider == "groq":
            raw_key = api_key if api_key is not None else os.environ.get("GROQ_API_KEY", "")
            self.api_key = raw_key.strip() if raw_key else ""
            self.active_model = model or GROQ_MODELS[0]
            self.base_url = "https://api.groq.com/openai/v1"
            self.client = None
            cache_k = (self.provider, self.api_key)
            if cache_k in _VALIDATED_CACHE:
                self.active_model = _VALIDATED_CACHE[cache_k]
                self._validated = True

        elif self.provider == "ollama":
            self.api_key = ""  # Ollama requires no key
            self.active_model = model or DEFAULT_OLLAMA_MODELS[0]
            self.base_url = (base_url or os.environ.get("OLLAMA_HOST", "http://localhost:11434")).rstrip("/")
            self.client = None

        else:
            self.api_key = ""
            self.active_model = "unknown"
            self.last_error = f"Unsupported provider: {provider}"

    # ---------------- STATUS & DISCOVERY ----------------

    @staticmethod
    def check_ollama_status(host: str = "http://localhost:11434") -> Tuple[bool, List[str]]:
        """Checks if local Ollama daemon is reachable and lists installed models."""
        try:
            r = requests.get(f"{host.rstrip('/')}/api/tags", timeout=1.5)
            if r.status_code == 200:
                data = r.json()
                models = [m["name"] for m in data.get("models", []) if "name" in m]
                return True, models
        except Exception:
            pass
        return False, []

    @staticmethod
    def get_supported_models(provider: str) -> List[str]:
        p = provider.lower().strip()
        if p == "gemini":
            return list(GEMINI_MODELS)
        elif p == "groq":
            return list(GROQ_MODELS)
        elif p == "ollama":
            online, models = LLMClient.check_ollama_status()
            if online and models:
                return models
            return list(DEFAULT_OLLAMA_MODELS)
        return []

    def validate_connection(self) -> bool:
        """Validates connection with the configured provider with automatic model discovery and fallback."""
        self.last_error = ""

        if self.provider == "gemini":
            if not self.client or not self.api_key:
                return False

            candidate_models = []
            if self.active_model:
                candidate_models.append(self.active_model)

            # Discover models authorized for this key
            try:
                discovered = []
                for m in self.client.models.list():
                    m_name = getattr(m, "name", "").replace("models/", "")
                    if "gemini" in m_name and "image" not in m_name and "embedding" not in m_name:
                        discovered.append(m_name)
                # Prioritize lite and flash models
                lite = [m for m in discovered if "flash-lite" in m]
                flash = [m for m in discovered if "flash" in m and "flash-lite" not in m]
                others = [m for m in discovered if "flash" not in m]
                for m in (lite + flash + others + list(GEMINI_MODELS)):
                    if m not in candidate_models:
                        candidate_models.append(m)
            except Exception:
                for m in GEMINI_MODELS:
                    if m not in candidate_models:
                        candidate_models.append(m)

            # Test candidates in order until a working one is found
            for model_name in candidate_models:
                try:
                    res = self.client.models.generate_content(
                        model=model_name,
                        contents="Say OK"
                    )
                    if res and res.text:
                        self.active_model = model_name
                        self._validated = True
                        self.last_error = ""
                        _VALIDATED_CACHE[(self.provider, self.api_key)] = model_name
                        return True
                except Exception as e:
                    self.last_error = str(e)
                    continue

            self._validated = False
            return False

        elif self.provider == "groq":
            if not self.api_key:
                return False
            try:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                body = {
                    "model": self.active_model,
                    "messages": [{"role": "user", "content": "Say OK"}],
                    "max_tokens": 10,
                    "temperature": 0.1
                }
                r = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=body, timeout=12)
                if r.status_code == 200:
                    self._validated = True
                    return True
                else:
                    try:
                        err_json = r.json()
                        self.last_error = err_json.get("error", {}).get("message", r.text)
                    except Exception:
                        self.last_error = f"HTTP {r.status_code}: {r.text[:100]}"
            except Exception as e:
                self.last_error = str(e)
            self._validated = False
            return False

        elif self.provider == "ollama":
            online, models = self.check_ollama_status(self.base_url)
            if not online:
                self.last_error = f"Local Ollama is offline at {self.base_url}"
                self._validated = False
                return False
            if models and self.active_model not in models:
                # Use the first available model if current isn't downloaded
                self.active_model = models[0]
            self._validated = True
            return True

        return False

    def is_active(self) -> bool:
        if self._validated:
            return True
        if self.provider == "gemini":
            if not self.client or not self.api_key:
                return False
        elif self.provider == "groq":
            if not self.api_key:
                return False
        elif self.provider == "ollama":
            pass  # checks via validate_connection
        else:
            return False

        return self.validate_connection()

    # ---------------- TEXT GENERATION ----------------

    def generate_text(self, prompt: str, system_instruction: str = "") -> Optional[str]:
        if not self.is_active():
            return None

        # 1. Google Gemini
        if self.provider == "gemini":
            try:
                config = types.GenerateContentConfig(
                    system_instruction=system_instruction if system_instruction else None,
                    temperature=0.3,
                )
                response = self.client.models.generate_content(
                    model=self.active_model,
                    contents=prompt,
                    config=config
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                self.last_error = str(e)
                print(f"[Gemini Error] {self.active_model}: {e}")
            return None

        # 2. Groq Cloud
        elif self.provider == "groq":
            try:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                messages = []
                if system_instruction:
                    messages.append({"role": "system", "content": system_instruction})
                messages.append({"role": "user", "content": prompt})

                payload = {
                    "model": self.active_model,
                    "messages": messages,
                    "temperature": 0.3,
                }
                r = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=25)
                if r.status_code == 200:
                    data = r.json()
                    choices = data.get("choices", [])
                    if choices:
                        return choices[0].get("message", {}).get("content", "")
                else:
                    self.last_error = f"Groq HTTP {r.status_code}: {r.text[:120]}"
            except Exception as e:
                self.last_error = str(e)
                print(f"[Groq Error] {self.active_model}: {e}")
            return None

        # 3. Local Ollama
        elif self.provider == "ollama":
            try:
                messages = []
                if system_instruction:
                    messages.append({"role": "system", "content": system_instruction})
                messages.append({"role": "user", "content": prompt})

                payload = {
                    "model": self.active_model,
                    "messages": messages,
                    "temperature": 0.3,
                }
                r = requests.post(f"{self.base_url}/v1/chat/completions", json=payload, timeout=45)
                if r.status_code == 200:
                    data = r.json()
                    choices = data.get("choices", [])
                    if choices:
                        return choices[0].get("message", {}).get("content", "")
                else:
                    # Fallback to Ollama native /api/generate
                    payload_native = {
                        "model": self.active_model,
                        "prompt": prompt,
                        "system": system_instruction,
                        "stream": False
                    }
                    r2 = requests.post(f"{self.base_url}/api/generate", json=payload_native, timeout=45)
                    if r2.status_code == 200:
                        return r2.json().get("response", "")
            except Exception as e:
                self.last_error = str(e)
                print(f"[Ollama Error] {self.active_model}: {e}")
            return None

        return None

    # ---------------- JSON GENERATION ----------------

    def generate_json(self, prompt: str, system_instruction: str = "") -> Optional[Any]:
        if not self.is_active():
            return None

        # 1. Google Gemini
        if self.provider == "gemini":
            for use_mime in [True, False]:
                try:
                    config_args = {"temperature": 0.1}
                    if system_instruction:
                        config_args["system_instruction"] = system_instruction
                    if use_mime:
                        config_args["response_mime_type"] = "application/json"

                    config = types.GenerateContentConfig(**config_args)
                    response = self.client.models.generate_content(
                        model=self.active_model,
                        contents=prompt,
                        config=config
                    )
                    if response and response.text:
                        parsed = clean_json_string(response.text)
                        if parsed is not None:
                            return parsed
                except Exception as e:
                    self.last_error = str(e)
                    continue
            return None

        # 2. Groq Cloud
        elif self.provider == "groq":
            try:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                messages = []
                system_with_json = (system_instruction + "\nReturn ONLY raw valid JSON without markdown wrapping.").strip()
                messages.append({"role": "system", "content": system_with_json})
                messages.append({"role": "user", "content": prompt})

                payload = {
                    "model": self.active_model,
                    "messages": messages,
                    "temperature": 0.1,
                    "response_format": {"type": "json_object"}
                }
                r = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=25)
                if r.status_code == 200:
                    data = r.json()
                    choices = data.get("choices", [])
                    if choices:
                        content = choices[0].get("message", {}).get("content", "")
                        parsed = clean_json_string(content)
                        if parsed is not None:
                            return parsed
                else:
                    # Retry without response_format if model doesn't support json_object
                    payload.pop("response_format", None)
                    r2 = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=25)
                    if r2.status_code == 200:
                        content = r2.json().get("choices", [{}])[0].get("message", {}).get("content", "")
                        return clean_json_string(content)
            except Exception as e:
                self.last_error = str(e)
                print(f"[Groq JSON Error] {self.active_model}: {e}")
            return None

        # 3. Local Ollama
        elif self.provider == "ollama":
            try:
                system_with_json = (system_instruction + "\nReturn ONLY valid JSON.").strip()
                messages = [
                    {"role": "system", "content": system_with_json},
                    {"role": "user", "content": prompt}
                ]
                payload = {
                    "model": self.active_model,
                    "messages": messages,
                    "temperature": 0.1,
                    "format": "json"
                }
                r = requests.post(f"{self.base_url}/v1/chat/completions", json=payload, timeout=45)
                if r.status_code == 200:
                    content = r.json().get("choices", [{}])[0].get("message", {}).get("content", "")
                    parsed = clean_json_string(content)
                    if parsed is not None:
                        return parsed
                else:
                    # Native /api/generate with format='json'
                    native_payload = {
                        "model": self.active_model,
                        "prompt": prompt,
                        "system": system_with_json,
                        "stream": False,
                        "format": "json"
                    }
                    r2 = requests.post(f"{self.base_url}/api/generate", json=native_payload, timeout=45)
                    if r2.status_code == 200:
                        return clean_json_string(r2.json().get("response", ""))
            except Exception as e:
                self.last_error = str(e)
                print(f"[Ollama JSON Error] {self.active_model}: {e}")
            return None

        return None
