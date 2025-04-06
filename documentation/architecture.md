graph TD
    A[User Interface] --> B[API Gateway]
    B --> C[Negotiation Engine]
    B --> D[Emotion Analyzer]
    B --> E[Digital Twin]
    C --> F[Guardian AI]
    D --> F
    E --> F
    F --> B
