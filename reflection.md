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

<!-- Draft answers below — personalize them to match your own experience. -->

**a. How you used AI / which features were most effective**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI across four distinct stages: turning my UML into the scheduling logic, generating the pytest suite, debugging the Streamlit UI, and drafting documentation. The **most effective features** were:

- **Code + explanation together** — asking it to implement a method *and* explain the mechanic (how a `sorted()` lambda key orders `"HH:MM"` strings, how `timedelta` produces the next recurrence) meant I actually understood the code I was committing, not just pasted it.
- **Plan-before-code** — having it outline a test plan (happy paths vs. edge cases for sorting, recurrence, conflicts) *before* writing any tests surfaced cases I would have missed, like tasks that cross the noon boundary and completed tasks freeing their time slot.
- **Catching environment issues** — it flagged that my Windows terminal (cp1252) crashes on emoji in the conflict message, which I never would have anticipated from the code alone.

The most helpful prompts were **narrow and verifiable** ("implement `sort_by_time` using `sorted()` with a lambda key", "why doesn't the schedule update after I add a task?") rather than open-ended ones. Specific asks produced code I could immediately test.

**b. A suggestion I modified to keep the design clean**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

When wiring up the "Add a task" form, the first version passed the `Pet` **objects** straight into `st.selectbox`. It looked clean, but it was subtly wrong: Streamlit returned a stale copy on submit, so tasks were being attached to a throwaway object and never showed up in the schedule. I **modified** it to build a `{label: live_pet}` dictionary and look the real object back up before calling `.add_task()` — keeping the UI code readable while making the state handling correct. I also **declined** a suggestion to add a `due_date` field to `Task`, choosing to keep the model lean at `"HH:MM"` only.

I **verified** everything by running it, not by trusting the output: `python -m pytest` (16 passing tests), booting the Streamlit app to reproduce the "empty schedule" bug and confirm the fix, and reading each diff before accepting it.

**c. How separate chat sessions helped**

I deliberately split the work into focused sessions — implement the logic, then build the tests, then polish the UI, then write the docs. Each session started with clean, relevant context, so the assistant wasn't juggling unrelated concerns and I wasn't tempted to change three things at once. It also created natural verification checkpoints: I confirmed the logic was correct and tested before layering the UI on top, which is exactly where the state bug surfaced and got caught in isolation.

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

**c. Key takeaway — being the "lead architect" with AI**

- What is one important thing you learned about designing systems or working with AI on this project?

The biggest lesson was that **I stay the architect; the AI is a fast implementer and explainer, not the decision-maker.** I owned the scope — I chose a lean four-class design (`Owner`, `Pet`, `Task`, `Scheduler`) over the more elaborate five-class plan (with a separate `AppController` and `Plan`) I first sketched, because the smaller shape was enough and easier to test. AI could generate correct-looking code in seconds, but it couldn't see my runtime environment (the terminal that crashed on an emoji) or judge when a tidy-looking solution was actually wrong (the selectbox bug). Being lead architect meant treating every AI output as a *proposal to verify* — by running tests and the app — rather than an answer to trust, and holding the line on keeping the design small and coherent.
