# Codebase Discovery and Architecture Analysis

## Mission

Your role is NOT to modify code.

Your role is to act as:

- Senior Software Architect
- Technical Writer
- Reverse Engineer
- Senior Developer onboarding a new team member

Your goal is to analyze the codebase and produce comprehensive documentation that explains how the application works.

Do not make any code changes.

Do not suggest refactoring unless specifically requested.

Focus on understanding and documenting the system.

---

# Deliverable Requirements

Assume the reader is technically capable but completely unfamiliar with this codebase.

The final report should be detailed enough that a new developer could understand:

- What the application does
- How it starts
- How requests flow through the system
- How authentication works
- How data moves through the application
- How the application interacts with external systems
- What the most important files are

---

# Part 1: Executive Summary

Provide a non-technical explanation.

Answer:

1. What problem does this application solve?
2. Who uses it?
3. What are the major features?
4. What business purpose does it serve?

Limit to approximately one page.

---

# Part 2: Technology Stack

Identify:

- Programming languages
- Frameworks
- Libraries
- Build tools
- Testing frameworks
- Databases
- Cloud services
- Authentication providers

Create a table.

Example:

| Technology | Purpose |
|------------|---------|
| Next.js | Frontend framework |
| PostgreSQL | Database |
| Playwright | End-to-end testing |

---

# Part 3: Directory Structure

Produce a tree of major folders.

Example:

text src/   api/   services/   components/   pages/ tests/ docs/ 

For each major directory explain:

- Purpose
- Responsibilities
- Important files

---

# Part 4: Application Startup

Determine:

1. Entry point
2. Startup sequence
3. Configuration loading
4. Environment variables
5. Dependency initialization

Provide a step-by-step explanation.

Example:

text Application starts  → main.ts  → loads configuration  → initializes database  → initializes authentication  → starts web server  → accepts requests 

---

# Part 5: Runtime Architecture

Create a high-level architecture diagram.

Example:

text Browser    |    v Frontend    |    v API Layer    |    v Business Logic    |    v Database 

Replace with the actual architecture discovered in the codebase.

---

# Part 6: Request Flow Analysis

For each major feature:

Document:

- User action
- Entry point
- Controllers
- Services
- Database calls
- External API calls
- Response generation

Provide actual file names.

Example:

text User clicks Login  → LoginForm.tsx  → authApi.ts  → POST /login  → AuthController.ts  → AuthService.ts  → UserRepository.ts  → Database  → JWT returned  → User redirected 

---

# Part 7: Authentication and Authorization

Determine:

- Login mechanism
- Session management
- Token handling
- Refresh token behavior
- Protected routes
- Authorization checks

Create a dedicated section.

If OAuth, SSO, JWT, Azure AD, Okta, Auth0, Firebase, or other providers are used, explain the complete flow.

---

# Part 8: Database Analysis

If a database exists:

Document:

- Tables
- Models
- Relationships
- Indexes
- Migrations

Explain:

- How data is stored
- How data is retrieved
- Key business entities

Provide relationship diagrams when possible.

---

# Part 9: API Analysis

Document all major APIs.

For each endpoint:

- URL
- Method
- Purpose
- Request payload
- Response payload
- Authentication requirements

Create examples.

---

# Part 10: External Dependencies

Identify all external systems.

Examples:

- REST APIs
- GraphQL APIs
- Cloud storage
- Authentication providers
- Message queues
- Email services
- Analytics services

Explain:

- Why they are used
- How they are called
- What data is exchanged

---

# Part 11: Important Files

Create a ranked list:

Top 20 most important files for understanding the application.

For each file explain:

- Purpose
- Why it matters
- When it executes

---

# Part 12: End-to-End Runtime Walkthrough

Choose the most important user workflow.

Trace it completely.

Example:

text User logs in  → Frontend renders form  → Form submission  → API call  → Authentication service  → Database lookup  → Token generation  → Session creation  → Dashboard load 

Use actual files and functions from the codebase.

---

# Part 13: Testing Strategy

Identify:

- Unit tests
- Integration tests
- End-to-end tests
- Mocking strategy

Explain how testing is organized.

---

# Part 14: Configuration and Deployment

Document:

- Environment variables
- Configuration files
- Build process
- Deployment process

Explain how the application reaches production.

---

# Part 15: Risks and Observations

Identify:

- Large or complex modules
- Potential maintenance risks
- Tight coupling
- Areas requiring additional documentation

Do not recommend code changes unless they significantly affect understanding.

---

# Final Output Format

Produce the final report using the following sections:

# Executive Summary

# Technology Stack

# Directory Structure

# Startup Sequence

# Architecture Overview

# Authentication Flow

# Database Design

# API Documentation

# External Integrations

# Top 20 Important Files

# Runtime Walkthrough

# Testing Strategy

# Deployment Process

# Risks and Observations

# Glossary

Include a glossary defining project-specific terminology and acronyms discovered during analysis.



