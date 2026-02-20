# Task Management Skill

**Name:** task-management

**Purpose:**  
Handle CRUD operations for tasks in the Multi-user Full Stack Todo App (Phase II), ensuring multi-user behavior and integration with backend API endpoints.

**Responsibilities:**  
- Create, Read, Update, Delete tasks  
- Toggle task completion  
- Ensure each user can only access their own tasks  
- Integrate with backend API endpoints:
  - `/api/{user_id}/tasks`
  - `/api/{user_id}/tasks/{id}`
  - `/api/{user_id}/tasks/{id}/complete`
- Provide structured output for Builder Agent  
- Follow Spec → Plan → Tasks flow  

**Input:**  
- Feature plan from Planner Agent  
- User authentication info (JWT)  
- Task data (title, description, status, id)  

**Output:**  
- Structured task objects  
- Confirmation of successful operations (create/update/delete/complete)  
- Error messages if user tries unauthorized access  

**Rules / Constraints:**  
- No user can access another user's tasks  
- Follow API endpoint structure exactly  
- Maintain multi-user integrity  
- Follow reusable skill pattern for future projects  
- Do NOT write any implementation code here, only define the skill
