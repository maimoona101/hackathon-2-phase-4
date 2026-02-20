# Authentication Skill

**Name:** authentication-jwt

**Purpose:**  
Provide secure, reusable JWT-based authentication for the Multi-user Full Stack Todo App (Phase II), ensuring that only authenticated users can access protected resources.

**Responsibilities:**  
- Handle user authentication using JWT tokens  
- Validate JWT on every protected API request  
- Ensure user identity is extracted from JWT, not from client input  
- Enforce multi-user security across all backend endpoints  
- Integrate with Better Auth (frontend) and FastAPI (backend) flow  
- Support environment-based shared JWT secret  

**Input:**  
- JWT token from frontend (Authorization header)  
- Authentication metadata from Better Auth  
- Incoming API request  

**Output:**  
- Verified user identity (user_id)  
- Authorization decision (allow / deny)  
- Authentication error messages for invalid or expired tokens  

**Rules / Constraints:**  
- JWT secret must be loaded from environment variables  
- User identity must come ONLY from verified JWT  
- Never trust client-provided user_id directly  
- Each request must be authenticated before accessing task data  
- Must be reusable for Phase III–V projects  
- Do NOT write any implementation code here, only define the skill
