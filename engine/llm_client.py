import os
import json
import urllib.request
import urllib.error

class GeminiLLMClient:
    """
    Client kết nối mô hình ngôn ngữ lớn Google Gemini (Gemini 3.8 Flash)
    với cơ chế Hybrid Fallback đảm bảo 100% độ sẵn sàng cho Hệ thống An Tín.
    """
    def __init__(self, api_key=None, model="models/gemini-3.8-flash", timeout=12):
        if not api_key:
            # Try to load from environment or .env file
            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key and os.path.exists(".env"):
                with open(".env", "r", encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("GEMINI_API_KEY="):
                            api_key = line.strip().split("=", 1)[1]
                            break
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.is_configured = bool(self.api_key and not self.api_key.startswith("YOUR_"))

    def call_gemini(self, system_instruction, user_prompt):
        """Gọi API Gemini 3.8 Flash sinh phản hồi thông minh."""
        if not self.is_configured:
            return None

        url = f"https://generativelanguage.googleapis.com/v1beta/{self.model}:generateContent?key={self.api_key}"
        
        full_prompt = f"HƯỚNG DẪN HỆ THỐNG:\n{system_instruction}\n\nYÊU CẦU NGƯỜI DÙNG:\n{user_prompt}"
        payload = {
            "contents": [
                {
                    "parts": [{"text": full_prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 1024
            }
        }

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                candidates = data.get("candidates", [])
                if candidates and "content" in candidates[0]:
                    text = candidates[0]["content"]["parts"][0]["text"]
                    return text
        except Exception as e:
            # Silently fallback to deterministic expert engine if network/timeout occurs
            return None

        return None

