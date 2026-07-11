# Nur Academy: Foundational Manual

## 🎯 Vision
To provide a premium, modern, and highly effective AI-powered study environment for IGCSE Islamiyat and Pakistan Studies students, combining deep traditional knowledge with cutting-edge UX/UI.

## 🏛️ Architectural Mandates
1.  **Decoupled & Scalable:** Keep the Frontend (Next.js) and Backend (FastAPI) strictly separated to allow independent scaling on Google Cloud Run.
2.  **API-First Logic:** All business logic, AI interactions, and file I/O must reside in the FastAPI backend. The frontend should be a stateless visual engine.
3.  **Strict Validation:** Use Pydantic models for all API requests and responses to ensure data integrity.
4.  **Persistent Storage:** Continue using JSON-based storage in `backend/data/` for simplicity and portability, while ensuring robust path handling.

## 🛠️ Key Functionalities & Implementation
### 1. The Memorize Engine (Interactive Typing)
- **Logic:** Character-by-character matching between student input and reference text.
- **Visuals:** 
    - `text-slate-400`: Untyped characters.
    - `text-emerald-700 font-bold`: Correctly typed.
    - `text-red-500 bg-red-100`: Typos.
    - `animate-pulse`: Active cursor position.
- **UX Enhancements:** 
    - Real-time search bar for topic selection.
    - **Topic Grouping:** Topics are structured under categorized headings (e.g., Tier 1, Tier 2).
    - Auto-scrolling text container that keeps the active line centered.
    - Smart navigation: The bottom Nav bar button dynamically starts or resets sessions based on context.
- **State:** Managed via `typedLines` array, `activeLineIdx`, and `searchQuery` in React.

### 2. The Exam Engine (Dynamic Generation)
- **Generation:** API filters the full question bank based on student selection and returns a randomized subset.
- **Navigation:** Integrated "Question Map" allowing instant jumps across the exam paper.
- **Evaluation:** Automated scoring of MCQs; result objects saved to student history as JSON attempts.

### 3. Content Enrichment
- **Topic 2:** Significantly expanded from detailed study guide PDF. Includes 11 cards covering Revelation, Preservation, Compilation, and Authority of the Quran.
- **Pakistan Studies Syllabus Tiers:** Syllabi content categorized into three Tiers (Tier 1: Critical, Tier 2: Most Important, Tier 3: Nice to Learn) applied to both Exam and Memorize engines.
- **Pakistan Studies Memorize:** Expanded from 5 to **11 topics**. The 5 original topics had their lines enhanced for accuracy/exam-relevance; 6 new topics added (2 per tier): Key Dates Timeline & Founding Leaders (T1); Physical Geography & Economic Challenges (T2); Population & Employment & Nuclear Programme/Global Role (T3). All content is anchored to the LRN 2107 spec + Nov/Dec 2025 paper/mark scheme + revision booklet in `backend/data/source_docs/pak_studies/`. File: `backend/data/pak_studies/memorize_content.json` — keep cards grouped by tier (tier order = JSON first-appearance order).
- **Standardization:** All em-dashes (`—`) and en-dashes (`–`) replaced with simple hyphens (`-`) for keyboard ease. Memorize lines must stay plain typeable ASCII since the engine matches input character-by-character.

### 4. Frontend Typing
- Memorize cards are typed via the `MemCard` interface in `src/App.tsx` (`memData`/`memQueue` are `MemCard[]`, not `any[]`).
- The tier-grouping `.map((groupId: string) => ...)` callback must keep its explicit `string` annotation; otherwise TS widens it to `unknown` and `npm run lint` (`tsc --noEmit`) fails. `npm run build` (Vite/esbuild) does **not** typecheck, so always run `npm run lint` to catch type regressions.

## 🚀 Development Roadmap
- [ ] **Social Auth:** Implement NextAuth.js (Auth.js) with Google/Facebook providers.
- [ ] **Mobile Optimization:** Further refine the "Typer" for virtual mobile keyboards.
- [ ] **AI Feedback:** Port the Claude-powered exam analysis logic into a dedicated `/api/exam/analyze` endpoint.
- [ ] **Deployment:** Create Dockerfiles for both frontend and backend for Google Cloud Run deployment.
