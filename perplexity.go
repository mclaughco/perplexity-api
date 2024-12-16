// Package main provides a script to interact with the Perplexity API.
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io"
    "log"
    "net/http"
    "os"
    "strings"
    "time"
    "unicode"
    "github.com/joho/godotenv"
)

// PPLX_API_URL is the endpoint for Perplexity's chat completions API.
const PPLX_API_URL = "https://api.perplexity.ai/chat/completions"

// Message represents a single message in the chat conversation.
type Message struct {
    Role    string `json:"role"`
    Content string `json:"content"`
}

// ChatRequest represents the structure of a request to the Perplexity API.
type ChatRequest struct {
    Model    string    `json:"model"`
    Messages []Message `json:"messages"`
}

// ChatResponse represents the structure of a response from the Perplexity API.
type ChatResponse struct {
    ID      string    `json:"id"`
    Choices []Choice  `json:"choices"`
    Error   *APIError `json:"error,omitempty"`
}

// Choice represents a single choice in the API response.
type Choice struct {
    Message Message `json:"message"`
}

// APIError represents an error returned by the API.
type APIError struct {
    Message string `json:"message"`
}

// rateLimiter is used to control the rate of API requests.
var rateLimiter = time.Tick(time.Second / 10) // 10 requests per second


func getModelChoice() string {
    fmt.Println("Select a model:")
    fmt.Println("1. llama-3.1-sonar-small-128k-online")
    fmt.Println("2. llama-3.1-sonar-large-128k-online")
    fmt.Println("3. llama-3.1-sonar-huge-128k-online")
    
    var choice string
    fmt.Print("Enter your choice (1, 2, or 3): ")
    fmt.Scanln(&choice)
    
    switch choice {
    case "1":
        return "llama-3.1-sonar-small-128k-online"
    case "2":
        return "llama-3.1-sonar-large-128k-online"
    case "3":
        return "llama-3.1-sonar-huge-128k-online"
    default:
        log.Fatal("Invalid model choice")
        return ""
    }
}

// main is the entry point of the script.
func main() {
    // Load .env file
    err := godotenv.Load()
    if err != nil {
        log.Fatal("Error loading .env file")
    }

    // Get the API key
    apiKey := os.Getenv("PPLX_API_KEY")
    if apiKey == "" {
        log.Fatal("PPLX_API_KEY not found in environment")
    }

    // Create the request payload.
    request := ChatRequest{
        Model: getModelChoice(), // or "sonar-small-chat"
        Messages: []Message{
            {
                Role:    "user",
                Content: sanitizeInput("What are the three laws of robotics?"),
            },
        },
    }

    // Convert request to JSON.
    jsonData, err := json.Marshal(request)
    if err != nil {
        log.Fatalf("Error marshaling request: %v", err)
    }

    // Create HTTP request.
    req, err := http.NewRequest("POST", PPLX_API_URL, bytes.NewBuffer(jsonData))
    if err != nil {
        log.Fatalf("Error creating request: %v", err)
    }

    // Set headers.
    req.Header.Set("Content-Type", "application/json")
    req.Header.Set("Authorization", "Bearer "+apiKey)

    // Send request with rate limiting.
    <-rateLimiter
    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        log.Fatalf("Error sending request: %v", err)
    }
    defer resp.Body.Close()

    // Read response body.
    body, err := io.ReadAll(resp.Body)
    if err != nil {
        log.Fatalf("Error reading response: %v", err)
    }

    // Parse response.
    var chatResponse ChatResponse
    if err := json.Unmarshal(body, &chatResponse); err != nil {
        log.Fatalf("Error parsing response: %v", err)
    }

    // Check for API errors.
    if chatResponse.Error != nil {
        log.Fatalf("API Error: %s", chatResponse.Error.Message)
    }

    // Print the response.
    if len(chatResponse.Choices) > 0 {
        fmt.Println("Response:", chatResponse.Choices[0].Message.Content)
    } else {
        fmt.Println("No response received")
    }
}

// sanitizeInput removes potentially harmful characters from the input string.
func sanitizeInput(input string) string {
    return strings.Map(func(r rune) rune {
        if unicode.IsLetter(r) || unicode.IsNumber(r) || r == ' ' {
            return r
        }
        return -1
    }, input)
}
