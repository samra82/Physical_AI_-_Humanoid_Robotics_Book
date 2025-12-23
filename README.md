# Physical AI & Humanoid Robotics Textbook

![Project Banner](/display.PNG)

## Overview

This project is a comprehensive textbook for teaching **Physical AI & Humanoid Robotics**, created using:

- **Claude Code** – AI-assisted writing
- **Spec-Kit Plus** – Specification-driven book creation
- **MCP Cortex 7** – Modular content planning & management
- **Docusaurus** – Documentation framework
- **Mermaid** – Flowchart and diagram generation

The book bridges the gap between digital AI models and physical robots, teaching students how to simulate, control, and deploy humanoid robots for real-world tasks.

---

## Project Structure

This project is organized into two main components:

- **Frontend (`my-book/`)**: Docusaurus-based documentation site with interactive textbook content
- **Backend (`backend/`)**: RAG (Retrieval-Augmented Generation) system for AI-powered Q&A

For detailed information about each component, see their respective README files:
- [Frontend README](./my-book/README.md)
- [Backend README](./backend/README.md)

---

## What This Book Covers

This textbook introduces **Physical AI** and embodied intelligence. It covers:

- Robotic control using **ROS 2**
- Simulation of humanoid robots in **Gazebo** and **Unity**
- Advanced AI perception with **NVIDIA Isaac™**
- Integration of **LLMs** and voice commands for autonomous robots
- Capstone project: building an autonomous humanoid capable of perception, planning, and interaction

---

## Why Physical AI Matters

Humanoid robots are designed to operate in human-centered environments. By combining AI with physical embodiment, students learn to apply AI beyond digital simulations and into real-world robotic applications.

---

## Learning Outcomes

By completing this textbook, students will be able to:

- Understand Physical AI principles and embodied intelligence
- Control robots using ROS 2
- Simulate humanoid robots with Gazebo and Unity
- Develop with NVIDIA Isaac AI robotics platform
- Design humanoid robots for natural interactions
- Use GPT models for conversational robotics

---

## Special Features

- **Interactive Docusaurus Book:** Fully navigable online textbook with integrated chatbot
- **AI-Powered Q&A:** RAG system for answering questions about the textbook content
- **Spec-Kit Plus Integration:** Ensures clear and consistent specification-driven content
- **Modular MCP Cortex 7:** Organize content for easy updates and extensions

---

## Tech Stack

### Frontend
- **Docusaurus** – Documentation framework
- **React** – UI framework for interactive components
- **TypeScript** – Type-safe development
- **CSS Modules** – Component-scoped styling

### Backend
- **FastAPI** – Web framework for API
- **Cohere** – Embedding generation
- **Qdrant** – Vector database
- **OpenRouter** – LLM API access

### Tools & Infrastructure
- **Spec-Kit Plus** – Specification-driven book creation
- **Claude Code** – AI-assisted content writing
- **MCP Cortex 7** – Modular content management
- **Mermaid** – Diagrams and flowcharts

---

## Languages Used

- **TypeScript** – Primary programming language for Docusaurus components
- **Python** – Backend services and RAG pipeline
- **React** – UI framework for interactive components
- **Markdown** – For content writing and documentation

---

## Deployment

The textbook frontend is deployed using **Vercel**. You can access the live version here: [Physical AI & Humanoid Robotics Book](https://physical-ai-humanoid-robotics-book-steel.vercel.app/)

The backend API is deployed and accessible at: https://samra82-book-chatbot.hf.space/
API documentation is available at: https://samra82-book-chatbot.hf.space/docs

The backend provides the RAG (Retrieval-Augmented Generation) functionality for the AI-powered Q&A system. You can test the API endpoints directly at the deployed URL:
- Health check: https://samra82-book-chatbot.hf.space/api/v1/health
- Chat endpoint: https://samra82-book-chatbot.hf.space/api/v1/chat
- Legacy ask endpoint: https://samra82-book-chatbot.hf.space/ask

---

## Getting Started

### Frontend Setup
1. Navigate to the frontend directory: `cd my-book`
2. Install dependencies: `npm install`
3. Start the development server: `npm start`

### Backend Setup
1. Navigate to the backend directory: `cd backend`
2. Install Python dependencies: `pip install -r requirements.txt`
3. Set up environment variables (see `.env` file)
4. Start the API server: `uvicorn api:app --host 0.0.0.0 --port 8000`

For detailed setup instructions, refer to the individual README files:
- [Frontend README](./my-book/README.md)
- [Backend README](./backend/README.md)

