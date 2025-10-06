import os
import tempfile
import subprocess
import logging
import requests
import re
import speech_recognition as sr
import json

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any

# --- Import your new e-commerce tools ---
import ecommerce_tools

# Load environment variables
try:
  from dotenv import load_dotenv
  load_dotenv()
except ImportError:
  pass

logger = logging.getLogger('MultiAgentOrchestrator')
logging.basicConfig(level=logging.INFO)

GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
MURF_API_KEY = os.getenv('MURF_API_KEY', '')
MODEL_NAME = os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant')
MURF_GENERATE_URL = "https://api.murf.ai/v1/speech/generate"

app = FastAPI(title="Agentic E-commerce Orchestrator", version="3.1.0") # Version bump for the fix

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"], # Adjust in production
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

recognizer = sr.Recognizer()

# Groq client init
try:
  from groq import Groq
  groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
except ImportError:
  groq_client = None
  logger.warning("Groq is not installed, LLM features disabled.")

# [ AdvancedEmotionDetector CLASS as defined in your original code ]
class AdvancedEmotionDetector:
    def __init__(self):
        self.emotion_keywords = {
            'joy': ['happy', 'joyful', 'glad', 'pleased', 'cheerful', 'delighted', 'content'],
            'excitement': ['excited', 'thrilled', 'pumped', 'energized', 'hyped', 'enthusiastic', 'amazing', 'fantastic', 'incredible'],
            'love': ['love', 'adore', 'cherish', 'treasure', 'appreciate', 'care about', 'fond of'],
            'gratitude': ['thank you', 'grateful', 'thankful', 'appreciate', 'blessed', 'thanks'],
            'sadness': ['sad', 'unhappy', 'down', 'blue', 'gloomy', 'dejected', 'melancholy'],
            'anger': ['angry', 'mad', 'furious', 'livid', 'outraged', 'irate', 'pissed'],
            'frustration': ['frustrated', 'annoyed', 'irritated', 'aggravated', 'bothered', 'irked'],
            'fear': ['scared', 'afraid', 'frightened', 'terrified', 'petrified'],
            'anxiety': ['anxious', 'worried', 'nervous', 'stressed', 'tense', 'uneasy', 'concerned'],
            'surprise': ['surprised', 'shocked', 'amazed', 'astonished', 'stunned', 'wow'],
            'confusion': ['confused', 'puzzled', 'bewildered', 'perplexed', "don't understand"],
            'calm': ['calm', 'peaceful', 'relaxed', 'serene', 'tranquil', 'at ease'],
            'hopeful': ['hopeful', 'optimistic', 'positive', 'looking forward', 'bright future'],
            'neutral': ['okay', 'fine', 'alright', 'normal', 'usual', 'regular'],
        }
        self.intensifiers = {
            'high': ['very', 'extremely', 'incredibly', 'absolutely', 'totally', 'completely', 'utterly', 'so', 'really'],
            'medium': ['quite', 'fairly', 'somewhat', 'rather', 'pretty', 'kind of'],
            'low': ['a bit', 'a little', 'slightly', 'somewhat']
        }

    def detect_emotion_intensity(self, text):
        text_lower = text.lower()
        if any(intensifier in text_lower for intensifier in self.intensifiers['high']): return 'high'
        if any(word.isupper() for word in text.split() if len(word) > 2): return 'high'
        if text.count('!') >= 2: return 'high'
        if text.count('!') == 1: return 'medium'
        if any(intensifier in text_lower for intensifier in self.intensifiers['medium']): return 'medium'
        if any(intensifier in text_lower for intensifier in self.intensifiers['low']): return 'low'
        return 'medium'

    def llm_emotion_detection(self, text):
        if not groq_client: return None, 0, 'medium'
        try:
            emotion_list = list(self.emotion_keywords.keys())
            emotion_prompt = f"""Analyze the emotional tone of this text: "{text}"
Respond in this exact format:
Primary: [emotion from list: {', '.join(emotion_list)}]
Confidence: [0.1-1.0]"""
            response = groq_client.chat.completions.create(
                messages=[{"role": "user", "content": emotion_prompt}],
                model=MODEL_NAME, temperature=0.3, max_tokens=50
            )
            result = response.choices[0].message.content.strip()
            primary_match = re.search(r'Primary:\s*(\w+)', result)
            confidence_match = re.search(r'Confidence:\s*([\d.]+)', result)
            if primary_match:
                emotion = primary_match.group(1).lower()
                confidence = float(confidence_match.group(1)) if confidence_match else 0.8
                if emotion in emotion_list:
                    return emotion, confidence, self.detect_emotion_intensity(text)
            return None, 0, 'medium'
        except Exception as e:
            logger.error(f"LLM emotion detection failed: {e}")
            return None, 0, 'medium'

    def detect_comprehensive_emotion(self, text):
        llm_emotion, llm_confidence, llm_intensity = self.llm_emotion_detection(text)
        return {
            'emotion': llm_emotion or 'neutral',
            'confidence': llm_confidence,
            'intensity': llm_intensity
        }

