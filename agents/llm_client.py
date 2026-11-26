"""
LLM Client Interface using Google GenAI SDK with dynamic model discovery and key validation.
"""
import os
import json
from typing import Optional, Dict, Any, List

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

PREFERRED_MODELS = [
    "gemini-3.8-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash"
]


class LLMClient:
    def __init__(self, api_key: Optional[str] = None):
        raw_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        self.api_key = raw_key.strip() if raw_key else ""
        self.client = None
        self.last_error = ""
        self.active_model = PREFERRED_MODELS[0]
        self._validated = False
        
        if GENAI_AVAILABLE and self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                self.last_error = str(e)
                self.client = None

    def validate_connection(self) -> bool:
        """Discovers authorized models from the API key and tests generation."""
        if not self.client or not self.api_key:
            return False
        
        # 1. Try discovering models from the account
        candidate_models = list(PREFERRED_MODELS)
        try:
            discovered = []
            for m in self.client.models.list():
                m_name = getattr(m, "name", "")
                if "gemini" in m_name:
                    clean_name = m_name.replace("models/", "")
                    discovered.append(clean_name)
            if discovered:
                # Prioritize flash models from discovered list
                candidate_models = [m for m in discovered if "flash" in m] + [m for m in discovered if "flash" not in m]
        except Exception as e:
            # If list fails, fall back to preferred list
            self.last_error = str(e)

        # 2. Test generation with candidate models
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
                    return True
            except Exception as e:
                self.last_error = str(e)
                continue

        self._validated = False
        return False

    def is_active(self) -> bool:
        if not self.client or not self.api_key:
            return False
        if not self._validated:
            return self.validate_connection()
        return True

    def generate_text(self, prompt: str, system_instruction: str = "") -> Optional[str]:
        if not self.is_active():
            return None
        
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
            print(f"Error calling {self.active_model}: {e}")

        return None

    def generate_json(self, prompt: str, system_instruction: str = "") -> Optional[Any]:
        if not self.is_active():
            return None
        
        # First try structured JSON output
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
                    raw = response.text.strip()
                    # Strip markdown block if model added it
                    if raw.startswith("```json"):
                        raw = raw[7:]
                    elif raw.startswith("```"):
                        raw = raw[3:]
                    if raw.endswith("```"):
                        raw = raw[:-3]
                    raw = raw.strip()
                    try:
                        return json.loads(raw)
                    except Exception:
                        import re
                        m = re.search(r'(\{.*\})', raw, re.DOTALL)
                        if m:
                            return json.loads(m.group(1))
            except Exception as e:
                self.last_error = str(e)
                print(f"Error calling {self.active_model} for JSON (mime={use_mime}): {e}")
                continue

        return None
