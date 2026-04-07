# Auth UI Implementation Plan

## Overview
Create a React + Vite frontend with Tailwind CSS for the auth-service backend. The UI will feature a dark theme with lime/yellow-green neon accents, smooth animations, and proper API integration.

## Project Structure
```
auth-service/
├── frontend/                    # New React + Vite project
│   ├── src/
│   │   ├── components/
│   │   │   ├── auth/
│   │   │   │   ├── LoginForm.jsx
│   │   │   │   ├── SignupForm.jsx
│   │   │   │   ├── AuthToggle.jsx
│   │   │   │   └── InputField.jsx
│   │   │   └── ui/
│   │   │       ├── Button.jsx
│   │   │       └── LoadingSpinner.jsx
│   │   ├── api/
│   │   │   └── authApi.js       # Axios API layer
│   │   ├── hooks/
│   │   │   └── useAuth.js       # Auth state management
│   │   ├── styles/
│   │   │   └── globals.css      # Custom animations & utilities
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
```

## Step 1: Initialize React + Vite Project
- Create `frontend/` directory using Vite with React template
- Install dependencies: React, Axios v1.10, Tailwind CSS, react-router-dom
- Configure Tailwind CSS with custom theme (dark mode, lime accent color)
- Set up Vite proxy for API calls to `http://localhost:8000`

## Step 2: Create API Layer (`src/api/authApi.js`)
- Configure Axios instance with base URL and credentials (for cookies)
- Implement `signup(name, email, password)` - POST to `/api/user/signup`
- Implement `signin(email, password)` - POST to `/api/user/signin`
- Handle response transformations and error formatting
- Export typed error messages for UI display

## Step 3: Create Reusable UI Components

### `src/components/ui/Button.jsx`
- Neon lime primary button with hover/press animations
- Loading state support with spinner
- Scale animation on press (transform: scale(0.98))
- Smooth transitions using Tailwind + custom CSS

### `src/components/ui/InputField.jsx`
- Rounded input with subtle inner shadow (glossy effect)
- Focus animation with lime border glow
- Support for password visibility toggle
- Error state styling
- Icon support (email, lock icons)

### `src/components/ui/LoadingSpinner.jsx`
- Minimal spinner component for loading states

## Step 4: Create Auth Form Components

### `src/components/auth/AuthToggle.jsx`
- Toggle button to switch between Login and Signup
- Smooth slide/fade transition animation
- Active state indicator with lime accent

### `src/components/auth/LoginForm.jsx`
- Email input field
- Password input with visibility toggle
- "Remember me" checkbox
- "Forgot password?" link (placeholder)
- Submit button with loading state
- Form validation (email format, password required)
- Error message display
- Success state handling (mock redirect)

### `src/components/auth/SignupForm.jsx`
- Name input field
- Email input field
- Password input with visibility toggle
- Submit button with loading state
- Form validation (all fields required, email format)
- Error message display
- Success state handling (redirect to login)

## Step 5: State Management (`useAuth.js`)

Manage:

* mode (login/signup)
* loading, error, success states

Flow:

* idle → loading → success/error

Important:

* DO NOT store tokens (no localStorage, no memory storage)
* Auth state is NOT persisted in frontend
* Treat authentication as a request-response cycle only

---

## API Behavior

* Axios v1.10 with `withCredentials: true`
* Backend handles authentication via HTTP-only cookies
* Frontend does NOT manage tokens

Handle:

* loading state
* error state (invalid credentials, server errors)
* success state (trigger redirect or callback)

---

## Security Model

* No token storage in frontend
* Authentication handled by backend (cookies/session)
* Frontend remains stateless and reusable across projects


## Step 6: Create Main App Component (`src/App.jsx`)
- Centered card layout with dark background
- Floating blurred gradient shapes for background decoration
- Entry animation (fade + slight slide up)
- Responsive layout (mobile-first, flexbox)
- Integrate LoginForm and SignupForm with AuthToggle
- Display error/success messages

## Step 7: Styling & Animations (`src/styles/globals.css`)
- Custom CSS animations:
  - Fade-in with slide-up for card entry
  - Smooth focus ring animation for inputs
  - Button press scale effect
  - Background gradient floating animation
- Tailwind config extensions:
  - Custom lime neon color palette
  - Custom shadows (inner shadow for glossy inputs)
  - Animation keyframes
- Dark theme base styles

## Step 8: Tailwind Configuration (`tailwind.config.js`)
- Enable dark mode (class-based)
- Extend theme with:
  - Primary color: lime-400/lime-500
  - Custom shadows for glossy effect
  - Animation utilities
  - Font family (Inter or similar clean sans-serif)

## Step 9: Vite Configuration (`vite.config.js`)
- Set up dev server proxy to backend:
  - `/api` → `http://localhost:8000/api`
- Configure base path for portability
- Optimize build settings

## Technical Details

### API Integration
- Axios v1.10 with `withCredentials: true` for cookie handling
- Error handling for 401, 404, 409, 500 status codes
- Loading states during API calls
- Success callbacks for navigation

### Animations (CSS-first approach)
- Card entry: `@keyframes fadeInUp` (opacity 0→1, translateY 20px→0)
- Input focus: box-shadow transition with lime glow
- Button press: `active:scale-95` with smooth transition
- Background: Slow floating gradient blobs (CSS animation, 20s duration)
- Form toggle: Opacity + transform transition (300ms ease)

### Responsive Design
- Mobile-first approach
- Card: max-width 420px, width 90% on mobile, fixed on desktop
- Inputs: Full width with padding
- Buttons: Full width on mobile
- No fixed widths, use flexbox and max-width constraints

### Form Validation
- Client-side validation before API call
- Email format validation
- Password minimum length (8 characters)
- Real-time error display
- Disable submit during loading

### Security Considerations
- Access token stored in localStorage
- Refresh token handled by backend cookies (HTTP-only)
- Form inputs with autocomplete attributes
- Password masking by default

## File Creation Order
1. Initialize project structure (Vite + dependencies)
2. Configure Tailwind + Vite
3. Create API layer (`authApi.js`)
4. Create UI components (Button, InputField, LoadingSpinner)
5. Create auth components (LoginForm, SignupForm, AuthToggle)
6. Create state hook (`useAuth.js`)
7. Create main App component
8. Add global styles and animations
9. Test and verify all features

## Testing Checklist
- Login form submission with valid credentials
- Signup form submission with valid data
- Error handling (invalid email, wrong password, duplicate email)
- Loading states during API calls
- Password visibility toggle
- Form toggle between Login/Signup
- Responsive layout