# Neural Voice: A Full-Stack Empathetic Conversational Agentic AI Platform

<img width="251" height="381" alt="Screenshot from 2025-10-07 01-59-42" src="https://github.com/user-attachments/assets/4b7862ec-75da-401f-8c8d-b6516c1368cf" />







Neural Voice is a full-stack, emotion-aware conversational AI assistant engineered to elevate human-AI interactions. Utilizing a robust REST architecture and high-performance inference services, the system delivers contextually appropriate, empathetic responses synthesized with professional, emotion-adaptive voice technology.

## 1. Core Capabilities

The platform's core differentiator is its ability to process and adapt to human emotional states in real-time, delivering a truly personalized conversational experience.

| Feature                    | Technical Insight                                                    | Value Proposition                                                                           |
| :------------------------- | :------------------------------------------------------------------- | :------------------------------------------------------------------------------------------ |
| Advanced Emotion Detection | Multi-layered analysis (Keyword + Pattern + LLM) supporting 25+ distinct emotions and 3 intensity levels. | Robust, high-fidelity emotional understanding that surpasses basic sentiment analysis.      |
| Professional Voice Synthesis | Integration with Murf AI (en-US-natalie) with dynamic parameter adaptation for natural, empathetic speech. | Delivers a high-quality, professional, and emotionally expressive voice output.             |
| Empathetic AI Response     | Powered by Groq Llama 3.1 with sophisticated emotion-aware prompt engineering. | Ensures contextually and emotionally appropriate conversational flow.                       |
| Real-Time Processing       | Optimized HTTP REST pipeline for Speech-to-Text (STT) → Emotion → LLM → Text-to-Speech (TTS) workflow. | Low-latency, stable interaction loop for seamless voice communication.                      |

## 2. Technical Architecture
<img width="1324" height="407" alt="Screenshot from 2025-10-07 02-10-19" src="https://github.com/user-attachments/assets/57c77513-5f40-489d-b881-556f86bd1349" />



The backend implements a deterministic, sequential emotion-aware pipeline, prioritizing emotional accuracy and empathetic fidelity over raw speed.

### 2.1. Agentic AI Core: Intelligent Decision-Making and Tool Utilization


A central tenet of the Neural Voice platform is its **Agentic AI Core**, which moves beyond traditional conversational models to enable a system that can understand user intent, make autonomous decisions, and execute specific actions through a suite of integrated tools. This capability transforms the AI from a mere responder into an active participant capable of problem-solving and task fulfillment within the e-commerce domain.

#### Beyond Simple Question Answering

Unlike basic chatbots that rely on keyword matching or pre-scripted dialogue flows, the Agentic AI does not simply retrieve information. Instead, it processes natural language inputs to infer the user's underlying goal or task (e.g., "find me shoes," "add to cart," "check my order"). This involves a sophisticated understanding of context and conversational nuance.

#### The Reasoning and Planning Engine (LLM-Powered)

At the heart of the agentic core is a Large Language Model (LLM), specifically **Groq Llama 3.1**, which serves as the "brain." When a user's text is received:

* **Intent Extraction:** The LLM first identifies the primary intent. For instance, "I need some running shoes" triggers a "product search" intent.
* **Tool Selection:** Based on the identified intent and the current conversational context, the LLM dynamically selects the most appropriate tool from its predefined `Tool Library`.
* **Parameter Extraction:** Once a tool is selected, the LLM meticulously extracts all necessary parameters from the user's input to invoke that tool. For example, for a "product search," it would identify "running shoes" as the `query` and potentially "footwear" as the `category`.

#### The Tool Library: Expanding Capabilities

The Agentic AI's ability to act is governed by its `Tool Library` (implemented in `ecommerce_tools.py`). Each tool is a specialized function designed to perform a specific, externalized action or retrieve domain-specific information. This modular design allows for easy expansion of the agent's capabilities without altering its core reasoning logic.

Current tools empower the agent to:

* `search_products`: Query the product catalog with various filters.
* `recommend_products`: Suggest items based on user preferences or product relationships.
* `get_order_status`: Retrieve real-time information about customer orders.
* `add_to_cart`: Manage the user's shopping cart, adding specified products and quantities.
* `view_cart`: Display the current contents and total of the shopping cart.
* `get_product_reviews`: Fetch customer reviews for specific products.
* `get_general_help`: Provide information on common support topics (store hours, returns).

#### Action Execution and Result Processing

Once a tool and its parameters are determined, the `Action Executor` component programmatically calls the corresponding Python function. The result returned by the tool (e.g., a list of products, an order status, a confirmation of item added to cart) is then fed back into the LLM.

#### Intelligent Response Generation

The LLM (again, Groq Llama 3.1) performs a second, crucial task: **response synthesis**. It takes the raw output from the executed tool, integrates it with the user's original query, and most importantly, factors in the detected emotional state. This ensures that the final response is not only factually correct based on the tool's output but also empathetic, natural-sounding, and contextually appropriate. For example, if a user is "frustrated," the response might acknowledge that emotion before providing the requested information.

### 2.2. Processing Workflow

1.  **Input Acquisition:** Audio is uploaded via multipart/form-data.
2.  **Speech-to-Text (STT):** Transcription via Google Speech Recognition.
3.  **Emotion Detection:** Text analysis leveraging a multi-layered model (keyword matching, pattern recognition, LLM inference).
4.  **LLM Generation:** Groq Llama 3.1 generates emotionally attuned responses using the detected context.
5.  **Text-to-Speech (TTS):** Murf AI synthesizes the reply, dynamically adjusting speech rate, pitch, and tone based on the detected emotion and its intensity level.
6.  **Audio Delivery:** Playback of the natural, empathetic response.

### 2.3. Technology Stack

| Component            | Technology                         | Role                                                                    |
| :------------------- | :--------------------------------- | :---------------------------------------------------------------------- |
| Backend / Orchestration | Python (FastAPI)                   | Core REST endpoints, pipeline management, emotion processing.           |
| Inference (LLM)      | Groq Llama 3.1 8B Instant          | High-speed, context-aware response generation.                          |
| Emotion Engine       | Multi-layered Analysis             | Keyword, Pattern, and LLM-based emotion classification.                 |
| STT                  | Google Speech Recognition          | High-accuracy voice transcription.                                      |
| TTS                  | Murf AI (en-US-natalie)            | Professional voice synthesis with advanced emotional parameter control. |
| Frontend / UI        | HTML5, JavaScript, Web Audio API   | Voice recording, real-time visualization, and conversation interface.   |
| Audio Utilities      | FFmpeg, SpeechRecognition          | Audio format conversion and real-time processing.                       |

## 3. Deployment and Setup

### 3.1. Prerequisites

-   Python 3.8+ and pip
-   FFmpeg (System-level installation for audio processing)
-   Modern Web Browser with microphone support.
-   API Keys for Groq and Murf AI services.

### 3.2. Repository Setup

1.  **Clone the Repository:**

    ```bash
    git clone [https://github.com/yourusername/neural-voice.git](https://github.com/yourusername/neural-voice.git)
    cd neural-voice
    ```

2.  **Environment Setup:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate # On Windows: .\venv\Scripts\activate
    pip install -r requirements.txt
    ```

### 3.3. Running Locally

1.  **Start the Backend (FastAPI):**

    ```bash
    cd neural-voice
    source venv/bin/activate
    uvicorn main:app --reload # Assuming your main FastAPI app is in main.py
    # Server runs on http://localhost:8000
    ```

2.  **Start the Frontend:**
    You'll need a simple HTTP server to serve `index.html`.

    ```bash
    # Option 1: Using Python's built-in HTTP server (from the neural-voice directory)
    python -m http.server 3000
    # or:
    # Option 2: Using a Node.js http-server (if you have Node.js/npm installed)
    # npm install -g http-server
    # http-server -p 3000
    ```

3.  **Access:** Navigate to `http://localhost:3000` in your browser.

## 4. API Reference

Base URL: `http://localhost:8000`

### 4.1. Complete Emotion-Aware Pipeline

