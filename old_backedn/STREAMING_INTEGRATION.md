# LangGraph Streaming Integration

## Overview
This document explains the streaming functionality integrated into your legal research AI application using LangGraph's streaming capabilities.

## Features Implemented

### 1. **Multiple Streaming Modes**
- **`updates` mode**: Shows progress after each graph node execution
- **`messages` mode**: Streams LLM tokens as they're generated (when properly configured)
- **Custom status updates**: Manual progress indicators

### 2. **Enhanced Node Functions**
All nodes now support streaming with backward compatibility:

#### Direct Answer Node
- Streams LLM responses in real-time
- Enhanced prompt formatting for better legal advice
- Maintains compatibility with non-streaming calls

#### Retriever Node  
- Fetches data from Indian Kanoon API
- Enhanced error handling
- Progress tracking capability

#### Summarizer Node
- Streams legal case analysis
- Better case formatting and filtering (top 5 cases)
- Structured analysis with clear sections

#### Formatter Node
- Streams final report generation
- Professional legal report formatting with emojis
- Comprehensive legal analysis structure

### 3. **FastAPI Streaming Endpoint**

#### New Endpoint: `/ask-stream`
- **Method**: POST
- **Content-Type**: `application/json`
- **Response**: Server-Sent Events (SSE)

#### Request Format:
```json
{
    "query": "What is a contract in Indian law?",
    "research_mode": false
}
```

#### Response Stream Events:
```javascript
// Status updates
{"type": "status", "message": "Starting analysis...", "step": "init"}

// Node completion
{"type": "node_complete", "node": "retriever", "message": "Legal database search completed"}

// Final result
{"type": "final_result", "report": "...", "mode": "research"}

// Completion
{"type": "complete"}

// Errors
{"type": "error", "message": "Error description"}
```

## Usage Examples

### 1. Backend Testing
```bash
cd backend
python test_streaming.py
```

### 2. Frontend Integration
Open `streaming_example.html` in a browser to test the streaming UI.

### 3. API Testing with curl
```bash
curl -X POST "http://localhost:8000/ask-stream" \
  -H "Content-Type: application/json" \
  -d '{"query": "contract law India", "research_mode": true}' \
  --no-buffer
```

### 4. JavaScript/React Integration
```javascript
const response = await fetch('http://localhost:8000/ask-stream', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream'
    },
    body: JSON.stringify({
        query: "What is a contract?",
        research_mode: false
    })
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    
    const chunk = decoder.decode(value, { stream: true });
    const lines = chunk.split('\n');
    
    for (const line of lines) {
        if (line.startsWith('data: ')) {
            const data = JSON.parse(line.slice(6));
            handleStreamEvent(data);
        }
    }
}
```

## Benefits

### 1. **User Experience**
- Real-time feedback during legal research
- Progress indicators for long-running queries
- Responsive, ChatGPT-like interface

### 2. **Performance**
- Non-blocking operations
- Better handling of long API calls
- Reduced perceived latency

### 3. **Transparency**
- Users see each step of the legal research process
- Clear indication of data sources being used
- Better trust and understanding

## Technical Details

### Stream Configuration
```python
stream_config = {
    "configurable": {
        "stream_mode": ["updates", "messages"]
    }
}
```

### Error Handling
- Graceful degradation to non-streaming mode
- Comprehensive error reporting
- Connection cleanup on failures

### CORS Configuration
Streaming endpoint includes proper CORS headers:
```python
headers={
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "*"
}
```

## Backward Compatibility
- Original `/ask` endpoint remains unchanged
- All nodes work with or without streaming config
- Existing frontend code continues to work

## Next Steps
1. Test with your React frontend
2. Add token-level streaming for LLM responses
3. Implement custom progress events for Indian Kanoon API calls
4. Add streaming metrics and monitoring

## Troubleshooting

### Common Issues
1. **CORS errors**: Ensure proper headers in streaming response
2. **Connection drops**: Implement reconnection logic in frontend
3. **Large responses**: Consider chunking very large legal documents
4. **API timeouts**: Add timeout handling for Indian Kanoon API calls

### Debug Mode
Set environment variable for detailed logging:
```bash
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
```