# [ VoiceSynthesizer CLASS as defined in your original code ]
class VoiceSynthesizer:
    def __init__(self):
        self.emotion_voice_settings = {
            'joy': {'rate': 1.15, 'pitch': 1.08}, 'excitement': {'rate': 1.25, 'pitch': 1.12},
            'sadness': {'rate': 0.8, 'pitch': 0.92}, 'anger': {'rate': 0.9, 'pitch': 0.98},
            'fear': {'rate': 0.85, 'pitch': 1.05}, 'surprise': {'rate': 1.2, 'pitch': 1.15},
            'calm': {'rate': 0.95, 'pitch': 1.0}, 'neutral': {'rate': 1.0, 'pitch': 1.0}
        }

    def adjust_voice_for_intensity(self, base_settings, intensity):
        settings = base_settings.copy()
        if intensity == 'high':
            settings['rate'] = min(settings['rate'] * 1.1, 1.4)
            settings['pitch'] = min(settings['pitch'] * 1.05, 1.2)
        elif intensity == 'low':
            settings['rate'] = max(settings['rate'] * 0.95, 0.7)
            settings['pitch'] = max(settings['pitch'] * 0.98, 0.85)
        return settings

    def synthesize_speech(self, text, emotion_data):
        if not MURF_API_KEY:
            logger.warning("No Murf API key available; skipping TTS")
            return None
        emotion = emotion_data.get('emotion', 'neutral')
        intensity = emotion_data.get('intensity', 'medium')
        base_settings = self.emotion_voice_settings.get(emotion, self.emotion_voice_settings['neutral'])
        settings = self.adjust_voice_for_intensity(base_settings, intensity)
        
        payload = {
            "voiceId": "en-US-natalie", "style": "conversational", "text": text,
            "rate": settings['rate'], "pitch": settings['pitch'], "format": "WAV", "sampleRate": 44100
        }
        headers = {"api-key": MURF_API_KEY, "Content-Type": "application/json"}
        try:
            response = requests.post(MURF_GENERATE_URL, json=payload, headers=headers, timeout=15)
            response.raise_for_status()
            audio_url = response.json().get('audioFile')
            logger.info(f"Generated TTS audio URL: {audio_url}")
            return audio_url
        except Exception as e:
            logger.error(f"Speech synthesis error: {e}")
        return None