**`POST /chat`**

| Parameter | Type   | Description                |
| :-------- | :----- | :------------------------- |
| `text`    | string | The user's input text.     |

**Purpose:** Executes STT → Emotion → LLM → TTS workflow. Accepts text, returns response text, emotion analysis, and audio URL.

**Example Request:**

```bash
curl -s -X POST "http://localhost:8000/chat" \
-H "Content-Type: application/json" \
-d '{"text": "I am so frustrated with this problem!"}'
```

**Example Response (200 OK):**

```json
{
  "response_text": "I understand that feeling anxious before a presentation is completely normal. You've got this!",
  "emotion_data": {
    "emotion": "anxiety",
    "confidence": 0.87,
    "intensity": "high"
  },
  "agent": "no_tool_found",
  "audio_url": "[https://murf.ai/user-upload/temp/response-audio.wav](https://murf.ai/user-upload/temp/response-audio.wav)"
}
```

### 4.2. Supporting Endpoints

| Endpoint          | Method | Purpose                                                          | Data Type          |
| :---------------- | :----- | :--------------------------------------------------------------- | :----------------- |
| `/process_speech` | POST   | Transcribes audio file and performs emotion detection.           | `multipart/form-data` |
| `/chat`           | POST   | Processes text input through the agentic pipeline.               | `application/json` |
| `/health`         | GET    | Checks service availability (backend, Groq, Murf AI).            | None               |

*Note: The `/detect_emotion` and `/synthesize_speech` endpoints mentioned in your sample are not explicitly created as standalone endpoints in the provided `main.py`. The full `/chat` and `/process_speech` endpoints encapsulate this functionality. If you wish to expose them, you would need to add them to `main.py`.*

## 5. Directory Structure

A standardized, organized file structure for rapid development and maintenance.

```
neural-voice/
├── main.py                     # FastAPI orchestration, REST endpoints, agentic logic
├── ecommerce_tools.py          # Tools library for e-commerce specific actions
├── index.html                  # Core frontend interface
├── requirements.txt            # Project dependencies
├── .env.example                # Example environment variables file
├── .env                        # Environment variables (Sensitive configuration, excluded from Git)
└── README.md                   # This documentation
```

## 6. Production Deployment Notes

For robust, production-ready deployment, adhere to the following best practices:

-   **Service Hosting:** Deploy the backend using Gunicorn + Uvicorn workers, tuning the worker count to the host CPU cores.
-   **Security:** Enforce HTTPS for all client-side interactions to ensure microphone access and data security.
-   **API Management:** Implement strict rate limiting and request size controls at the ASGI or gateway layer.
-   **Observability:** Log emotion analytics and system events using structured logging for conversation insights and error tracking.
-   **Optimization:** Implement audio response caching to reduce latency and API costs for frequently triggered emotional phrases.

## 7. Roadmap and Future Development

The platform is evolving towards a more personalized and integrated conversational experience.

-   **Real-time Streaming:** Implement WebSocket for streaming emotion detection and low-latency response delivery.
-   **Contextual Memory:** Integrate Conversation Memory for multi-turn emotion tracking and deeper personalization.
-   **Advanced Profiling:** Develop Psychological Profiling based on emotion patterns for mental health and customer service applications.
-   **Mobile Integration:** Release Mobile SDKs for iOS and Android with optimized on-device audio preprocessing.

---

## Configuration

### System Dependencies (FFmpeg):

| OS              | Command                                                                 |
| :-------------- | :---------------------------------------------------------------------- |
| Ubuntu/Debian   | `sudo apt update && sudo apt install ffmpeg portaudio19-dev`            |
| macOS           | `brew install ffmpeg portaudio`                                         |
| Windows         | Download FFmpeg and add the executable to the system PATH.              |

### Configuration File (`.env`):

Create a `.env` file based on `.env.example` and populate the API keys.

```env
# .env file

GROQ_API_KEY="gsk_your_groq_api_key_here"
MURF_API_KEY="your_murf_api_key_here"
GROQ_MODEL="llama-3.1-8b-instant"
# ... other configuration settings
```

---

