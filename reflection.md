# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
The initial design follows an Object-Oriented Architecture utilizing a Controller-Entity-Strategy pattern. This approach separates the data models from the scheduling engine, ensuring that the application remains modular and easy to extend. The flow is centralized: the AppController facilitates interaction between the user and the system, the Pet and Task classes act as data containers, and the SchedulePlanner serves as the logic engine that evaluates constraints to generate an optimized Plan. This structure allows the core scheduling algorithm to be swapped or updated independently of the user interface.
- What classes did you include, and what responsibilities did you assign to each?
I have identified five core classes to handle the system's requirements:

Pet: Functions as the primary entity representing the animal. It manages the state and maintains a collection of Task objects associated with that specific pet.

Task: A data model representing a single care requirement. It stores critical attributes such as name, priority (to handle importance), duration (to manage time constraints), and is_recurring status.

SchedulePlanner: The central logic engine. It is responsible for ingesting user constraints (e.g., total available time, specific preferences) and performing the algorithmic selection of tasks to create an optimized daily schedule.

Plan: A container class that acts as the output of the SchedulePlanner. It holds the finalized list of selected_tasks and the generated rationale string, which explains the logic behind why certain tasks were prioritized or deferred.

AppController: Acts as the bridge between the backend logic and the Streamlit UI. It manages the lifecycle of the application, handling user inputs from the interface and triggering the appropriate methods within the other classes to return the final view.
**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