# --- Define and Register Agentic Tools ---
AVAILABLE_TOOLS = {
    "search_products": {
        "function": ecommerce_tools.search_products,
        "description": "Searches for products in the e-commerce catalog based on a query, category, and maximum price.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search term for the product name, e.g., 'running shoes', 'leather wallet'."},
                "category": {"type": "string", "description": "The specific category to filter by, e.g., 'apparel', 'electronics'."},
                "max_price": {"type": "number", "description": "The maximum price for the products."}
            }, "required": ["query"]
        }
    },
    "get_order_status": {
        "function": ecommerce_tools.get_order_status,
        "description": "Retrieves the status and details of a specific order using its ID.",
        "parameters": {
            "type": "object",
            "properties": {"order_id": {"type": "string", "description": "The unique identifier for the order, e.g., 'ord_12345'."}},
            "required": ["order_id"]
        }
    },
    "recommend_products": {
        "function": ecommerce_tools.recommend_products,
        "description": "Recommends other products based on a specific product and criteria like 'related' items or 'top-rated' in the same category.",
        "parameters": {
            "type": "object",
            "properties": {
                "product_id": {"type": "string", "description": "The ID of the product to base recommendations on, e.g., 'p001'."},
                "criteria": {"type": "string", "description": "Recommendation criteria: 'related' or 'top-rated'. Defaults to 'related'."}
            },
            "required": ["product_id"]
        }
    },
    "get_general_help": {
        "function": ecommerce_tools.get_general_help,
        "description": "Provides general help or information about common topics like store hours, return policy, or contact info.",
        "parameters": {
            "type": "object",
            "properties": {"topic": {"type": "string", "description": "The topic the user is asking about, e.g., 'hours', 'return policy', 'contact'."}},
            "required": ["topic"]
        }
    },
    "add_to_cart": {
        "function": ecommerce_tools.add_to_cart,
        "description": "Adds a specified quantity of a product to the user's shopping cart.",
        "parameters": {
            "type": "object",
            "properties": {
                "product_id": {"type": "string", "description": "The unique ID of the product to add, e.g., 'p001'."},
                "quantity": {"type": "integer", "description": "The number of units of the product to add."}
            },
            "required": ["product_id", "quantity"]
        }
    },
    "view_cart": {
        "function": ecommerce_tools.view_cart,
        "description": "Shows the current contents of the user's shopping cart, including items and total price.",
        "parameters": {"type": "object", "properties": {}}
    },
    "get_product_reviews": {
        "function": ecommerce_tools.get_product_reviews,
        "description": "Retrieves customer reviews for a specific product by its ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "product_id": {"type": "string", "description": "The unique ID of the product to get reviews for, e.g., 'p007'."}
            },
            "required": ["product_id"]
        }
    }
}

# --- Agentic Core Logic ---
def choose_and_execute_tool(text: str):
    if not groq_client: return {"error": "LLM client not available."}
    tools_prompt = json.dumps([{"name": name, "description": data["description"], "parameters": data["parameters"]} for name, data in AVAILABLE_TOOLS.items()], indent=2)
    system_prompt = f"""You are an intelligent e-commerce assistant. Your task is to understand the user's request,
select the appropriate tool from the provided list, and extract the necessary parameters to call it.
Available tools: {tools_prompt}
Respond with ONLY a single, valid JSON object in the format: {{"tool_name": "...", "parameters": {{...}} }}
If no tool is suitable, respond with: {{"tool_name": "no_tool_found", "parameters": {{}} }}"""
    try:
        completion = groq_client.chat.completions.create(
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": text}],
            model=MODEL_NAME, temperature=0.0, max_tokens=256, response_format={"type": "json_object"}
        )
        choice_json = json.loads(completion.choices[0].message.content)
        tool_name = choice_json.get("tool_name")
        parameters = choice_json.get("parameters", {})
        logger.info(f"LLM decided to use tool '{tool_name}' with parameters: {parameters}")
        if tool_name in AVAILABLE_TOOLS:
            tool_function = AVAILABLE_TOOLS[tool_name]["function"]
            result = tool_function(**parameters)
            return {"tool_name": tool_name, "result": result}
        else:
            return {"tool_name": "no_tool_found", "result": "I am not sure how to help with that. Could you please rephrase your request?"}
    except Exception as e:
        logger.error(f"Agentic tool selection failed: {e}")
        return {"tool_name": "error", "result": f"An error occurred: {e}"}

emotion_detector = AdvancedEmotionDetector()
voice_synthesizer = VoiceSynthesizer()

def convert_audio_to_wav(input_path: str, output_path: str) -> bool:
  """Converts an audio file to WAV format using ffmpeg."""
  try:
    command = ['ffmpeg', '-i', input_path, '-ar', '16000', '-ac', '1', '-f', 'wav', output_path, '-y']
    subprocess.run(command, check=True, capture_output=True)
    logger.info(f"Successfully converted {input_path} to {output_path}")
    return True
  except (subprocess.CalledProcessError, FileNotFoundError) as e:
    logger.error(f"Audio conversion failed: {e}")
    # If ffmpeg command fails, log its output for debugging
    if isinstance(e, subprocess.CalledProcessError):
        logger.error(f"FFmpeg stderr: {e.stderr.decode()}")
    return False

# API Models
class TextInput(BaseModel):
  text: str

class ChatResponse(BaseModel):
  response_text: str
  emotion_data: Dict[str, Any]
  agent: str # Repurposed to show 'tool_used'
  audio_url: Optional[str] = None

# --- Helper function to process text (used by both endpoints) ---
async def process_text_request(text: str):
    logger.info(f"Processing text: {text}")
    emotion_data = emotion_detector.detect_comprehensive_emotion(text)
    tool_output = choose_and_execute_tool(text)
    tool_name = tool_output.get("tool_name", "error")
    tool_result = tool_output.get("result", {})

    response_text = ""
    if groq_client:
        system_prompt = f"""You are Natalie, an empathetic e-commerce assistant.
User's emotion: {emotion_data['emotion']} (Intensity: {emotion_data['intensity']}).
A tool was run to address the user's request.
User's request: "{text}"
Tool executed: "{tool_name}"
Data returned from the tool: {json.dumps(tool_result, indent=2)}
Synthesize this information into a single, friendly, natural-sounding response.
- If successful, explain the result clearly.
- If an error occurred or no tool was found, apologize and ask for clarification.
- Do not mention the tool name or raw data explicitly.
"""
        try:
            completion = groq_client.chat.completions.create(
                messages=[{"role": "system", "content": system_prompt}],
                model=MODEL_NAME, temperature=0.7, max_tokens=150,
            )
            response_text = completion.choices[0].message.content.strip()
            logger.info(f"LLM generated final response: {response_text}")
        except Exception as e:
            logger.error(f"LLM response generation failed: {e}")
            response_text = "I'm having a little trouble right now. Could you say that again?"
    else:
        response_text = str(tool_result)

    audio_url = voice_synthesizer.synthesize_speech(response_text, emotion_data)
    return ChatResponse(
        response_text=response_text,
        emotion_data=emotion_data,
        agent=tool_name,
        audio_url=audio_url,
    )

# --- Endpoints ---
@app.post("/process_speech", response_model=ChatResponse)
async def process_speech(audio_file: UploadFile = File(...)):
  temp_webm = None
  temp_wav = None
  try:
    # Step 1: Save the incoming WebM file from the browser
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp_webm:
        tmp_webm.write(await audio_file.read())
        temp_webm = tmp_webm.name

    # Step 2: Prepare a path for the output WAV file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
        temp_wav = tmp_wav.name

    # Step 3: Convert the WebM file to WAV using the helper function
    if not convert_audio_to_wav(temp_webm, temp_wav):
        raise HTTPException(status_code=500, detail="Audio conversion failed.")

    # Step 4: Process the properly converted WAV file
    with sr.AudioFile(temp_wav) as source:
      audio = recognizer.record(source)
      text = recognizer.recognize_google(audio)
    
    return await process_text_request(text)

  except sr.UnknownValueError:
    raise HTTPException(status_code=400, detail="Could not understand the audio")
  except sr.RequestError as e:
    raise HTTPException(status_code=503, detail=f"Speech recognition service unavailable: {e}")
  except Exception as e:
    logger.error(f"Speech processing error: {e}")
    raise HTTPException(status_code=500, detail="Speech processing failed")
  finally:
    # Clean up both temporary files
    if temp_webm and os.path.exists(temp_webm):
      os.unlink(temp_webm)
    if temp_wav and os.path.exists(temp_wav):
      os.unlink(temp_wav)

@app.post("/chat", response_model=ChatResponse)
async def chat(input_data: TextInput):
  return await process_text_request(input_data.text)

@app.get("/")
async def root():
  return {"message": "Agentic E-commerce Orchestrator running"}

@app.get("/health")
async def health():
  return {"status": "healthy"}

if __name__ == "__main__":
  import uvicorn
  uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
